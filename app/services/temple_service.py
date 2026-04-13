# app/services/temple_service.py 
from __future__ import annotations 
 
import json 
from datetime import datetime 
from pathlib import Path 
from typing import Optional 
 
import pytz 
from sqlalchemy import select 
from sqlalchemy.orm import Session 
 
from app.db.models import ( 
    FestivalOverride, 
    Route, 
    RoutePoint, 
    Schedule, 
    Temple, 
    TempleAdvisory, 
    UserSession, 
) 
 
# ── canonical lookup maps ───────────────────────────────────────────────────── 
 
AREA_MAP: dict[str, str] = { 
    "1": "vrindavan", 
    "2": "mathura", 
    "3": "govardhan", 
    "4": "outstation", 
} 
 
AREA_TEMPLE_MAP: dict[str, dict[str, str]] = { 
    "vrindavan": { 
        "1":  "banke_bihari", 
        "2":  "prem_mandir", 
        "3":  "iskcon_vrindavan", 
        "4":  "radha_raman", 
        "5":  "radha_vallabh", 
        "6":  "nidhivan", 
        "7":  "govind_dev_ji", 
        "8":  "madan_mohan", 
        "9":  "radha_damodar", 
        "10": "gopinath_temple", 
        "11": "radha_shyamasundar", 
        "12": "rangji_temple", 
        "13": "kesi_ghat", 
        "14": "jaipur_temple", 
        "15": "vrinda_devi_temple", 
        "16": "pagal_baba_mandir", 
        "17": "katyayani_shaktipeeth", 
    }, 
    "mathura": { 
        "1": "dwarkadhish", 
        "2": "krishna_janmabhoomi", 
        "3": "akrur_ghat", 
        "4": "potara_kund", 
        "5": "gita_mandir_mathura", 
    }, 
    "govardhan": { 
        "1": "radha_kund", 
        "2": "govardhan_hill", 
        "3": "kusum_sarovar", 
    }, 
    "outstation": { 
        "1": "nandgaon", 
        "2": "barsana", 
        "3": "gokul", 
    }, 
} 
 
# Flat TEMPLE_MAP for legacy compatibility (number keys may overlap across areas; 
# used only where a globally unique lookup is needed) 
TEMPLE_MAP: dict[str, str] = { 
    code: temple_code 
    for area_dict in AREA_TEMPLE_MAP.values() 
    for code, temple_code in area_dict.items() 
} 
 
FROM_MAP: dict[str, str] = { 
    "1": "mathura_junction", 
    "2": "mathura_new_bus_stand", 
    "3": "vishram_ghat", 
    "4": "vrindavan_gate", 
} 
 
IST = pytz.timezone("Asia/Kolkata") 
 
# ── translations loader ─────────────────────────────────────────────────────── 
 
_TRANSLATIONS: dict[str, dict[str, str]] = {} 
 
 
 def _load_translations() -> dict[str, dict[str, str]]: 
    global _TRANSLATIONS 
    if not _TRANSLATIONS: 
        path = Path(__file__).parent.parent / "data" / "translations.json" 
        with path.open(encoding="utf-8") as f: 
            _TRANSLATIONS = json.load(f) 
    return _TRANSLATIONS 
 
 
def tr(key: str, lang: str) -> str: 
    """Return translated string; falls back to English if key/lang missing.""" 
    data = _load_translations() 
    return data.get(key, {}).get(lang) or data.get(key, {}).get("en", f"[{key}]") 
 
 
# ── season logic ────────────────────────────────────────────────────────────── 
 
def _current_season(now_ist: datetime) -> str: 
    m = now_ist.month 
    if m in (11, 12, 1, 2): 
         return "winter" 
    if m in (7, 8, 9, 10): 
         return "monsoon" 
    return "summer" 
 
 
# ── open/closed logic ───────────────────────────────────────────────────────── 
 
def _is_open(schedule: Schedule | FestivalOverride, now_ist: datetime) -> bool: 
    t = now_ist.time() 
    morning_open = ( 
        schedule.open_morning is not None 
        and schedule.close_morning is not None 
        and schedule.open_morning <= t <= schedule.close_morning 
    ) 
    evening_open = ( 
        schedule.open_evening is not None 
        and schedule.close_evening is not None 
        and schedule.open_evening <= t <= schedule.close_evening 
    ) 
    bhog_closed = False 
    if ( 
        hasattr(schedule, "bhog_start") 
        and schedule.bhog_start is not None 
        and schedule.bhog_end is not None 
    ): 
        bhog_closed = schedule.bhog_start <= t <= schedule.bhog_end 
    return (morning_open or evening_open) and not bhog_closed 
 
 
def _fmt_time(t: object) -> str: 
    if t is None: 
        return "—" 
    return datetime.strptime(str(t), "%H:%M:%S").strftime("%I:%M %p").lstrip("0") 
 
 
# ── session helpers ─────────────────────────────────────────────────────────── 
 
