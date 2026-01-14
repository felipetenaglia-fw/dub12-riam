# AWS Credentials Configuration

This document explains how AWS credentials are handled in different environments.

## Overview

The application supports three credential methods with automatic detection:

1. **IAM Role** (ECS/EC2) - Automatic, no configuration needed
2. **AWS Profile** (Local development) - Uses `~/.aws/credentials`
3. **Access Keys** (Manual) - Explicit credentials in `.env`

## Local Development

### Option 1: AWS Profile (Recommended)

1. Create `.env` file from example:
   ```bash
   cd api
   cp .env.example .env
   ```

2. Set your AWS profile in `.env`:
   ```bash
   AWS_PROFILE=hackaton
   AWS_REGION=us-west-2
   ```

3. Ensure your AWS credentials file has the profile:
   ```bash
   cat ~/.aws/credentials
   ```
   
   Should contain:
   ```ini
   [hackaton]
   aws_access_key_id = YOUR_ACCESS_KEY
   aws_secret_access_key = YOUR_SECRET_KEY
   ```

4. If using SSO, refresh your token:
   ```bash
   aws sso login --profile hackaton
   ```

### Option 2: Explicit Access Keys

In `.env`:
```bash
AWS_REGION=us-west-2
AWS_ACCESS_KEY_ID=YOUR_ACCESS_KEY
AWS_SECRET_ACCESS_KEY=YOUR_SECRET_KEY
# Leave AWS_PROFILE empty
AWS_PROFILE=
```

⚠️ **Warning**: Never commit `.env` with real credentials!

## ECS/Production

When deployed to ECS, the application automatically uses the IAM role attached to the ECS task. No configuration needed!

### How it Works

The code detects the AWS environment by checking:
- `AWS_EXECUTION_ENV` environment variable
- `ECS_CONTAINER_METADATA_URI` environment variable

If either is present, it uses the IAM role credentials automatically.

### Required IAM Permissions

The ECS task role needs these permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:Converse",
        "bedrock:ConverseStream"
      ],
      "Resource": [
        "arn:aws:bedrock:us-west-2::foundation-model/us.anthropic.claude-3-5-sonnet-20241022-v2:0"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject"
      ],
      "Resource": "arn:aws:s3:::riam-lms-recordings-*/*"
    }
  ]
}
```

These permissions are automatically configured by the CDK stack in `infra/stacks/ecs_stack.py`.

## Credential Priority

The application checks credentials in this order:

1. **Is running in AWS?** → Use IAM role
2. **Has AWS_PROFILE set?** → Use profile from `~/.aws/credentials`
3. **Has AWS_ACCESS_KEY_ID?** → Use explicit keys
4. **None of above?** → Use default credential chain (environment vars, instance metadata)

## Troubleshooting

### Error: "Token has expired and refresh failed"

This happens when using SSO profiles and the token expired.

**Solution**:
```bash
aws sso login --profile hackaton
```

### Error: "Unable to locate credentials"

**Check**:
1. `.env` file exists in `api/` directory
2. `AWS_PROFILE` is set correctly
3. Profile exists in `~/.aws/credentials`
4. SSO token is valid (if using SSO)

**Debug**:
```bash
# Check which credentials are being used
aws sts get-caller-identity --profile hackaton

# Test Bedrock access
aws bedrock list-foundation-models --region us-west-2 --profile hackaton
```

### Error: "Access Denied"

Your AWS credentials don't have Bedrock permissions.

**Solution**:
1. Ensure you're using the correct AWS account
2. Request Bedrock access from AWS admin
3. Verify IAM permissions include `bedrock:InvokeModel`

## Environment Variables Reference

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `AWS_REGION` | AWS region for Bedrock/S3 | Yes | `us-west-2` |
| `AWS_PROFILE` | Profile name from `~/.aws/credentials` | Local only | empty |
| `AWS_ACCESS_KEY_ID` | Explicit access key | Optional | empty |
| `AWS_SECRET_ACCESS_KEY` | Explicit secret key | Optional | empty |
| `S3_BUCKET_NAME` | S3 bucket for recordings | Yes | `riam-lms-recordings` |

## Logging

The application logs which credential method is being used:

```
[INFO] Using AWS profile: hackaton
[INFO] Bedrock client initialized successfully for region: us-west-2
```

or

```
[INFO] Running in AWS environment - using IAM role credentials
[INFO] Bedrock client initialized successfully for region: us-west-2
```

Check the logs to verify the correct method is being used.

## Security Best Practices

### Local Development

✅ **DO**:
- Use AWS profiles (`AWS_PROFILE`)
- Keep `.env` file in `.gitignore`
- Use SSO when possible
- Rotate credentials regularly

❌ **DON'T**:
- Commit `.env` file
- Share credentials in chat/email
- Use root account credentials
- Hard-code credentials in code

### Production (ECS)

✅ **DO**:
- Use IAM roles (automatic)
- Follow principle of least privilege
- Enable CloudTrail for auditing
- Rotate task role regularly

❌ **DON'T**:
- Use access keys in ECS
- Grant `*` permissions
- Share task role across environments
- Disable credential rotation

## Testing Credentials

Test your setup:

```bash
# Start the API
cd api
uvicorn app.main:app --reload

# Check logs for:
# "[INFO] Using AWS profile: hackaton"
# or
# "[INFO] Running in AWS environment - using IAM role credentials"

# Test API endpoint
curl http://localhost:8000/health

# Test AI Coach (with auth)
curl -X POST http://localhost:8000/ai-coach/chat-public \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Test question",
    "analysis_context": null
  }'
```

If you see a response, credentials are working!

## Summary

| Environment | Credential Method | Configuration |
|-------------|-------------------|---------------|
| **Local Dev** | AWS Profile | `.env`: `AWS_PROFILE=hackaton` |
| **ECS/Production** | IAM Role | Automatic (no config) |
| **Manual** | Access Keys | `.env`: `AWS_ACCESS_KEY_ID=...` |

The system automatically detects the environment and uses the appropriate credential method. For local development, use the `hackaton` AWS profile. For production ECS deployment, the IAM role is used automatically.
