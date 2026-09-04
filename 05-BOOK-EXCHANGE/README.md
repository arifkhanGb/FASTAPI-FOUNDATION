# Kitab Exchange API

## API key configuration

All write endpoints require an `X-API-Key` header. Configure the expected key
before starting the application:

```powershell
$env:API_KEY = "$(python -c "import secrets; print(secrets.token_urlsafe(32))")"
uvicorn main:app --reload
```

For local development, copy `.env.example` to `.env`; the application loads it
automatically. Environment variables take precedence over `.env`. In
production, store `API_KEY` in the platform secret manager; do not commit a
`.env` file or hard-code a key.

Example request:

```bash
curl -X POST http://127.0.0.1:8000/books/ \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"title":"Dune","author":"Frank Herbert","price":10}'
```