def get_or_create_session(db: Session, wa_number: str) -> UserSession: 
    session = db.execute( 
        select(UserSession).where(UserSession.wa_number == wa_number) 
    ).scalar_one_or_none() 
    if session is None: 
        session = UserSession( 
            wa_number=wa_number, 
            language_code="en", 
            current_state="language_select", 
            message_count=0, 
        ) 
        db.add(session) 
        db.flush() 
    return session 
 
 
def save_session( 
    db: Session, 
    session: UserSession, 
    *, 
    state: Optional[str] = None, 
    lang: Optional[str] = None, 
    selected_temple: Optional[str] = None, 
    selected_route_from: Optional[str] = None, 
    pending_action: Optional[str] = None, 
    selected_area: Optional[str] = None, 
) -> None: 
    now = datetime.now(IST).replace(tzinfo=None) 
    if state is not None: 
        session.prev_state = session.current_state 
        session.current_state = state 
    if lang is not None: 
        session.language_code = lang 
    if selected_temple is not None: 
        session.selected_temple = selected_temple 
    if selected_route_from is not None: 
        session.selected_route_from = selected_route_from 
    if pending_action is not None: 
        session.pending_action = pending_action 
    if selected_area is not None: 
        session.selected_area = selected_area 
    session.message_count = (session.message_count or 0) + 1 
    session.last_seen_at = now 
    session.updated_at = now 
    db.flush() 
 
 
# ── schedule fetcher ────────────────────────────────────────────────────────── 
 
def _get_active_schedule( 
    db: Session, temple_id: int, now_ist: datetime 
) -> Schedule | FestivalOverride | None: 
    today = now_ist.date() 
 
    override = db.execute( 
        select(FestivalOverride).where( 
            FestivalOverride.temple_id == temple_id, 
            FestivalOverride.date_from <= today, 
            FestivalOverride.date_to >= today, 
            FestivalOverride.is_active.is_(True), 
        ) 
    ).scalar_one_or_none() 
    if override: 
        return override 
 
    season = _current_season(now_ist) 
    sched = db.execute( 
        select(Schedule).where( 
            Schedule.temple_id == temple_id, 
            Schedule.season == season, 
            Schedule.is_current.is_(True), 
        ) 
    ).scalar_one_or_none() 
    if sched: 
        return sched 
 
    return db.execute( 
        select(Schedule).where( 
            Schedule.temple_id == temple_id, 
            Schedule.season == "general", 
            Schedule.is_current.is_(True), 
        ) 
    ).scalar_one_or_none() 
 
 
# ── advisory emoji map ──────────────────────────────────────────────────────── 
 
ADVISORY_EMOJI: dict[str, str] = { 
    "crowd":       "👥", 
    "mobile":      "📵", 
    "footwear":    "👟", 
    "parking":     "🅿️", 
    "elderly":     "♿", 
    "dress_code":  "👕", 
    "photography": "📷", 
    "donation":    "🪙", 
} 
 
_MSG_FIELD  = {"en": "message_en", "hi": "message_hi", "bn": "message_bn", "ta": "message_ta"} 
_NOTE_FIELD = {"en": "notes_en",   "hi": "notes_hi"} 
 
 
# ── public service functions ────────────────────────────────────────────────── 
 
def get_open_temples(db: Session) -> list[str]: 
    """Return list of temple name_en strings currently open.""" 
    now_ist = datetime.now(IST) 
    temples = db.execute( 
        select(Temple).where(Temple.is_active.is_(True)) 
    ).scalars().all() 
    open_names: list[str] = [] 
    for temple in temples: 
        sched = _get_active_schedule(db, temple.id, now_ist) 
        if sched and _is_open(sched, now_ist): 
            open_names.append(temple.name_en) 
    return open_names 
 
 
def get_timing_card(db: Session, temple_code: str, lang: str) -> str: 
    """Return formatted timing card for the given temple and language.""" 
    now_ist = datetime.now(IST) 
    temple = db.execute( 
        select(Temple).where(Temple.code == temple_code) 
    ).scalar_one_or_none() 
    if not temple: 
        return tr("not_understood", lang) 
 
    name_field  = f"name_{lang}" if lang in ("en", "hi", "bn", "ta") else "name_en" 
    temple_name = getattr(temple, name_field, temple.name_en) 
 
    sched = _get_active_schedule(db, temple.id, now_ist) 
    if not sched: 
        return f"🏛️ *{temple_name}*\n⚠️ Timing information not available. Verify on arrival." 
 
    is_festival = isinstance(sched, FestivalOverride) 
    status = "🟢 Open" if _is_open(sched, now_ist) else "🔴 Closed" 
 
    lines: list[str] = [ 
        f"🏛️ *{temple_name}*", 
        f"Status: {status}", 
        f"🌅 Morning: {_fmt_time(sched.open_morning)} – {_fmt_time(sched.close_morning)}", 
    ] 
 
    bhog_start = getattr(sched, "bhog_start", None) 
    bhog_end   = getattr(sched, "bhog_end",   None) 
    if bhog_start and bhog_end: 
        lines.append(f"🍽 Bhog (closed): {_fmt_time(bhog_start)} – {_fmt_time(bhog_end)}") 
 
    lines.append(f"🌆 Evening: {_fmt_time(sched.open_evening)} – {_fmt_time(sched.close_evening)}") 
 
    if is_festival: 
        lines.append(f"📌 Source: Festival override — {sched.festival_name}") 
        special = getattr(sched, f"special_note_{lang}", None) or getattr(sched, "special_note_en", None) 
        if special: 
            lines.append(f"🎉 {special}") 
    else: 
        verified = getattr(sched, "verified_by", None) 
        if verified: 
            lines.append(f"📌 Source: {verified}") 
        note_key = _NOTE_FIELD.get(lang, "notes_en") 
        note = getattr(sched, note_key, None) or getattr(sched, "notes_en", None) 
        if note: 
            lines.append(f"💡 {note}") 
 
    lines.append("⚠️ Festival days may change timings. Verify on arrival.") 
    return "\n".join(lines) 
 
 
