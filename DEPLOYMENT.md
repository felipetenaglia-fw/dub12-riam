# RIAM LMS - AWS Deployment Guide

## Prerequisites

1. **AWS CLI** configured with credentials
   ```bash
   aws configure --profile hackaton
   # Or use default profile
   ```

2. **AWS CDK** installed
   ```bash
   npm install -g aws-cdk
   ```

3. **Python 3.12+** with pip

4. **Docker** running (for building container images)

## Deployment Steps

### 1. Verify AWS Credentials

```bash
aws sts get-caller-identity --profile hackaton
```

### 2. Install CDK Dependencies

```bash
cd infra
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Bootstrap CDK (First Time Only)

```bash
cdk bootstrap aws://ACCOUNT-ID/us-west-2 --profile hackaton
```

Replace `ACCOUNT-ID` with your AWS account ID.

### 4. Build and Test API Docker Image Locally (Optional)

```bash
cd ../api
docker build -t riam-lms-api:test .

# Test the image
docker run -p 8000:8000 \
  -e AWS_REGION=us-west-2 \
  -e AWS_ACCESS_KEY_ID=your-key \
  -e AWS_SECRET_ACCESS_KEY=your-secret \
  riam-lms-api:test

# Visit http://localhost:8000/docs to test
```

### 5. Synthesize CDK Stack (Dry Run)

```bash
cd ../infra
cdk synth --profile hackaton
```

This will show you what resources will be created without deploying them.

### 6. Deploy the Stack

```bash
cd infra
cdk deploy --profile hackaton --require-approval never
```

This will:
- Create an S3 bucket for recordings
- Deploy the API as an ECS Fargate service behind an ALB
- Create an S3 bucket for the static UI
- Deploy the UI to S3 with CloudFront distribution
- Grant Bedrock permissions for AI Coach feature

**Note:** The deployment takes ~10-15 minutes.

### 7. Update UI with API Endpoint

After deployment, CDK will output the API URL. Update the static UI configuration:

```bash
# Copy the ApiUrl from CDK output
API_URL="http://RiamL-RiamL-xxxxx.us-west-2.elb.amazonaws.com"

# Update config.js
./update-api-endpoint.sh "$API_URL"

# Redeploy UI only
cdk deploy --profile hackaton --hotswap
```

### 8. Access the Application

The CDK output will show:
- **UiUrl**: CloudFront URL for the web interface
- **ApiUrl**: Load balancer URL for the API
- **ApiDocsUrl**: Swagger documentation URL

```
✅  RiamLmsStack

Outputs:
RiamLmsStack.ApiDocsUrl = http://RiamL-RiamL-xxxxx.us-west-2.elb.amazonaws.com/docs
RiamLmsStack.ApiUrl = http://RiamL-RiamL-xxxxx.us-west-2.elb.amazonaws.com
RiamLmsStack.UiUrl = https://d1234567890.cloudfront.net
RiamLmsStack.LoadBalancerDNS = RiamL-RiamL-xxxxx.us-west-2.elb.amazonaws.com
RiamLmsStack.S3BucketName = riam-lms-recordings-123456789012
RiamLmsStack.UiBucketName = riam-lms-ui-123456789012
```

Visit the **UiUrl** to access the application!

## Testing the Deployment

1. **Health Check**
   ```bash
   curl http://<LoadBalancerDNS>/health
   # Should return: {"status":"healthy"}
   ```

2. **API Documentation**
   Visit `http://<LoadBalancerDNS>/docs` in your browser

3. **Login to UI**
   - Visit the CloudFront URL
   - Login with: `student` / `student`
   - Upload an audio file to test AI Coach

## Monitoring

### View ECS Service Logs

```bash
aws logs tail /ecs/riam-lms-api --follow --profile hackaton
```

### Check ECS Service Status

```bash
aws ecs describe-services \
  --cluster riam-lms-cluster \
  --services riam-lms-api \
  --profile hackaton
```

## Updating the Deployment

### API Code Changes

```bash
cd infra
cdk deploy --profile hackaton
```

CDK will automatically rebuild and redeploy the Docker image.

### UI Changes

```bash
cd infra
cdk deploy --profile hackaton --hotswap
```

The `--hotswap` flag enables faster deployments for static assets.

## Cost Estimation

Monthly costs (approximate, us-west-2):
- **ECS Fargate**: $15-20 (512 CPU, 1GB RAM, 1 task)
- **ALB**: $18-20
- **S3 + CloudFront**: $1-5 (low traffic)
- **Bedrock**: Pay-per-use (~$0.01-0.02 per AI analysis)

**Total**: ~$35-50/month for low traffic

## Teardown

To delete all resources and stop incurring costs:

```bash
cd infra
cdk destroy --profile hackaton
```

⚠️ **Warning:** This will delete:
- All S3 buckets (including recordings)
- The database (SQLite, stored in container)
- All ECS resources

## Troubleshooting

### Container fails to start

Check ECS logs:
```bash
aws logs tail /ecs/riam-lms-api --follow --profile hackaton
```

Common issues:
- Missing Bedrock permissions
- S3 bucket access denied
- Audio dependencies missing

### AI Coach not working

1. Verify Bedrock model access:
   ```bash
   aws bedrock list-foundation-models \
     --region us-west-2 \
     --profile hackaton | grep claude-3-5-sonnet
   ```

2. Check ECS task IAM role has Bedrock permissions

3. Verify region is `us-west-2` (Claude 3.5 Sonnet v2 availability)

### UI not loading from CloudFront

1. Check S3 bucket has files:
   ```bash
   aws s3 ls s3://riam-lms-ui-ACCOUNT-ID/ --profile hackaton
   ```

2. Invalidate CloudFront cache:
   ```bash
   aws cloudfront create-invalidation \
     --distribution-id <DISTRIBUTION-ID> \
     --paths "/*" \
     --profile hackaton
   ```

3. Check config.js has correct API_BASE_URL

## Production Recommendations

Before going to production:

1. **Use Custom Domain**
   - Register domain in Route 53
   - Add custom domain to CloudFront
   - Use ACM certificate for HTTPS

2. **Secure CORS**
   - Update `api/app/main.py` to restrict CORS origins
   - Only allow your CloudFront domain

3. **Database**
   - Replace SQLite with RDS PostgreSQL/MySQL
   - Enable backups

4. **Monitoring**
   - Enable CloudWatch alarms for ECS CPU/Memory
   - Set up API Gateway for rate limiting

5. **S3 Bucket Policies**
   - Change `RemovalPolicy.DESTROY` to `RETAIN`
   - Enable versioning for recordings bucket

6. **Secrets Management**
   - Use AWS Secrets Manager for sensitive configs
   - Rotate JWT secret keys

## Support

For issues or questions, refer to:
- [AWS CDK Documentation](https://docs.aws.amazon.com/cdk/)
- [ECS Troubleshooting](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/troubleshooting.html)
- [Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
