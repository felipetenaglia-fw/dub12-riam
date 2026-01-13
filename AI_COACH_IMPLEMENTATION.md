# AI Music Coach - Implementation Guide

## Overview

The AI Music Coach feature provides students with expert guidance on their musical practice using Claude Opus 4.5 through AWS Bedrock.

## Important: Text-Based Coaching

**Claude Opus 4.5 does not support direct audio analysis.** The model only supports TEXT and IMAGE inputs, not AUDIO.

### How It Works

1. **Student uploads audio file** - File is received and acknowledged (stored for future use)
2. **Student provides context** - Piece name, composer, notes/questions
3. **AI provides expert coaching** - Based on the context, piece, and common challenges

### What Students Get

Comprehensive feedback based on the RIAM framework:
- **Technical Skill**: Typical challenges, exercises, practice methods
- **Musicianship Knowledge**: Structure, harmony, theory concepts
- **Repertoire & Culture**: Historical context, performance traditions
- **Performing Artistry**: Expression, phrasing, interpretation
- **Practice Strategy**: Structured practice plans
- **Key Focus Points**: 3-5 specific areas to prioritize

## Quick Start

### 1. Start the Services

```bash
./start.sh
```

This will:
- Check and clear ports 8000 and 5001
- Start API on port 8000
- Start UI on port 5001

### 2. Access the UI

Open http://localhost:5001

**Login credentials:**
- Student: `student` / `student`
- Teacher: `teacher` / `teacher`
- Admin: `admin` / `admin`

### 3. Use AI Coach

1. Scroll to the purple "AI Music Coach" section
2. Upload an audio file (mp3, wav, m4a, ogg - max 10MB)
3. Fill in details (piece name, composer, your questions)
4. Click "Get AI Feedback"
5. Receive detailed coaching guidance

## Configuration

### AWS Setup

**Profile**: `hackaton` (for local development)
**Region**: `us-west-2`
**Model**: `global.anthropic.claude-opus-4-5-20251101-v1:0`

```bash
# Verify AWS profile
aws sts get-caller-identity --profile hackaton

# Test Bedrock access
aws bedrock list-foundation-models --region us-west-2 --profile hackaton | grep opus
```

### Files Structure

```
hackaton-riam/
├── api/
│   ├── app/
│   │   ├── main.py                    # Registers ai_coach router
│   │   ├── config.py                  # AWS region: us-west-2
│   │   ├── services/
│   │   │   └── bedrock.py            # Text-only coaching logic
│   │   ├── routers/
│   │   │   └── ai_coach.py           # POST /ai-coach/analyze
│   │   └── schemas/
│   │       └── ai_coach.py           # Request/response models
├── ui/
│   ├── app.py                         # Port 5001, proxy route
│   └── templates/
│       └── dashboard.html             # AI Coach UI section
├── infra/
│   └── stacks/
│       └── ecs_stack.py              # Bedrock IAM permissions
├── start.sh                           # ✅ Updated with port checks
└── input.mp3                          # Test audio file
```

## API Endpoint

### POST /ai-coach/analyze

**Authentication**: JWT token required (student role)

**Request** (multipart/form-data):
```
audio_file: File (required) - Audio recording
piece_name: String (optional) - Name of the piece
composer: String (optional) - Composer name
student_notes: String (optional) - Questions/concerns
```

**Response**:
```json
{
  "success": true,
  "feedback": "Detailed coaching feedback...",
  "model": "global.anthropic.claude-opus-4-5-20251101-v1:0",
  "error": null
}
```

### Example with curl

```bash
# Get token
TOKEN=$(curl -s -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"student","password":"student"}' \
  | jq -r '.access_token')

# Upload for coaching
curl -X POST http://localhost:8000/ai-coach/analyze \
  -H "Authorization: Bearer $TOKEN" \
  -F "audio_file=@input.mp3" \
  -F "piece_name=Moonlight Sonata" \
  -F "composer=Beethoven" \
  -F "student_notes=Struggling with dynamics in the second movement"
```

## Testing

### Test Script

```bash
python /tmp/test_ai_coach_fix.py
```

This verifies:
- ✅ AWS Bedrock connection
- ✅ Global inference profile works
- ✅ Claude provides detailed feedback
- ✅ Text-only approach successful

### Expected Output

