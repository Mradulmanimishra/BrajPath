from __future__ import annotations

from sqlalchemy.orm import Session

from app.db.models import QueryLog, SupportRequest, UserSession
from app.services.temple_service import (
    AREA_MAP,
    AREA_TEMPLE_MAP,
    FROM_MAP,
    get_advisories,
    get_area_menu,
    get_area_temple_menu,
    get_fair_price_card,
    get_open_temples,
    get_or_create_session,
    get_routes,
    get_timing_card,
    save_session,
    tr,
)

LANG_MAP: dict[str, str] = {"1": "en", "2": "hi", "3": "bn", "4": "ta"}
ENTRY_TRIGGERS: frozenset[str] = frozenset({"hi", "hello", "menu", "start", "radhe", "jai shree krishna", "hare krishna", "hare ram"})


def _log(
    db: Session,
    wa_number: str,
    lang: str,
    incoming: str,
    state: str,
    intent: str,
    entity: str = "",
    status: str = "ok",
) -> None:
    db.add(
        QueryLog(
            wa_number=wa_number,
            language_code=lang,
            incoming_text=incoming,
            detected_state=state,
            detected_intent=intent,
            detected_entity=entity,
            response_status=status,
        )
    )


def _safe(text: str, max_len: int = 1600) -> str:
    return text[:max_len] if len(text) > max_len else text


def _main_menu_reply(lang: str) -> str:
    return tr("main_menu", lang)


def _handle_language_select(text: str, session: UserSession, wa_number: str, incoming: str, db: Session) -> str:
    current_lang = session.language_code
    if text in LANG_MAP:
        chosen = LANG_MAP[text]
        save_session(db, session, state="main_menu", lang=chosen)
        _log(db, wa_number, chosen, incoming, "language_select", "set_language", chosen)
        return _safe(_main_menu_reply(chosen))
    _log(db, wa_number, current_lang, incoming, "language_select", "invalid_input", text)
    return _safe(tr("welcome", current_lang))


def _handle_main_menu(text: str, session: UserSession, wa_number: str, incoming: str, db: Session) -> str:
    lang = session.language_code

    if text == "1":
        save_session(db, session, state="main_menu")
        _log(db, wa_number, lang, incoming, "main_menu", "open_now")
        open_list = get_open_temples(db)
        if open_list:
            return _safe("Currently open temples:\n\n" + "\n".join(f"- {name}" for name in open_list))
        return _safe("No temples appear to be open right now. Timings may vary, so please verify locally.")

    if text == "2":
        save_session(db, session, state="temple_area_select", pending_action="timing")
        _log(db, wa_number, lang, incoming, "main_menu", "timing_select")
        return _safe(get_area_menu(lang))

    if text == "3":
        save_session(db, session, state="temple_area_select", pending_action="route")
        _log(db, wa_number, lang, incoming, "main_menu", "route_select")
        return _safe(get_area_menu(lang))

    if text == "4":
        save_session(db, session, state="main_menu")
        _log(db, wa_number, lang, incoming, "main_menu", "fair_price")
        return _safe(get_fair_price_card(lang))

    if text == "5":
        save_session(db, session, state="partner_browse")
        _log(db, wa_number, lang, incoming, "main_menu", "partner_browse")
        return _safe(tr("help_escalation", lang))

    if text == "6":
        save_session(db, session, state="temple_area_select", pending_action="advisory")
        _log(db, wa_number, lang, incoming, "main_menu", "advisory_select")
        return _safe(get_area_menu(lang))

    if text == "7":
        save_session(db, session, state="language_select")
        _log(db, wa_number, lang, incoming, "main_menu", "change_language")
        return _safe(tr("welcome", lang))

    if text == "0":
        save_session(db, session, state="main_menu")
        _log(db, wa_number, lang, incoming, "main_menu", "resend_menu")
        return _safe(_main_menu_reply(lang))

    save_session(db, session, state="main_menu")
    _log(db, wa_number, lang, incoming, "main_menu", "not_understood", text)
    return _safe(tr("not_understood", lang) + "\n\n" + _main_menu_reply(lang))


def _handle_temple_area_select(text: str, session: UserSession, wa_number: str, incoming: str, db: Session) -> str:
    lang = session.language_code
    action = session.pending_action or "timing"

    if text == "0":
        save_session(db, session, state="main_menu")
        _log(db, wa_number, lang, incoming, "temple_area_select", "back")
        return _safe(_main_menu_reply(lang))

    if text in AREA_MAP:
        area = AREA_MAP[text]
        if not AREA_TEMPLE_MAP.get(area):
            _log(db, wa_number, lang, incoming, "temple_area_select", "area_not_available", area)
            save_session(db, session, state="temple_area_select")
            return _safe(tr("area_not_available", lang) + "\n\n" + get_area_menu(lang))
        save_session(db, session, state="area_temple_select", selected_area=area, pending_action=action)
        _log(db, wa_number, lang, incoming, "temple_area_select", "select_area", area)
        return _safe(get_area_temple_menu(area, lang))

    _log(db, wa_number, lang, incoming, "temple_area_select", "not_understood", text)
    return _safe(tr("not_understood", lang) + "\n\n" + get_area_menu(lang))


