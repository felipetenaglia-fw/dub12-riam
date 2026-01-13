# AI Music Coach Feature

## Overview

The AI Music Coach feature allows students to upload audio recordings of their musical performances and receive instant, detailed feedback from Claude Opus (Anthropic's most advanced AI model). The feedback is based on the RIAM framework for developing great musicians.

## Features

- **Audio Upload**: Students can upload MP3, WAV, M4A, or OGG files (max 10MB)
- **Contextual Information**: Optional fields for piece name, composer, and student notes
- **Structured Feedback**: AI provides feedback organized by RIAM categories:
  - Technical Skill and Competence
  - Compositional and Musicianship Knowledge
  - Repertoire and Cultural Knowledge
  - Performing Artistry
- **Encouragement**: Constructive, motivating feedback suitable for music students

## How It Works

### Backend (API)

**New Files Created:**
- `api/app/services/bedrock.py` - AWS Bedrock service for Claude Opus integration
- `api/app/schemas/ai_coach.py` - Pydantic schemas for request/response
- `api/app/routers/ai_coach.py` - API endpoint for audio analysis

**Endpoint:**
```
POST /ai-coach/analyze
```

**Request (multipart/form-data):**
- `audio_file` (required): Audio file
- `piece_name` (optional): Name of the musical piece
- `composer` (optional): Composer name
- `student_notes` (optional): Student's questions or context

**Response:**
```json
{
  "success": true,
  "feedback": "Detailed AI feedback text...",
  "model": "anthropic.claude-3-opus-20240229-v1:0"
}
```

### Frontend (UI)

**Modified Files:**
- `ui/templates/dashboard.html` - Added AI Coach section to student dashboard
- `ui/app.py` - Added proxy route `/api/ai-coach` to forward requests to backend

**UI Features:**
- Beautiful gradient card design with purple/indigo theme
- File upload with format validation
- Optional context fields
- Loading state with spinner
- Formatted feedback display
- Error handling

## AWS Configuration

### Region and Model

The application uses:
- **Region**: `us-west-2` 
- **Model**: Claude Opus 4.5 via **cross-region inference** (`us.anthropic.claude-opus-4-5-v1:0`)
- **Profile**: `hackaton` (for local development)

Cross-region inference automatically routes requests to the best available region for optimal performance and availability.

### Local Development

Make sure you have:

1. AWS CLI configured with the hackaton profile:
```bash
aws configure --profile hackaton
```

2. Bedrock access enabled in your AWS account (us-west-2 region)
3. Cross-region inference enabled (automatic with proper permissions)

### Production Deployment (CDK)

The CDK stack has been updated with Bedrock IAM permissions for cross-region inference:

```python
# Add Bedrock permissions for AI Coach
fargate_service.task_definition.task_role.add_to_policy(
    iam.PolicyStatement(
        effect=iam.Effect.ALLOW,
        actions=[
            "bedrock:InvokeModel",
            "bedrock:InvokeModelWithResponseStream",
        ],
        resources=[
            # Cross-region inference profile for Claude Opus 4.5
            f"arn:aws:bedrock:{self.region}::inference-profile/us.anthropic.claude-opus-4-5-v1:0",
            # Fallback to direct model access
            f"arn:aws:bedrock:{self.region}::foundation-model/anthropic.claude-opus-4-5-20251101-v1:0",
        ],
    )
)
```

When deploying to AWS ECS, the task role will have the necessary permissions to invoke Claude Opus 4.5 via cross-region inference.

## Configuration

### Environment Variables

Configuration in `api/app/config.py`:

```python
# AWS Settings
aws_region: str = "us-west-2"  # Bedrock region
aws_profile: str = "hackaton"  # For local development only
```

Model ID uses cross-region inference profile: `us.anthropic.claude-opus-4-5-v1:0`

### Profile Priority

The services check for credentials in this order:
1. **Local Development**: Use `aws_profile` (named profile from ~/.aws/credentials)
2. **Explicit Credentials**: Use `aws_access_key_id` and `aws_secret_access_key` if provided
3. **Default**: Use IAM role or environment variables (for ECS deployment)

## Usage

### For Students

1. Log in to the RIAM LMS UI at http://localhost:5000
2. Use credentials: `student` / `student`
3. Scroll to the "AI Music Coach" section (purple gradient card)
4. Upload an audio file of your performance
5. Optionally add piece name, composer, and notes
6. Click "Get AI Feedback"
7. Review the detailed feedback provided by the AI

### Testing

You can test the endpoint directly with curl:

```bash
# Get auth token first
TOKEN=$(curl -s -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"student","password":"student"}' | jq -r '.access_token')

# Upload audio for analysis
curl -X POST http://localhost:8000/ai-coach/analyze \
  -H "Authorization: Bearer $TOKEN" \
  -F "audio_file=@/path/to/your/recording.mp3" \
  -F "piece_name=Moonlight Sonata" \
  -F "composer=Beethoven" \
  -F "student_notes=I struggled with the tempo in the second movement"
```

## API Documentation

Full interactive API documentation is available at:
- Swagger UI: http://localhost:8000/docs
- Look for the "AI Coach" tag/section

## Cost Considerations

**Claude Opus Pricing (as of 2024):**
- Input: ~$15 per million tokens
- Output: ~$75 per million tokens

**Typical Usage:**
- Audio files are encoded to base64, increasing size by ~33%
- A 3-minute MP3 (3MB) ≈ 4MB base64 ≈ ~1M tokens for audio
- AI response: ~500-1000 tokens
- **Cost per analysis: ~$15-20** (mostly from audio input)

**Recommendations:**
- Consider using Claude Sonnet or Haiku for lower costs
- Implement rate limiting for production
- Add file size warnings in UI
- Consider audio compression before upload

## Security

- Endpoint is protected by JWT authentication
- Only students can access the AI coach endpoint
- File size limited to 10MB
- File type validation (mp3, wav, m4a, ogg only)
- Request timeout set to 120 seconds

## Future Enhancements

- [ ] Save AI feedback to database for history
- [ ] Compare feedback over time for progress tracking
- [ ] Link AI feedback to specific tasks
- [ ] Add audio compression/conversion
- [ ] Support for video files
- [ ] Multi-language support
- [ ] Teacher access to view student AI feedback

## Troubleshooting

### "Invalid credentials" error
- Check AWS profile configuration: `aws configure --profile hackaton`
- Verify credentials: `aws sts get-caller-identity --profile hackaton`

### "Model not found" error
- Enable model access in AWS Bedrock console
- Verify region is correct (eu-west-1)

### Timeout errors
- Check network connectivity
- Reduce audio file size
- Increase timeout in `ui/app.py` (currently 120s)

### "Address already in use" error
- Kill existing processes: `lsof -ti:8000 | xargs kill -9`
- Restart servers with `./start.sh`

## Technical Architecture

```
Student Browser
    ↓ (Upload MP3)
Flask UI (port 5000)
    ↓ (Proxy request)
FastAPI Backend (port 8000)
    ↓ (Encode to base64)
AWS Bedrock / Claude Opus
    ↓ (AI Analysis)
FastAPI Backend
    ↓ (Format response)
Flask UI
    ↓ (Display feedback)
Student Browser
```

## Files Modified/Created

### Backend
- ✅ `api/app/services/bedrock.py` - New Bedrock service
- ✅ `api/app/services/s3.py` - Updated for profile support
- ✅ `api/app/schemas/ai_coach.py` - New schemas
- ✅ `api/app/routers/ai_coach.py` - New router
- ✅ `api/app/main.py` - Register new router
- ✅ `api/app/config.py` - Add aws_profile setting

### Frontend
- ✅ `ui/templates/dashboard.html` - Add AI Coach UI
- ✅ `ui/app.py` - Add proxy route

### Infrastructure
- ✅ `infra/stacks/ecs_stack.py` - Add Bedrock IAM permissions

---

**Status**: ✅ Fully Implemented and Ready for Testing

**Servers Running**:
- API: http://localhost:8000
- UI: http://localhost:5000
- Docs: http://localhost:8000/docs
