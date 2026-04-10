# Quick Start

## Docker Compose (Recommended)

```bash
git clone https://github.com/abderrahmen-bchini/bank-chat-bot-.git
cd bank-chat-bot-

cp .env.example .env
docker-compose up -d
```

Access points:
- API: http://localhost:8000
- Frontend: http://localhost:3000
- Qdrant: http://localhost:6333/dashboard
- API Docs: http://localhost:8000/docs

## Manual Setup

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn api.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm start
```

### Services

Run in separate terminals:

PostgreSQL:
```bash
docker run -p 5432:5432 -e POSTGRES_PASSWORD=bankpass postgres:15-alpine
```

Qdrant:
```bash
docker run -p 6333:6333 qdrant/qdrant
```

Ollama:
```bash
ollama run mistral
```

## Initial Setup

Create admin user:
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@bank.com",
    "password": "password",
    "role": "admin"
  }'
```

## Common Commands

```bash
# View logs
docker logs bank-chatbot-backend -f

# Stop services
docker-compose down

# Reset database
docker-compose down -v

# Run tests
pytest tests/ -v

# Build frontend
cd frontend && npm run build
```

## Troubleshooting

Port in use:
```bash
lsof -i :8000    # macOS/Linux
netstat -ano | findstr :8000  # Windows
```

Database connection error:
```bash
psql -U bankuser -d bankchatbot
```

LLM not responding:
```bash
curl http://localhost:11434/api/tags
ollama pull mistral
```

---

See [../README.md](../README.md) for full documentation.
