# AI Coach Configuration Update

## Changes Made

Updated the AI Coach feature to use AWS Bedrock's **cross-region inference** with Claude Opus 4.5.

### Configuration Changes

#### 1. Region Update (`api/app/config.py`)
```python
# Before
aws_region: str = "eu-west-1"

# After
aws_region: str = "us-west-2"  # Bedrock region
```

#### 2. Model ID Update (`api/app/services/bedrock.py`)
```python
# Before
self.model_id = "anthropic.claude-3-opus-20240229-v1:0"

# After - Using GLOBAL cross-region inference profile
self.model_id = "global.anthropic.claude-opus-4-5-20251101-v1:0"
```

**Note**: The `global.` prefix indicates worldwide routing across all AWS regions.

#### 3. CDK Permissions Update (`infra/stacks/ecs_stack.py`)
```python
# Updated to use global inference profile ARN
resources=[
    # Global cross-region inference profile for Claude Opus 4.5
    f"arn:aws:bedrock:{self.region}::inference-profile/global.anthropic.claude-opus-4-5-20251101-v1:0",
]
```

## What is Cross-Region Inference?

AWS Bedrock's **global** cross-region inference automatically routes requests to the best available region worldwide for:
- **Maximum availability**: Falls back across ALL AWS regions
- **Optimal latency**: Routes to closest available region globally
- **Highest throughput**: Distributes load across the entire AWS network

The **global** inference profile ID: `global.anthropic.claude-opus-4-5-20251101-v1:0`
- Prefix: `global.` indicates worldwide routing (not limited to US/EU)
- Model: `anthropic.claude-opus-4-5-20251101-v1:0`
- Version: Specific model version with date (2025-11-01)

## Benefits

1. **Improved Reliability**: Automatic failover if a region has issues
2. **Better Performance**: Intelligent routing to optimal region
3. **Simplified Management**: Single profile ID works across regions
4. **Future-Proof**: AWS manages regional availability automatically

## Testing

The API server has been restarted with the new configuration. You can now test the AI Coach feature:

1. Navigate to http://localhost:5000
2. Login as `student` / `student`
3. Scroll to the AI Music Coach section
4. Upload an audio file
5. Get instant feedback from Claude Opus 4.5

## Troubleshooting

If you still get "model identifier is invalid" error:

1. **Verify AWS profile works:**
```bash
aws sts get-caller-identity --profile hackaton --region us-west-2
```

2. **Check Bedrock access:**
```bash
aws bedrock list-foundation-models --region us-west-2 --profile hackaton | grep opus
```

3. **Test inference profile directly:**
```bash
aws bedrock invoke-model \
  --model-id global.anthropic.claude-opus-4-5-20251101-v1:0 \
  --region us-west-2 \
  --profile hackaton \
  --body '{"anthropic_version":"bedrock-2023-05-31","max_tokens":100,"messages":[{"role":"user","content":[{"type":"text","text":"Hello"}]}]}' \
  /tmp/test-response.json && cat /tmp/test-response.json
```

4. **Check API logs:**
```bash
tail -f /tmp/api.log
```

## Cost Implications

Claude Opus 4.5 is the most advanced and expensive model:
- **Input**: ~$15-20 per million tokens
- **Output**: ~$75-100 per million tokens
- **3-minute audio file**: ~$15-25 per analysis

For production, consider:
- Claude 3.5 Sonnet v2: `global.anthropic.claude-3-5-sonnet-20241022-v2:0` (~70% cost reduction)
- Claude 3.5 Haiku: `global.anthropic.claude-3-5-haiku-20241022-v1:0` (~90% cost reduction)

To change models, update `self.model_id` in `api/app/services/bedrock.py`

## Status

✅ Configuration updated
✅ API server restarted
✅ Ready for testing with cross-region inference
