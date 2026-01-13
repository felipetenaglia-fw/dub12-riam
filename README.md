# RIAM Learning Management System - Backend API

A comprehensive REST API for the Royal Irish Academy of Music (RIAM) Learning Management System. Built with FastAPI, deployed to AWS ECS via CDK.

## Overview

This system facilitates the relationship between music teachers and students, tracking classes, assignments, feedback, recordings, and performance metrics based on RIAM's framework of musical excellence.

### RIAM Framework Categories
1. **Technical Skill and Competence**
2. **Compositional and Musicianship Knowledge**
3. **Repertoire and Cultural Knowledge**
4. **Performing Artistry**

## Features

- **Authentication & Authorization**: JWT-based auth with role-based access control (Admin, Teacher, Student)
- **User Management**: CRUD operations for users with different roles
- **Class Sessions**: Teachers create session notes with improvement points and actions
- **Task Assignment**: Teachers assign practice and listening tasks to students
- **Student Feedback**: Students provide feedback on tasks with emotional context
- **Practice Recordings**: S3-backed file storage with presigned URLs
- **Quizzes**: Free-text quizzes for listening tasks with student responses
- **Performance Dashboard**: Comprehensive metrics for students, teachers, and admins
- **Musical Pieces Library**: Database of compositions with metadata

## Architecture

```
┌─────────────────┐
│   Application   │
│  Load Balancer  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌──────────────┐
│   ECS Fargate   │────▶│  S3 Bucket   │
│   (FastAPI)     │     │  (Recordings)│
└────────┬────────┘     └──────────────┘
         │
         ▼
┌─────────────────┐
│ SQLite In-Memory│
│    Database     │
└─────────────────┘
```

## Tech Stack

- **Framework**: FastAPI 0.109.2
- **Database**: SQLite (in-memory)
- **Authentication**: JWT (python-jose)
- **Password Hashing**: bcrypt (passlib)
- **Cloud Storage**: AWS S3 (boto3)
- **Infrastructure**: AWS CDK 2.151.0
- **Container**: Docker
- **Deployment**: AWS ECS Fargate + ALB

## Components

This project consists of three main components:
1. **Backend API** (`api/`) - FastAPI REST API with JWT auth
2. **Web UI** (`ui/`) - Flask web interface with HTMX
3. **Infrastructure** (`infra/`) - AWS CDK for deployment

## Project Structure

```
hackaton-riam/
├── api/                          # Python Backend API (FastAPI)
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── config.py            # Configuration
│   │   ├── database.py          # Database setup
│   │   ├── seed_data.py         # Mock data seeder
│   │   ├── auth/                # JWT & permissions
│   │   ├── models/              # SQLAlchemy models
│   │   ├── schemas/             # Pydantic schemas
│   │   ├── routers/             # API endpoints
│   │   └── services/            # S3 & consistency helpers
│   ├── Dockerfile
│   └── requirements.txt
├── ui/                           # Web User Interface (Flask)
│   ├── app.py                   # Flask application
│   ├── templates/               # HTML templates
│   │   ├── base.html
│   │   ├── login.html
│   │   └── dashboard.html
│   ├── static/css/style.css
│   └── requirements.txt
├── infra/                        # CDK Infrastructure
│   ├── app.py
│   ├── stacks/
│   │   └── ecs_stack.py
│   ├── cdk.json
│   └── requirements.txt
├── postman/
│   └── RIAM_LMS_API.postman_collection.json
└── README.md
```

## Quick Start

### Prerequisites

- Python 3.12+
- Docker
- AWS CLI configured
- AWS CDK CLI
- Postman (optional, for API testing)

### Local Development

#### 1. Start the Backend API

```bash
cd api
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

#### 2. Start the Web UI

In a new terminal:

```bash
cd ui
pip install -r requirements.txt
python app.py
```

The UI will be available at:
- **Web Interface**: http://localhost:5000

#### 3. Login

Use any of the mock credentials:
- **Admin**: admin / admin
- **Teacher**: teacher / teacher  
- **Student**: student / student

### Using Docker

1. **Build the Docker image**:
```bash
cd api
docker build -t riam-lms-api .
```

2. **Run the container**:
```bash
docker run -p 8000:8000 \
  -e AWS_REGION=eu-west-1 \
  -e S3_BUCKET_NAME=riam-lms-recordings \
  -e AWS_ACCESS_KEY_ID=your_key \
  -e AWS_SECRET_ACCESS_KEY=your_secret \
  riam-lms-api
