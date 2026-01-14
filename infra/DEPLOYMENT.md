# RIAM LMS Deployment Guide

This guide explains how to deploy the RIAM Learning Management System to AWS using CDK.

## Prerequisites

- AWS CLI configured with credentials
- Node.js 18+ and npm
- Python 3.9+
- Docker (for building container images)

## Deployment Steps

### 1. Install Dependencies

```bash
cd infra
npm install -g aws-cdk
pip install -r requirements.txt
```

### 2. Bootstrap CDK (First Time Only)

```bash
cdk bootstrap
```

### 3. Deploy the Stack

```bash
cdk deploy
```

This will deploy:
- **ECS Fargate Service** - API backend
- **Application Load Balancer** - API endpoint
- **S3 Bucket** - Audio recordings storage
- **S3 Bucket + CloudFront** - Static UI hosting
- **IAM Roles** - Permissions for S3 and Bedrock

### 4. Get Deployment Outputs

After deployment completes, CDK will output:

```
Outputs:
RiamLmsStack.ApiUrl = http://riam-xxx.us-west-2.elb.amazonaws.com
RiamLmsStack.UiUrl = https://d1234567890.cloudfront.net
RiamLmsStack.LoadBalancerDNS = riam-xxx.us-west-2.elb.amazonaws.com
RiamLmsStack.S3BucketName = riam-lms-recordings-123456789012
RiamLmsStack.UiBucketName = riam-lms-ui-123456789012
```

### 5. Update UI Configuration

The UI needs to know the API endpoint. Update the config file:

**Option A: Update before deployment**

Edit `new_ui/config.js` and set the API URL:

```javascript
window.RIAM_CONFIG = {
    apiBaseUrl: 'https://your-api-url-here.com',
};
```

Then redeploy:
```bash
cdk deploy
```

**Option B: Update after deployment directly in S3**

1. Download the config file from S3:
```bash
aws s3 cp s3://riam-lms-ui-123456789012/config.js ./config.js
```

2. Edit `config.js` and update the `apiBaseUrl`:
```javascript
window.RIAM_CONFIG = {
    apiBaseUrl: 'http://riam-xxx.us-west-2.elb.amazonaws.com',
};
```

3. Upload back to S3:
```bash
aws s3 cp ./config.js s3://riam-lms-ui-123456789012/config.js
```

4. Invalidate CloudFront cache:
```bash
aws cloudfront create-invalidation --distribution-id YOUR_DISTRIBUTION_ID --paths "/config.js"
```

### 6. Update CORS Settings (Important!)

The API needs to allow requests from the CloudFront domain. Update `api/app/config.py`:

```python
cors_origins = [
    "https://d1234567890.cloudfront.net",  # Your CloudFront URL
    "http://localhost:5001",  # Keep for local dev
]
```

Then redeploy:
```bash
cdk deploy
```

### 7. Access the Application

Open the CloudFront URL in your browser:
```
https://d1234567890.cloudfront.net
```

**Default Credentials:**
- Student: `student` / `student`
- Teacher: `teacher` / `teacher`
- Admin: `admin` / `admin`

## Architecture

```
┌─────────────┐      HTTPS      ┌──────────────┐
│   Browser   │ ────────────────> │  CloudFront  │
└─────────────┘                  └──────────────┘
                                        │
                                        │ S3 Origin
                                        ▼
                                 ┌──────────────┐
                                 │  S3 (UI)     │
                                 │  new_ui/     │
                                 └──────────────┘
                                        
┌─────────────┐      HTTP       ┌──────────────┐
│  CloudFront │ ────────────────> │     ALB      │
│   (API)     │                  └──────────────┘
└─────────────┘                         │
                                        │ Forward
                                        ▼
                                 ┌──────────────┐
                                 │ ECS Fargate  │
                                 │  FastAPI     │
                                 └──────────────┘
                                        │
                    ┌───────────────────┼────────────────────┐
                    │                   │                    │
                    ▼                   ▼                    ▼
             ┌─────────────┐     ┌─────────────┐    ┌──────────────┐
             │ S3 Bucket   │     │  Bedrock    │    │   SQLite     │
             │ Recordings  │     │  Claude AI  │    │  (Container) │
             └─────────────┘     └─────────────┘    └──────────────┘
```

## Monitoring

### CloudWatch Logs

API logs are in CloudWatch Logs:
```bash
aws logs tail /ecs/riam-lms-api --follow
```

### ECS Service Status

```bash
aws ecs describe-services \
  --cluster riam-lms-cluster \
  --services riam-lms-api
```

### Load Balancer Health

Check target health:
```bash
aws elbv2 describe-target-health \
  --target-group-arn <TARGET_GROUP_ARN>
```

## Scaling

The API automatically scales based on CPU utilization:
- **Min Capacity**: 1 task
- **Max Capacity**: 3 tasks
- **Target CPU**: 70%

To adjust scaling settings, edit `infra/stacks/ecs_stack.py`:

```python
scaling = fargate_service.service.auto_scale_task_count(
    min_capacity=1,
    max_capacity=5,  # Increase max capacity
)
```

## Costs

**Estimated monthly costs (us-west-2):**
- ECS Fargate (1 task): ~$15-20
- Application Load Balancer: ~$16
- S3 Storage (UI): <$1
- S3 Storage (Recordings): ~$0.023/GB
- CloudFront: ~$0.085/GB (first 10TB)
- Bedrock (Claude): Pay per use (~$0.003/1K input tokens)

**Total**: ~$35-40/month + usage-based costs

## Teardown

To delete all resources:

```bash
cd infra
cdk destroy
```

⚠️ **Warning**: This will delete all data including recordings and the database.

## Troubleshooting

### UI shows "Failed to fetch"

- Check that the API URL in `config.js` is correct
- Verify CORS settings in API allow CloudFront domain
- Check API health: `curl http://<ALB_DNS>/health`

### API tasks failing to start

- Check CloudWatch logs for errors
- Verify IAM permissions for S3 and Bedrock
- Ensure Docker image built correctly for AMD64

### CloudFront shows 403 errors

- Verify S3 bucket has files deployed
- Check CloudFront OAI has read permissions
- Try invalidating cache: `aws cloudfront create-invalidation --distribution-id ID --paths "/*"`

### Database reset needed

The database is stored in the container and resets on each deployment. For persistent storage:

1. Use RDS instead of SQLite
2. Or mount EFS volume to ECS tasks

## Production Recommendations

Before going to production:

1. **SSL Certificate**: Add ACM certificate to ALB and CloudFront
2. **Custom Domain**: Use Route 53 with custom domain
3. **Database**: Migrate from SQLite to RDS PostgreSQL
4. **Secrets**: Use AWS Secrets Manager for JWT secret
5. **CORS**: Restrict to specific domains only
6. **Logging**: Enable access logs for ALB and CloudFront
7. **WAF**: Add AWS WAF for DDoS protection
8. **Backup**: Enable S3 versioning and lifecycle policies
9. **Monitoring**: Set up CloudWatch alarms for errors/latency
10. **CI/CD**: Set up GitHub Actions or CodePipeline

## Support

For issues or questions, refer to:
- `AGENTS.md` - Developer guidelines
- `api/README.md` - API documentation
- AWS CDK docs: https://docs.aws.amazon.com/cdk/