def get_routes(db: Session, from_code: str, temple_code: str, lang: str) -> str: 
    """Return formatted route card from origin to temple.""" 
    from_point = db.execute( 
        select(RoutePoint).where(RoutePoint.code == from_code) 
    ).scalar_one_or_none() 
    temple = db.execute( 
        select(Temple).where(Temple.code == temple_code) 
    ).scalar_one_or_none() 
    if not from_point or not temple: 
        return tr("not_understood", lang) 
 
    name_field  = f"name_{lang}" if lang in ("en", "hi", "bn", "ta") else "name_en" 
    from_name   = getattr(from_point, name_field, from_point.name_en) 
    temple_name = getattr(temple,     name_field, temple.name_en) 
 
    routes = db.execute( 
        select(Route).where( 
            Route.from_point_id == from_point.id, 
            Route.temple_id == temple.id, 
            Route.is_active.is_(True), 
        ) 
    ).scalars().all() 
 
    if not routes: 
        return f"🗺️ No route found from {from_name} to {temple_name}. Type *help* for assistance." 
 
    rt_field = f"route_text_{lang}" if lang in ("en", "hi", "bn", "ta") else "route_text_en" 
 
    lines: list[str] = [f"🗺️ *{from_name} → {temple_name}*\n"] 
    for r in routes: 
        mode_label = r.mode.replace("_", " ").title() 
        fare = ( 
            f"₹{r.fare_min}–{r.fare_max}" 
            if r.fare_min is not None and r.fare_max is not None and r.fare_max > 0 
            else "Free / walk" 
        ) 
        rt_text = getattr(r, rt_field, None) or r.route_text_en 
        lines.append(f"🚦 *{mode_label}* · ~{r.duration_min_est} min · {fare}") 
        lines.append(rt_text) 
        if r.last_mile_note: 
            lines.append(f"📍 {r.last_mile_note}") 
        lines.append("") 
 
    lines.append("💰 Fares are community-reported typical ranges. Agree price before boarding.") 
    return "\n".join(lines).strip() 
 
 
def get_advisories(db: Session, temple_code: str, lang: str) -> str: 
    """Return formatted advisory card for the given temple.""" 
    temple = db.execute( 
        select(Temple).where(Temple.code == temple_code) 
    ).scalar_one_or_none() 
    if not temple: 
        return tr("not_understood", lang) 
 
    name_field  = f"name_{lang}" if lang in ("en", "hi", "bn", "ta") else "name_en" 
    temple_name = getattr(temple, name_field, temple.name_en) 
 
    advisories = db.execute( 
        select(TempleAdvisory) 
        .where( 
            TempleAdvisory.temple_id == temple.id, 
            TempleAdvisory.is_active.is_(True), 
        )
    ).scalars().all()

    if not advisories:
        return f"ℹ️ No specific advisories for *{temple_name}* at this time."

    lines: list[str] = [f"ℹ️ *Advisories for {temple_name}*\n"]
    for adv in advisories:
        emoji = ADVISORY_EMOJI.get(adv.advisory_type, "📌")
        msg_key = _MSG_FIELD.get(lang, "message_en")
        msg = getattr(adv, msg_key, None) or adv.message_en
        lines.append(f"{emoji} {msg}")

    return "\n".join(lines)


def get_area_menu(lang: str) -> str:
    """Return the translated area selection menu."""
    return tr("select_area", lang)


def get_area_temple_menu(area_code: str, lang: str) -> str:
    """Return the translated temple selection menu for a given area."""
    # This implementation builds a list of temples from AREA_TEMPLE_MAP
    # You might want to fetch names from DB for a better experience, 
    # but for now we follow the structure of translations.json
    return tr("select_temple", lang)


def get_fair_price_card(lang: str) -> str:
    """Return the community fare guide card."""
    return tr("fair_price_menu", lang)