```

## AWS Deployment

### Prerequisites

1. **AWS Account** with appropriate permissions
2. **AWS CLI** configured with credentials
3. **CDK Bootstrap** (first-time only):
```bash
cd infra
cdk bootstrap aws://ACCOUNT-NUMBER/REGION
```

### Deploy to AWS

1. **Install CDK dependencies**:
```bash
cd infra
pip install -r requirements.txt
```

2. **Configure your account/region** (optional):
Edit `infra/app.py` to set your AWS account and region, or use context:
```bash
cdk deploy -c account=123456789012 -c region=eu-west-1
```

3. **Deploy the stack**:
```bash
cdk deploy
```

4. **Get the outputs**:
After deployment, CDK will output:
- **LoadBalancerDNS**: The ALB DNS name
- **ApiUrl**: Base URL for the API
- **ApiDocsUrl**: Swagger UI URL
- **S3BucketName**: S3 bucket for recordings

### Update Deployment

```bash
cd infra
cdk deploy
```

### Destroy Infrastructure

```bash
cd infra
cdk destroy
```

## Mock Credentials

The system comes pre-seeded with mock users:

| Username | Password | Role | Name |
|----------|----------|------|------|
| `admin` | `admin` | Admin | RIAM Administrator |
| `teacher` | `teacher` | Teacher | Dr. Sarah Murphy |
| `teacher2` | `teacher2` | Teacher | Prof. Michael O'Brien |
| `student` | `student` | Student | Emma Walsh |
| `student2` | `student2` | Student | Liam Kelly |
| `student3` | `student3` | Student | Aoife Brennan |

### Teacher-Student Relationships
- Dr. Sarah Murphy (teacher) teaches Emma Walsh (student) and Liam Kelly (student2)
- Prof. Michael O'Brien (teacher2) teaches Aoife Brennan (student3)

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/login` | Login with username/password |
| GET | `/auth/me` | Get current user info |

### Users
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/users` | List all users | Admin |
| GET | `/users/{id}` | Get user by ID | Admin, Self |
| POST | `/users` | Create user | Admin |
| PUT | `/users/{id}` | Update user | Admin, Self |

### Classes & Notes
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| POST | `/classes` | Create class session | Teacher |
| GET | `/classes` | List sessions | Teacher, Student, Admin |
| GET | `/classes/{id}` | Get session details | Teacher, Student, Admin |
| PUT | `/classes/{id}` | Update session | Teacher |
| GET | `/classes/students/{id}/history` | Get student history | Teacher, Student, Admin |

### Tasks
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| POST | `/tasks` | Assign task | Teacher |
| GET | `/tasks` | List tasks | Teacher, Student, Admin |
| GET | `/tasks/{id}` | Get task details | Teacher, Student, Admin |
| PUT | `/tasks/{id}` | Update task | Teacher |
| PUT | `/tasks/{id}/status` | Update task status | Student, Teacher |

### Musical Pieces
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/pieces` | List pieces | All authenticated |
| GET | `/pieces/{id}` | Get piece | All authenticated |
| POST | `/pieces` | Create piece | Teacher, Admin |
| PUT | `/pieces/{id}` | Update piece | Teacher, Admin |

### Feedback
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| POST | `/tasks/{id}/feedback` | Submit feedback | Student |
| GET | `/tasks/{id}/feedback` | Get feedback | Teacher, Student, Admin |

### Recordings
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| POST | `/recordings/tasks/{id}/recordings` | Create recording entry | Student |
| GET | `/recordings/tasks/{id}/recordings` | List recordings | Teacher, Student, Admin |
| GET | `/recordings/{id}/url` | Get presigned download URL | Teacher, Student, Admin |
| GET | `/recordings/{id}/upload-url` | Get presigned upload URL | Student |