def _handle_area_temple_select(text: str, session: UserSession, wa_number: str, incoming: str, db: Session) -> str:
    lang = session.language_code
    area = session.selected_area or "vrindavan"
    action = session.pending_action or "timing"
    area_map = AREA_TEMPLE_MAP.get(area, {})

    if text == "0":
        save_session(db, session, state="temple_area_select")
        _log(db, wa_number, lang, incoming, "area_temple_select", "back")
        return _safe(get_area_menu(lang))

    if text not in area_map:
        _log(db, wa_number, lang, incoming, "area_temple_select", "not_understood", text)
        return _safe(tr("not_understood", lang) + "\n\n" + get_area_temple_menu(area, lang))

    temple_code = area_map[text]
    if action == "timing":
        save_session(db, session, state="main_menu", selected_temple=temple_code)
        _log(db, wa_number, lang, incoming, "area_temple_select", "get_timing", temple_code)
        return _safe(get_timing_card(db, temple_code, lang))

    if action == "route":
        save_session(db, session, state="route_from_select", selected_temple=temple_code)
        _log(db, wa_number, lang, incoming, "area_temple_select", "get_route_menu", temple_code)
        return _safe(tr("select_from_point", lang))

    save_session(db, session, state="main_menu", selected_temple=temple_code)
    _log(db, wa_number, lang, incoming, "area_temple_select", "get_advisory", temple_code)
    return _safe(get_advisories(db, temple_code, lang))


def _handle_route_from_select(text: str, session: UserSession, wa_number: str, incoming: str, db: Session) -> str:
    lang = session.language_code
    temple_code = session.selected_temple or ""

    if text == "0":
        save_session(db, session, state="temple_area_select", pending_action="route")
        _log(db, wa_number, lang, incoming, "route_from_select", "back")
        return _safe(get_area_menu(lang))

    if text not in FROM_MAP:
        _log(db, wa_number, lang, incoming, "route_from_select", "not_understood", text)
        return _safe(tr("not_understood", lang) + "\n\n" + tr("select_from_point", lang))

    from_code = FROM_MAP[text]
    save_session(db, session, state="main_menu", selected_route_from=from_code)
    _log(db, wa_number, lang, incoming, "route_from_select", "get_route", f"{from_code}->{temple_code}")
    return _safe(get_routes(db, from_code, temple_code, lang))


def _handle_partner_browse(text: str, session: UserSession, wa_number: str, incoming: str, db: Session) -> str:
    lang = session.language_code
    save_session(db, session, state="main_menu")
    if text == "0":
        _log(db, wa_number, lang, incoming, "partner_browse", "back")
        return _safe(_main_menu_reply(lang))
    _log(db, wa_number, lang, incoming, "partner_browse", "no_partners")
    return _safe(tr("help_escalation", lang))


def _handle_help(session: UserSession, wa_number: str, incoming: str, db: Session) -> str:
    lang = session.language_code
    db.add(
        SupportRequest(
            wa_number=wa_number,
            language_code=lang,
            request_type="help_keyword",
            message_text=incoming,
            status="open",
        )
    )
    save_session(db, session, state="main_menu")
    _log(db, wa_number, lang, incoming, session.current_state, "help_escalation")
    return _safe(tr("help_escalation", lang))


def process_message(wa_number: str, incoming: str, db: Session) -> str:
    session = get_or_create_session(db, wa_number)
    lang = session.language_code
    text = incoming.strip().lower()

    if text in ENTRY_TRIGGERS:
        save_session(db, session, state="main_menu")
        _log(db, wa_number, lang, incoming, "any", "entry_trigger")
        return _safe(_main_menu_reply(lang))

    if text == "help":
        return _handle_help(session, wa_number, incoming, db)

    state = session.current_state
    if state == "language_select":
        return _handle_language_select(text, session, wa_number, incoming, db)
    if state == "main_menu":
        return _handle_main_menu(text, session, wa_number, incoming, db)
    if state == "temple_area_select":
        return _handle_temple_area_select(text, session, wa_number, incoming, db)
    if state == "area_temple_select":
        return _handle_area_temple_select(text, session, wa_number, incoming, db)
    if state == "route_from_select":
        return _handle_route_from_select(text, session, wa_number, incoming, db)
    if state == "partner_browse":
        return _handle_partner_browse(text, session, wa_number, incoming, db)

    save_session(db, session, state="main_menu")
    _log(db, wa_number, lang, incoming, state, "unknown_state", status="error")
    return _safe(_main_menu_reply(lang))