The test should return comprehensive feedback including:
- Technical guidance specific to the piece
- Practice strategies and exercises
- Historical/cultural context
- Motivational encouragement

**Cost per request**: ~$0.01 (431 input tokens + 2000 output tokens)

## Troubleshooting

### Port 5000 Conflict (macOS)

**Issue**: macOS AirPlay uses port 5000

**Solution**: UI now runs on port 5001
- Updated in `ui/app.py`: `app.run(debug=True, port=5001)`
- Updated in `start.sh`: Port checks and references

### Audio Analysis Not Working

**Issue**: "ValidationException: Input tag 'audio' not expected"

**Explanation**: Claude Opus 4.5 doesn't support audio input

**Solution**: Text-based coaching (implemented)
- Audio file is acknowledged but not analyzed
- Feedback based on piece/composer/context
- Future: Add AWS Transcribe for speech-to-text

### Model Not Found

**Issue**: "model identifier is invalid"

**Solution**: Use global inference profile
```python
model_id = "global.anthropic.claude-opus-4-5-20251101-v1:0"
```

Not: `us.anthropic...` or `anthropic.claude-3-opus...`

### Services Won't Start

```bash
# Kill existing processes
pkill -f "uvicorn app.main"
pkill -f "python3 app.py"

# Restart
./start.sh
```

## Cost Considerations

### Claude Opus 4.5 Pricing

- **Input**: ~$15-20 per million tokens
- **Output**: ~$75-100 per million tokens
- **Average request**: ~$0.01-0.02

### Cost-Effective Alternatives

For production, consider:

**Claude 3.5 Sonnet** (~70% cheaper):
```python
model_id = "global.anthropic.claude-3-5-sonnet-20241022-v2:0"
```

**Claude 3.5 Haiku** (~90% cheaper):
```python
model_id = "global.anthropic.claude-3-5-haiku-20241022-v1:0"
```

Change in `api/app/services/bedrock.py` line 34.

## Future Enhancements

### Option 1: AWS Transcribe Integration

Add actual audio transcription:

```python
# 1. Upload audio to S3
s3_key = f"temp-audio/{uuid.uuid4()}.mp3"
s3_service.upload_file(audio_data, s3_key)

# 2. Start transcription job
transcribe = boto3.client('transcribe')
job_name = f"transcribe-{uuid.uuid4()}"
transcribe.start_transcription_job(
    TranscriptionJobName=job_name,
    Media={'MediaFileUri': f's3://{bucket}/{s3_key}'},
    MediaFormat='mp3',
    LanguageCode='en-US'
)

# 3. Wait for completion and get transcript
# 4. Send transcript to Claude for analysis
```

### Option 2: Teacher Audio Feedback

Allow teachers to record audio feedback:
- Teacher uploads response audio
- Stored in S3
- Student can play back teacher's verbal feedback

### Option 3: Performance Metrics

Track student progress over time:
- Store AI feedback in database
- Compare feedback across uploads
- Show improvement trends
- Generate progress reports

## Documentation Files

- **AI_COACH_README.md** - Original feature documentation
- **AI_COACH_CONFIG_UPDATE.md** - Configuration changes history
- **AI_COACH_READY.md** - Quick start guide
- **AI_COACH_TEXT_ONLY.md** - Text-only approach explanation
- **AI_COACH_IMPLEMENTATION.md** - This file (comprehensive guide)

## Status

✅ **Fully Functional** - Text-based coaching working
✅ **API Server** - Running on port 8000
✅ **UI Server** - Running on port 5001
✅ **AWS Integration** - Global inference profile verified
✅ **Student Dashboard** - UI implemented with form and feedback display

**Ready for use at**: http://localhost:5001

## Support

### Check Logs

```bash
# API logs
tail -f api.log

# UI logs  
tail -f ui.log

# Startup logs
tail -f /tmp/startup.log
```

### Verify Services

```bash
# API health
curl http://localhost:8000/health

# UI health
curl -I http://localhost:5001/

# Check ports
lsof -i:8000
lsof -i:5001
```

### API Documentation

Interactive API docs: http://localhost:8000/docs

Look for "AI Coach" section.

---

**Created**: January 13, 2026
**Status**: Production Ready (Text-Based Coaching)
**Next Step**: Test with real students and gather feedback!