### Quizzes
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| POST | `/quizzes` | Create quiz | Teacher |
| GET | `/quizzes/{id}` | Get quiz | Teacher, Student |
| POST | `/quizzes/{id}/responses` | Submit response | Student |
| GET | `/quizzes/{id}/responses` | Get responses | Teacher, Admin |

### Performance Dashboard
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/performance/students/{id}` | Student performance | Teacher, Admin |
| GET | `/performance/teachers/{id}` | Teacher performance | Admin |
| GET | `/performance/overview` | Overall metrics | Admin |

## Using the Postman Collection

1. **Import the collection**:
   - Open Postman
   - Click "Import"
   - Select `postman/RIAM_LMS_API.postman_collection.json`

2. **Set the base URL**:
   - Go to collection variables
   - Update `base_url` to your API endpoint (local or AWS)

3. **Authenticate**:
   - Run one of the login requests (Admin, Teacher, or Student)
   - The access token will be automatically saved to collection variables
   - All subsequent requests will use this token

4. **Test the API**:
   - Explore the organized folders for different endpoints
   - Each request includes example data

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | SQLite database URL | `sqlite:///:memory:` |
| `JWT_SECRET_KEY` | JWT signing secret | `riam-lms-secret-key-change-in-production` |
| `JWT_ALGORITHM` | JWT algorithm | `HS256` |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration | `1440` (24 hours) |
| `AWS_REGION` | AWS region | `eu-west-1` |
| `S3_BUCKET_NAME` | S3 bucket name | `riam-lms-recordings` |
| `AWS_ACCESS_KEY_ID` | AWS access key | - |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key | - |

### Creating a `.env` file (Local Development)

```bash
DATABASE_URL=sqlite:///:memory:
JWT_SECRET_KEY=your-super-secret-key-change-me
AWS_REGION=eu-west-1
S3_BUCKET_NAME=riam-lms-recordings
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
```

## Data Consistency

The application enforces data consistency at the application level (not via foreign key constraints):
- Validation helpers ensure users, tasks, and relationships exist before operations
- Permission checks verify teacher-student relationships
- Role-based access control protects sensitive operations

## Security Considerations

### For Production:
1. **Change JWT Secret**: Update `JWT_SECRET_KEY` to a strong random value
2. **Use Environment Variables**: Never commit secrets to version control
3. **Enable HTTPS**: Configure SSL/TLS on the load balancer
4. **Restrict CORS**: Update CORS settings in `main.py` to allowed origins
5. **Database**: Consider migrating to RDS for persistence
6. **S3 Bucket**: Review bucket permissions and CORS settings
7. **IAM Roles**: Use least-privilege principles for ECS task roles

## Monitoring & Logs

### CloudWatch Logs
- ECS task logs are automatically sent to CloudWatch
- Log group: `/ecs/riam-lms-api`

### Health Check
- Endpoint: `/health`
- ALB performs health checks every 60 seconds

## Troubleshooting

### Local Issues

**API won't start**:
```bash
# Check Python version
python3 --version  # Should be 3.12+

# Reinstall dependencies
pip install -r requirements.txt
```

**Import errors**:
```bash
# Run from api directory
cd api
python -m uvicorn app.main:app --reload
```

### AWS Deployment Issues

**CDK deploy fails**:
```bash
# Ensure you're bootstrapped
cdk bootstrap

# Check AWS credentials
aws sts get-caller-identity
```

**ECS task fails to start**:
- Check CloudWatch logs for error messages
- Verify environment variables are set correctly
- Ensure S3 bucket exists and IAM role has permissions

**Cannot access API**:
- Check security groups allow inbound traffic on port 80/443
- Verify ALB health checks are passing
- Check ECS service events for errors

## Development

### Running Tests

```bash
cd api
pytest
```

### Code Style

The project follows PEP 8 guidelines. Format code with:
```bash
black app/
```

### Adding New Endpoints

1. Create a new router in `app/routers/`
2. Define Pydantic schemas in `app/schemas/`
3. Add database models if needed in `app/models/`
4. Register router in `app/main.py`
5. Update Postman collection

## License

Proprietary - Royal Irish Academy of Music

## Support

For issues or questions, contact the RIAM IT department.

---

**Built with by Felipe Tenaglia for RIAM Hackathon 2026**
