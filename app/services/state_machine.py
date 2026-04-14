"""
State Machine Service for BrajPath.
Manages conversation flows, state transitions, and user interaction logic.
Uses a Registry-based System Design for modularity and scalability.
"""
from __future__ import annotations

from typing import Callable

from sqlalchemy.orm import Session

from app.db.models import QueryLog, SupportRequest, UserSession
from app.services.context_service import ContextManager
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
    get_partner_categories_menu,
    get_partners_in_category,
    get_routes,
    get_timing_card,
    save_session,
    tr,
)

LANG_MAP: dict[str, str] = {"1": "en", "2": "hi", "3": "bn", "4": "ta"}
ENTRY_TRIGGERS: frozenset[str] = frozenset({"hi", "hello", "menu", "start", "radhe", "jai shree krishna", "hare krishna", "hare ram"})

# System Design: Handler Type for state transitions
HandlerType = Callable[[str, UserSession, ContextManager, str, str, Session], str]
HANDLER_REGISTRY: dict[str, HandlerType] = {}


def register_handler(state: str) -> Callable[[HandlerType], HandlerType]:
    def decorator(handler: HandlerType) -> HandlerType:
        HANDLER_REGISTRY[state] = handler
        return handler
    return decorator


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
    """Log query details for analytics and debugging.
    
    Args:
        db: SQLAlchemy session
        wa_number: User's WhatsApp number
        lang: Language code used
        incoming: Raw user input
        state: Current state machine state
        intent: Detected user intent
        entity: Detected entity/parameter
        status: Response status ('ok', 'error', etc)
    """
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


@register_handler("language_select")
def _handle_language_select(text: str, session: UserSession, ctx: ContextManager, wa_number: str, incoming: str, db: Session) -> str:
    current_lang = session.language_code
    if text in LANG_MAP:
        chosen = LANG_MAP[text]
        save_session(db, session, state="main_menu", lang=chosen)
        ctx.add_interaction("set_language")
        _log(db, wa_number, chosen, incoming, "language_select", "set_language", chosen)
        return _safe(_main_menu_reply(chosen))
    _log(db, wa_number, current_lang, incoming, "language_select", "invalid_input", text)
    return _safe(tr("welcome", current_lang))


@register_handler("main_menu")
def _handle_main_menu(text: str, session: UserSession, ctx: ContextManager, wa_number: str, incoming: str, db: Session) -> str:
    lang = session.language_code

    if text == "1":
        save_session(db, session, state="main_menu")
        ctx.add_interaction("open_now")
        _log(db, wa_number, lang, incoming, "main_menu", "open_now")
        open_list = get_open_temples(db)
        if open_list:
            return _safe("Currently open temples:\n\n" + "\n".join(f"- {name}" for name in open_list))
        return _safe("No temples appear to be open right now. Timings may vary, so please verify locally.")

    if text == "2":
        save_session(db, session, state="temple_area_select", pending_action="timing")
        ctx.add_interaction("timing_select")
        _log(db, wa_number, lang, incoming, "main_menu", "timing_select")
        return _safe(get_area_menu(lang))

    if text == "3":
        save_session(db, session, state="temple_area_select", pending_action="route")
        ctx.add_interaction("route_select")
        _log(db, wa_number, lang, incoming, "main_menu", "route_select")
        return _safe(get_area_menu(lang))

    if text == "4":
        save_session(db, session, state="main_menu")
        ctx.add_interaction("fair_price")
        _log(db, wa_number, lang, incoming, "main_menu", "fair_price")
        return _safe(get_fair_price_card(lang))

    if text == "5":
        save_session(db, session, state="partner_category_select")
        ctx.add_interaction("partner_browse")
        _log(db, wa_number, lang, incoming, "main_menu", "partner_browse")
        return _safe(get_partner_categories_menu(db, lang))

    if text == "6":
        save_session(db, session, state="temple_area_select", pending_action="advisory")
        ctx.add_interaction("advisory_select")
        _log(db, wa_number, lang, incoming, "main_menu", "advisory_select")
        return _safe(get_area_menu(lang))

    if text == "7":
        save_session(db, session, state="language_select")
        ctx.add_interaction("change_language")
        _log(db, wa_number, lang, incoming, "main_menu", "change_language")
        return _safe(tr("welcome", lang))

    if text == "0":
        save_session(db, session, state="main_menu")
        _log(db, wa_number, lang, incoming, "main_menu", "resend_menu")
        return _safe(_main_menu_reply(lang))

    save_session(db, session, state="main_menu")
    _log(db, wa_number, lang, incoming, "main_menu", "not_understood", text)
    return _safe(tr("not_understood", lang) + "\n\n" + _main_menu_reply(lang))


