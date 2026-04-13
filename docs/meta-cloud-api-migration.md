# BrajPath Twilio to Meta Cloud API Migration Guide

This document explains exactly what must change in this project to replace Twilio WhatsApp with Meta WhatsApp Cloud API.

## Current Twilio-specific parts

These files are Twilio-coupled today:

- `app/api/webhook.py`
- `app/config.py`
- `requirements.txt`
- `pyproject.toml`

The core business flow in these files can mostly stay:

- `app/services/state_machine.py`
- `app/services/temple_service.py`
- `app/db/models.py`

That means the conversation engine is reusable. The transport layer is what changes.

## What must change exactly

### 1. Inbound webhook format

Current Twilio flow:

- Twilio sends form-encoded fields like `From` and `Body`
- `app/api/webhook.py` reads them with `Form(...)`

Meta Cloud API flow:

- Meta sends JSON webhook payloads
- you must parse `entry -> changes -> value -> messages`

Required change:

- replace the current Twilio form handler with a Meta JSON webhook handler

### 2. Webhook verification

Current Twilio flow:

- validate the request with `X-Twilio-Signature`
- use `RequestValidator`

Meta Cloud API flow:

- add a GET verification route using `hub.mode`, `hub.verify_token`, and `hub.challenge`
- optionally validate `X-Hub-Signature-256`

Required change:

- remove Twilio request validation logic
- add Meta webhook verification logic

### 3. Outbound reply mechanism

Current Twilio flow:

- return TwiML from the webhook
- Twilio sends the WhatsApp reply for you

Meta Cloud API flow:

- your webhook returns `200 OK`
- your app must send outbound messages by calling Meta Graph API directly

Required change:

- replace `MessagingResponse()` and TwiML with an outbound HTTP client call

### 4. Configuration changes

Remove these as primary transport settings:

- `TWILIO_ACCOUNT_SID`
- `TWILIO_AUTH_TOKEN`
- `TWILIO_WHATSAPP_FROM`

Add these:

- `META_VERIFY_TOKEN`
- `META_APP_SECRET`
- `META_ACCESS_TOKEN`
- `META_PHONE_NUMBER_ID`
- `META_BUSINESS_ACCOUNT_ID` if needed for operations

### 5. Dependency changes

Current dependency:

- `twilio`

Migration:

- remove `twilio`
- add an HTTP client such as `httpx`

### 6. File-level code changes

`app/api/webhook.py`
- replace Twilio form fields with Meta JSON payload parsing
- add GET verification endpoint
- keep calling `process_message(...)` after extracting sender text
- send the reply through Meta Graph API instead of returning TwiML

`app/config.py`
- replace Twilio env vars with Meta env vars

`requirements.txt` and `pyproject.toml`
- remove `twilio`
- add `httpx`

## What does not need to change

- temple database tables
- seed data
- schedule logic
- advisory logic
- route logic
- state machine flow itself

## Recommended migration structure

If you want a clean migration, create a transport adapter layer:

- `app/channels/base.py`
- `app/channels/twilio.py`
- `app/channels/meta_whatsapp.py`

Then keep `state_machine.py` unchanged and swap only the channel integration.

## Official references

- Meta Cloud API overview: https://meta-preview.mintlify.io/docs/whatsapp/cloud-api/overview
- Meta Cloud API Postman collection: https://www.postman.com/meta/whatsapp-business-platform/documentation/wlk6lh4/whatsapp-cloud-api
