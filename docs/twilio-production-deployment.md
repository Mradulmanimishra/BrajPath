# BrajPath Twilio Production Deployment Guide

This guide is for deploying the current BrajPath project to production with Twilio WhatsApp.

## What is already production-aware in the code

- Twilio signature validation is enabled outside `APP_ENV=development` in `app/api/webhook.py`.
- `PUBLIC_WEBHOOK_BASE_URL` is supported so Twilio validation still works behind reverse proxies and load balancers.
- Health endpoints exist at `/` and `/health`.
- The app can run on SQLite locally and PostgreSQL in production.

## Recommended production environment variables

```env
APP_ENV=production
DATABASE_URL=postgresql://user:password@host:5432/brajpath
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
PUBLIC_WEBHOOK_BASE_URL=https://your-domain.example.com
ADMIN_WA_NUMBER=+91XXXXXXXXXX
APP_TIMEZONE=Asia/Kolkata
LOG_LEVEL=INFO
```

## Deployment checklist

1. Deploy with HTTPS only.
2. Set `APP_ENV=production`.
3. Set a real PostgreSQL `DATABASE_URL`.
4. Set `PUBLIC_WEBHOOK_BASE_URL` to the exact public base URL Twilio will call.
5. Seed the database before live traffic.
6. Point Twilio WhatsApp webhook to:

```text
https://your-domain.example.com/whatsapp/webhook
```

7. Verify the health endpoint:

```text
https://your-domain.example.com/health
```

## Docker deployment

Build:

```bash
docker build -t brajpath .
```

Run:

```bash
docker run --rm -p 8000:8000 --env-file .env brajpath
```

## Twilio production requirements

- Use a production-approved WhatsApp sender, not just the sandbox.
- Keep Twilio request validation enabled in production.
- Make sure the public URL seen by Twilio matches `PUBLIC_WEBHOOK_BASE_URL`.

## Recommended next production steps

- move from `Base.metadata.create_all(...)` to managed Alembic migrations
- add structured JSON logging
- add request rate limiting and alerting
- add monitoring for webhook errors and DB failures
- store secrets in a managed secret store instead of plain `.env`

## Official references

- Twilio WhatsApp API: https://www.twilio.com/docs/whatsapp/api
- Twilio WhatsApp Sandbox: https://www.twilio.com/docs/whatsapp/sandbox
- Twilio request validation: https://www.twilio.com/docs/usage/security