@register_handler("temple_area_select")
def _handle_temple_area_select(text: str, session: UserSession, ctx: ContextManager, wa_number: str, incoming: str, db: Session) -> str:
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
        
        # Context Engineering: Update last visited area
        ctx.update_visited_area(area)
        
        save_session(db, session, state="area_temple_select", selected_area=area, pending_action=action)
        _log(db, wa_number, lang, incoming, "temple_area_select", "select_area", area)
        return _safe(get_area_temple_menu(area, lang))

    _log(db, wa_number, lang, incoming, "temple_area_select", "not_understood", text)
    
    # Context Engineering: Suggest based on context if input not understood
    suggestion = ""
    suggested_area = ctx.get_suggested_area()
    if suggested_area:
        # Simple suggestion if they've been here before
        suggestion = f"\n\n(Tip: You previously looked at {suggested_area.title()})"
        
    return _safe(tr("not_understood", lang) + "\n\n" + get_area_menu(lang) + suggestion)


@register_handler("area_temple_select")
def _handle_area_temple_select(text: str, session: UserSession, ctx: ContextManager, wa_number: str, incoming: str, db: Session) -> str:
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
    
    # Context Engineering: Update last visited temple
    ctx.update_visited_temple(temple_code)
    
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


@register_handler("route_from_select")
def _handle_route_from_select(text: str, session: UserSession, ctx: ContextManager, wa_number: str, incoming: str, db: Session) -> str:
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


@register_handler("partner_category_select")
def _handle_partner_category_select(text: str, session: UserSession, ctx: ContextManager, wa_number: str, incoming: str, db: Session) -> str:
    """User selects a partner category - fetches and displays partners."""
    from app.db.models import PartnerCategory
    from sqlalchemy import select
    
    lang = session.language_code
    
    # Handle back to main menu
    if text == "0":
        save_session(db, session, state="main_menu")
        _log(db, wa_number, lang, incoming, "partner_category_select", "back")
        return _safe(_main_menu_reply(lang))
    
    # Get category list to map selection to ID
    categories = db.execute(
        select(PartnerCategory)
        .order_by(PartnerCategory.priority_order)
    ).scalars().all()
    
    if not categories or not text.isdigit():
        _log(db, wa_number, lang, incoming, "partner_category_select", "invalid_category", text)
        return _safe(tr("not_understood", lang))
    
    idx = int(text) - 1
    if idx < 0 or idx >= len(categories):
        _log(db, wa_number, lang, incoming, "partner_category_select", "invalid_category", text)
        return _safe(tr("not_understood", lang))
    
    selected_category = categories[idx]
    save_session(db, session, state="partner_list", pending_action=f"cat_{selected_category.id}")
    ctx.add_interaction("partner_category_select")
    _log(db, wa_number, lang, incoming, "partner_category_select", "view_partners", selected_category.code)
    
    return _safe(get_partners_in_category(db, selected_category.id, lang))


@register_handler("partner_list")
def _handle_partner_list(text: str, session: UserSession, ctx: ContextManager, wa_number: str, incoming: str, db: Session) -> str:
    """Handle partner list interactions - back to categories or main menu."""
    lang = session.language_code
    
    if text == "0":
        save_session(db, session, state="partner_category_select", pending_action=None)
        _log(db, wa_number, lang, incoming, "partner_list", "back")
        return _safe(get_partner_categories_menu(db, lang))
    
    # Other options (like contacting partner) not yet implemented
    _log(db, wa_number, lang, incoming, "partner_list", "invalid_action", text)
    save_session(db, session, state="main_menu")
    return _safe(_main_menu_reply(lang))


def _handle_help(session: UserSession, ctx: ContextManager, wa_number: str, incoming: str, db: Session) -> str:
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
    # Validate language code is supported, default to 'en' if invalid
    supported_langs = set(LANG_MAP.values())
    lang = session.language_code if session.language_code in supported_langs else "en"
    if lang != session.language_code:
        session.language_code = lang
    text = incoming.strip().lower()

    # System Design: Initialize Context Manager
    ctx = ContextManager(session)

    if text in ENTRY_TRIGGERS:
        save_session(db, session, state="main_menu")
        ctx.add_interaction("entry_trigger")
        _log(db, wa_number, lang, incoming, "any", "entry_trigger")
        return _safe(_main_menu_reply(lang))

    if text == "help":
        ctx.add_interaction("help")
        return _handle_help(session, ctx, wa_number, incoming, db)

    # System Design: Use Registry-based Dispatch
    state = session.current_state
    handler = HANDLER_REGISTRY.get(state)
    
    if handler:
        return handler(text, session, ctx, wa_number, incoming, db)

    # Fallback for unknown states
    save_session(db, session, state="main_menu")
    _log(db, wa_number, lang, incoming, state, "unknown_state", status="error")
    return _safe(_main_menu_reply(lang))
