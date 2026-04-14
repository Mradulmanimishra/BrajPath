from __future__ import annotations

from sqlalchemy.orm import Session

from app.services.state_machine import process_message


def _play(db: Session, wa_number: str, messages: list[str]) -> str:
    reply = ""
    for message in messages:
        reply = process_message(wa_number, message, db)
        db.commit()
    return reply


def test_timing_flow_returns_timing_card(db_session: Session) -> None:
    reply = _play(db_session, "+910000000001", ["1", "2", "1", "1"])

    assert "*Shri Banke Bihari Mandir*" in reply
    assert "Morning:" in reply
    assert "Evening:" in reply


def test_route_flow_returns_route_card(db_session: Session) -> None:
    reply = _play(db_session, "+910000000002", ["1", "3", "1", "1", "1"])

    assert "*Mathura Junction Railway Station → Shri Banke Bihari Mandir*" in reply
    assert "E Rickshaw" in reply
    assert "Fares are community-reported typical ranges" in reply


def test_advisory_flow_returns_advisories(db_session: Session) -> None:
    reply = _play(db_session, "+910000000003", ["1", "6", "1", "1"])

    assert "*Advisories for Shri Banke Bihari Mandir*" in reply
    assert "Expect heavy crowds in the evening" in reply
    assert "Mobile phones may be restricted inside" in reply
