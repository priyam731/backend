# Pipeline Backend API

FastAPI backend for pipeline validation and DAG analysis.

## Endpoints

- `GET /` - Health check
- `POST /pipelines/parse` - Parse and validate pipeline

## Deployment

### Railway

1. Connect your GitHub repository to Railway
2. Railway will automatically detect the Python project
3. The app will start using the command in Procfile

### Local Development

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Environment Variables

- `PORT` - Set by Railway automatically
