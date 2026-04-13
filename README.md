# BrajPath

A multilingual WhatsApp assistant for pilgrims visiting Mathura and Vrindavan.

BrajPath is designed to answer high-frequency travel and darshan questions in a simple WhatsApp-style flow. The current version focuses on temple timings, route guidance, advisories, local fare guidance, and multilingual menu navigation for key temple journeys.

## Overview

This project provides:

- A FastAPI webhook for Twilio WhatsApp integration
- A menu-driven state machine for multilingual conversations
- SQLAlchemy models for temples, schedules, routes, advisories, sessions, and logs
- Seed data for the initial temple set
- Local development support with SQLite by default
- PostgreSQL support through `DATABASE_URL`

## Current Scope

The application currently includes:

- English, Hindi, Bengali, and Tamil response support
- Seeded data for:
  - Shri Banke Bihari Mandir
  - Prem Mandir
  - ISKCON Sri Krishna Balaram Mandir
- User flows for:
  - View currently open temples
  - View temple timings
  - Get route guidance from common origin points
  - Read temple advisories
  - View fair-price guidance
  - Raise a local help request

## Tech Stack

- Python 3.11+
- FastAPI
- SQLAlchemy 2.x
- Twilio WhatsApp API
- Pydantic Settings
- SQLite for local development
- PostgreSQL via `pg8000` for deployment environments

## Project Structure

```text
braj_sahayak/
|-- app/
|   |-- api/
|   |   `-- webhook.py
|   |-- data/
|   |   `-- translations.json
|   |-- db/
|   |   |-- models.py
|   |   |-- seed.py
|   |   `-- session.py
|   |-- services/
|   |   |-- state_machine.py
|   |   `-- temple_service.py
|   |-- config.py
|   `-- main.py
|-- migrations/
|   `-- v1_schema.sql
|-- scripts/
|   `-- run_seed.py
|-- pyproject.toml
|-- requirements.txt
`-- README.md
```

## Architecture

### 1. Webhook Layer

`app/api/webhook.py` receives inbound WhatsApp messages from Twilio, validates requests, routes messages into the conversation state machine, and returns TwiML responses.

### 2. Conversation Layer

`app/services/state_machine.py` handles user intent through an explicit menu-based flow. It tracks session state, language choice, routing selections, advisory requests, and help escalation.

### 3. Domain Service Layer

`app/services/temple_service.py` contains read-oriented business logic for:

- current open/closed evaluation
- timing card generation
- route card generation
- temple advisories
- translation lookups
- user session persistence helpers

### 4. Persistence Layer

`app/db/models.py` defines the SQLAlchemy ORM models for operational data such as temples, schedules, route points, routes, advisories, user sessions, and query logs.

## Conversation Flow

The current state flow is intentionally simple and predictable:

```text
language_select
  -> main_menu
     -> open_now
     -> temple_area_select -> area_temple_select -> timing
     -> temple_area_select -> area_temple_select -> route_from_select -> route
     -> temple_area_select -> area_temple_select -> advisory
     -> fair_price
     -> partner/help flow
```

Special keywords:

- `menu` returns the user to the main menu
- `help` creates a support request

## Quick Start

### Prerequisites

- Python 3.11 or newer
- `uv` recommended for dependency management and local execution

### 1. Install dependencies

Using `uv`:

```bash
uv sync
```

Or using `pip`:

```bash
pip install -r requirements.txt
```

### 2. Configure environment

Copy the example file if you maintain one locally, or create a `.env` file manually.

Minimum useful local configuration:

```env
APP_ENV=development
DATABASE_URL=sqlite:///./brajpath.db
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
ADMIN_WA_NUMBER=
APP_TIMEZONE=Asia/Kolkata
LOG_LEVEL=INFO
```

### 3. Seed the database

```bash
uv run python -m scripts.run_seed
```

### 4. Run the API

```bash
uv run uvicorn app.main:app --reload --port 8000
```

### 5. Verify health endpoints

- `GET /`
- `GET /health`

## Testing

Run the automated bot-flow tests:

```bash
pytest -q
```

## Database Notes

### Local development

The application defaults to SQLite:

```env
DATABASE_URL=sqlite:///./brajpath.db
```

This keeps local setup fast and requires no external database service.

### PostgreSQL

For PostgreSQL deployments, set:

```env
DATABASE_URL=postgresql://user:password@host:5432/brajpath
```

The app automatically converts this to the SQLAlchemy `pg8000` dialect internally.

## Twilio WhatsApp Setup

To connect the webhook to Twilio Sandbox:

1. Start the FastAPI server locally.
2. Expose it with a tunneling tool such as `ngrok`.
3. In the Twilio Console, open WhatsApp Sandbox settings.
4. Point the webhook to:

```text
https://<your-public-url>/whatsapp/webhook
```

5. Use HTTP `POST`.
6. Send a test message such as `hi` or `menu`.

In `development` mode, Twilio signature validation is skipped to make local testing easier.

## Deployment and Migration Docs

- Twilio production deployment guide: [docs/twilio-production-deployment.md](docs/twilio-production-deployment.md)
- Meta Cloud API migration guide: [docs/meta-cloud-api-migration.md](docs/meta-cloud-api-migration.md)

## Key Files

- [app/main.py](app/main.py): FastAPI application entry point
- [app/api/webhook.py](app/api/webhook.py): WhatsApp webhook handler
- [app/services/state_machine.py](app/services/state_machine.py): conversation flow controller
- [app/services/temple_service.py](app/services/temple_service.py): query and formatting logic
- [app/db/models.py](app/db/models.py): database models
- [app/db/seed.py](app/db/seed.py): seed data

## Product Direction

BrajPath is well suited for expansion into:

- a broader temple and route catalog
- richer multilingual translations
- verified local partner discovery
- festival-day overrides and operational notices
- analytics dashboards based on `query_logs`
- human escalation workflows for on-ground support

## Development Notes

- The project uses menu-driven state handling instead of free-form NLU.
- Startup creates missing tables automatically through SQLAlchemy metadata.
- Seed data is intentionally idempotent for repeated local setup.
- Current content should still be manually verified before any production launch involving live pilgrims.

## Disclaimer

Temple timings, access rules, and local fares can change without notice. The current data should be treated as operational guidance for development and testing, not as an authoritative live source.
