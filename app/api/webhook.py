from __future__ import annotations

import logging
import time
from urllib.parse import urlsplit, urlunsplit

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session
from twilio.request_validator import RequestValidator
from twilio.twiml.messaging_response import MessagingResponse

from app.config import settings
from app.db.session import get_db
from app.services.state_machine import process_message

logger = logging.getLogger("brajpath.webhook")
router = APIRouter()


def _request_url_for_validation(request: Request) -> str:
    if not settings.PUBLIC_WEBHOOK_BASE_URL:
        return str(request.url)

    incoming = urlsplit(str(request.url))
    public_base = urlsplit(settings.PUBLIC_WEBHOOK_BASE_URL.rstrip("/"))
    return urlunsplit((public_base.scheme, public_base.netloc, incoming.path, incoming.query, ""))


async def validate_twilio_request(request: Request) -> None:
    if settings.APP_ENV == "development":
        return

    if not settings.TWILIO_AUTH_TOKEN:
        raise HTTPException(status_code=500, detail="TWILIO_AUTH_TOKEN is required in production")

    form = await request.form()
    validator = RequestValidator(settings.TWILIO_AUTH_TOKEN)
    signature = request.headers.get("X-Twilio-Signature", "")
    request_url = _request_url_for_validation(request)
    if not validator.validate(request_url, dict(form), signature):
        raise HTTPException(status_code=403, detail="Invalid Twilio signature")


@router.post("/whatsapp/webhook", response_class=PlainTextResponse)
async def whatsapp_webhook(
    request: Request,
    Body: str = Form(default=""),
    From: str = Form(default=""),
    db: Session = Depends(get_db),
) -> PlainTextResponse:
    await validate_twilio_request(request)
    started_at = time.perf_counter()

    wa_number = From.replace("whatsapp:", "").strip()
    incoming_text = Body.strip()
    logger.info("[WA] %s: %r", wa_number, incoming_text)

    if not wa_number or not incoming_text:
        return PlainTextResponse("", status_code=200)

    try:
        reply_text = process_message(wa_number, incoming_text, db)
        db.commit()
    except Exception:
        db.rollback()
        logger.exception("State machine error for %s", wa_number)
        reply_text = "Sorry, something went wrong. Please try again or type menu."

    elapsed_ms = int((time.perf_counter() - started_at) * 1000)
    logger.info("[WA] replied in %sms", elapsed_ms)

    twiml = MessagingResponse()
    twiml.message(reply_text)
    return PlainTextResponse(str(twiml), media_type="text/xml")
