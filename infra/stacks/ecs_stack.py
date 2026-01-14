from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_s3 as s3,
    aws_s3_deployment as s3deploy,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_iam as iam,
    aws_ecr_assets as ecr_assets,
    CfnOutput,
    RemovalPolicy,
    Duration,
)
from constructs import Construct


class RiamLmsStack(Stack):
    """CDK Stack for RIAM LMS API deployment."""

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create S3 bucket for recordings
        recordings_bucket = s3.Bucket(
            self,
            "RecordingsBucket",
            bucket_name=f"riam-lms-recordings-{self.account}",
            versioned=False,
            encryption=s3.BucketEncryption.S3_MANAGED,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy=RemovalPolicy.DESTROY,  # Change to RETAIN for production
            auto_delete_objects=True,  # Change to False for production
            cors=[
                s3.CorsRule(
                    allowed_methods=[
                        s3.HttpMethods.GET,
                        s3.HttpMethods.POST,
                        s3.HttpMethods.PUT,
                    ],
                    allowed_origins=["*"],  # Restrict in production
                    allowed_headers=["*"],
                    max_age=3000,
                )
            ],
        )

        # Create a new VPC with public subnets only for cost optimization
        vpc = ec2.Vpc(
            self,
            "VPC",
            max_azs=2,
            nat_gateways=0,  # No NAT gateways to save costs
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="Public",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24,
                )
            ],
        )

        # Create ECS cluster
        cluster = ecs.Cluster(
            self,
            "RiamLmsCluster",
            cluster_name="riam-lms-cluster",
            vpc=vpc,
        )

        # Create Fargate service with ALB
        fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            "RiamLmsService",
            cluster=cluster,
            service_name="riam-lms-api",
            cpu=512,
            memory_limit_mib=1024,
            desired_count=1,
            assign_public_ip=True,  # Required for tasks in public subnets
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_asset(
                    "../api",
                    platform=ecr_assets.Platform.LINUX_AMD64  # Force AMD64 architecture for Fargate
                ),
                container_port=8000,
                environment={
                    "AWS_REGION": self.region,
                    "S3_BUCKET_NAME": recordings_bucket.bucket_name,
                },
            ),
            public_load_balancer=True,
            health_check_grace_period=Duration.seconds(300),  # Increased to 5 minutes,
        )

        # Configure health check
        fargate_service.target_group.configure_health_check(
            path="/health",
            interval=Duration.seconds(60),
            timeout=Duration.seconds(30),
            healthy_threshold_count=2,
            unhealthy_threshold_count=5,  # Increased tolerance
        )

        # Increase ALB idle timeout for long-running AI requests (default is 60s)
        fargate_service.load_balancer.set_attribute(
            "idle_timeout.timeout_seconds", "300"  # 5 minutes
        )

        # Grant S3 permissions to the task role
        recordings_bucket.grant_read_write(fargate_service.task_definition.task_role)

        # Add S3 presigned URL permissions
        fargate_service.task_definition.task_role.add_to_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=[
                    "s3:GetObject",
                    "s3:PutObject",
                    "s3:DeleteObject",
                ],
                resources=[f"{recordings_bucket.bucket_arn}/*"],
            )
        )

        # Add Bedrock permissions for AI Coach
        fargate_service.task_definition.task_role.add_to_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=[
                    "bedrock:InvokeModel",
                    "bedrock:Converse",
                    "bedrock:ConverseStream",
                ],
                resources=[
                    # Allow all foundation models in all regions (for flexibility)
                    f"arn:aws:bedrock:*::foundation-model/*",
                    # Allow inference profiles in this region
                    f"arn:aws:bedrock:{self.region}:{self.account}:inference-profile/*",
                    # Allow global inference profiles
                    f"arn:aws:bedrock:*::inference-profile/*"
                ],
            )
        )

        # Configure auto-scaling
        scaling = fargate_service.service.auto_scale_task_count(
            min_capacity=1,
            max_capacity=3,
        )

        scaling.scale_on_cpu_utilization(
            "CpuScaling",
            target_utilization_percent=70,
            scale_in_cooldown=Duration.seconds(60),
            scale_out_cooldown=Duration.seconds(60),
        )

        # ===== STATIC UI HOSTING =====
        # Create S3 bucket for static website
        ui_bucket = s3.Bucket(
            self,
            "UiBucket",
            bucket_name=f"riam-lms-ui-{self.account}",
            website_index_document="login.html",
            website_error_document="login.html",
            public_read_access=True,
            block_public_access=s3.BlockPublicAccess(
                block_public_acls=False,
                block_public_policy=False,
                ignore_public_acls=False,
                restrict_public_buckets=False,
            ),
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            cors=[
                s3.CorsRule(
                    allowed_methods=[s3.HttpMethods.GET, s3.HttpMethods.HEAD],
                    allowed_origins=["*"],
                    allowed_headers=["*"],
                    max_age=3600,
                )
            ],
        )

        # Create CloudFront Origin Access Identity
        oai = cloudfront.OriginAccessIdentity(
            self, "UiOAI",
            comment="OAI for RIAM LMS UI"
        )
        
        ui_bucket.grant_read(oai)
        
        # Add bucket policy to allow all principals to read
        ui_bucket.add_to_resource_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                principals=[iam.AnyPrincipal()],
                actions=["s3:GetObject"],
                resources=[f"{ui_bucket.bucket_arn}/*"],
            )
        )

        # Create CloudFront distribution
        distribution = cloudfront.Distribution(
            self,
            "UiDistribution",
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3Origin(ui_bucket, origin_access_identity=oai),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                cache_policy=cloudfront.CachePolicy.CACHING_OPTIMIZED,
            ),
            default_root_object="login.html",
            error_responses=[
                cloudfront.ErrorResponse(
                    http_status=404,
                    response_http_status=200,
                    response_page_path="/login.html",
                    ttl=Duration.seconds(0),
                ),
                cloudfront.ErrorResponse(
                    http_status=403,
                    response_http_status=200,
                    response_page_path="/login.html",
                    ttl=Duration.seconds(0),
                ),
            ],
        )

        # Deploy static UI files to S3
        deployment = s3deploy.BucketDeployment(
            self,
            "UiDeployment",
            sources=[
                s3deploy.Source.asset("../new_ui"),
                s3deploy.Source.json_data("api-config.json", {
                    "apiBaseUrl": f"http://{fargate_service.load_balancer.load_balancer_dns_name}",
                    "endpoints": {
                        "aiCoach": "/ai-coach/analyze",
                        "aiCoachChat": "/ai-coach/chat",
                        "login": "/auth/login",
                        "me": "/auth/me"
                    }
                })
            ],
            destination_bucket=ui_bucket,
            distribution=distribution,
            distribution_paths=["/*"],
        )

        # Outputs
        CfnOutput(
            self,
            "LoadBalancerDNS",
            value=fargate_service.load_balancer.load_balancer_dns_name,
            description="API Load Balancer DNS",
        )

        CfnOutput(
            self,
            "ApiUrl",
            value=f"http://{fargate_service.load_balancer.load_balancer_dns_name}",
            description="API Base URL",
        )

        CfnOutput(
            self,
            "ApiDocsUrl",
            value=f"http://{fargate_service.load_balancer.load_balancer_dns_name}/docs",
            description="API Documentation (Swagger UI)",
        )

        CfnOutput(
            self,
            "S3BucketName",
            value=recordings_bucket.bucket_name,
            description="S3 Bucket for Recordings",
        )
        
        CfnOutput(
            self,
            "UiUrl",
            value=f"https://{distribution.distribution_domain_name}",
            description="Static UI URL (CloudFront)",
        )
        
        CfnOutput(
            self,
            "UiBucketName",
            value=ui_bucket.bucket_name,
            description="S3 Bucket for Static UI Files",
        )
