from __future__ import annotations

from datetime import time

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import PartnerCategory, Route, RoutePoint, Schedule, Temple, TempleAdvisory
from app.db.session import SessionLocal


def _t(hour: int, minute: int) -> time:
    return time(hour, minute)


def _get_temple(db: Session, code: str) -> Temple | None:
    return db.execute(select(Temple).where(Temple.code == code)).scalar_one_or_none()


def _get_route_point(db: Session, code: str) -> RoutePoint:
    route_point = db.execute(select(RoutePoint).where(RoutePoint.code == code)).scalar_one_or_none()
    if route_point is None:
        raise RuntimeError(f"Route point '{code}' is missing.")
    return route_point


def seed_route_points(db: Session) -> None:
    rows = [
        RoutePoint(code="mathura_junction", name_en="Mathura Junction Railway Station", name_hi="Mathura Junction Railway Station", name_bn="Mathura Junction Railway Station", name_ta="Mathura Junction Railway Station", city="Mathura", area="Mathura", point_type="railway_station", latitude=27.4945, longitude=77.6731),
        RoutePoint(code="mathura_new_bus_stand", name_en="Mathura New Bus Stand (Masani)", name_hi="Mathura New Bus Stand (Masani)", name_bn="Mathura New Bus Stand (Masani)", name_ta="Mathura New Bus Stand (Masani)", city="Mathura", area="Mathura", point_type="bus_stand", latitude=27.5080, longitude=77.6550),
        RoutePoint(code="vishram_ghat", name_en="Vishram Ghat", name_hi="Vishram Ghat", name_bn="Vishram Ghat", name_ta="Vishram Ghat", city="Mathura", area="Mathura", point_type="ghat", latitude=27.5014, longitude=77.6697),
        RoutePoint(code="vrindavan_gate", name_en="Vrindavan Gate", name_hi="Vrindavan Gate", name_bn="Vrindavan Gate", name_ta="Vrindavan Gate", city="Vrindavan", area="Vrindavan", point_type="temple_gate", latitude=27.5610, longitude=77.6980),
    ]
    for row in rows:
        if db.execute(select(RoutePoint).where(RoutePoint.code == row.code)).scalar_one_or_none() is None:
            db.add(row)
    db.flush()


def seed_partner_categories(db: Session) -> None:
    rows = [
        PartnerCategory(code="stay_near_temple", slug="stay-near-temple", name="Stay Near Temple", name_en="Stay Near Temple"),
        PartnerCategory(code="local_guide", slug="local-guide", name="Local Guide", name_en="Local Guide"),
        PartnerCategory(code="transport", slug="transport", name="Transport", name_en="Transport"),
        PartnerCategory(code="prasad_shop", slug="prasad-shop", name="Prasad Shop", name_en="Prasad Shop"),
        PartnerCategory(code="puja_samagri", slug="puja-samagri", name="Puja Samagri", name_en="Puja Samagri"),
    ]
    for row in rows:
        if db.execute(select(PartnerCategory).where(PartnerCategory.code == row.code)).scalar_one_or_none() is None:
            db.add(row)
    db.flush()


def _seed_temple(
    db: Session,
    *,
    code: str,
    name_en: str,
    area: str,
    city: str,
    latitude: float,
    longitude: float,
    notes: str,
    schedules: list[Schedule],
    advisories: list[TempleAdvisory],
    routes: list[Route],
) -> None:
    if _get_temple(db, code) is not None:
        return

    temple = Temple(
        code=code,
        name_en=name_en,
        name_hi=name_en,
        name_bn=name_en,
        name_ta=name_en,
        area=area,
        city=city,
        latitude=latitude,
        longitude=longitude,
        notes=notes,
    )
    db.add(temple)
    db.flush()

    for schedule in schedules:
        schedule.temple_id = temple.id
        db.add(schedule)
    for advisory in advisories:
        advisory.temple_id = temple.id
        db.add(advisory)
    for route in routes:
        route.temple_id = temple.id
        db.add(route)
    db.flush()


def seed_banke_bihari(db: Session) -> None:
    mj = _get_route_point(db, "mathura_junction")
    vg = _get_route_point(db, "vrindavan_gate")
    _seed_temple(
        db,
        code="banke_bihari",
        name_en="Shri Banke Bihari Mandir",
        area="Vrindavan",
        city="Vrindavan",
        latitude=27.5739,
        longitude=77.6975,
        notes="Most visited temple in Vrindavan.",
        schedules=[
            Schedule(season="summer", open_morning=_t(7, 45), close_morning=_t(12, 0), bhog_start=_t(12, 0), bhog_end=_t(17, 30), open_evening=_t(17, 30), close_evening=_t(21, 30), is_current=True, verified_by="Community verification Apr 2026", notes_en="Very crowded in the evening.", notes_hi="Very crowded in the evening."),
            Schedule(season="winter", open_morning=_t(8, 45), close_morning=_t(13, 0), bhog_start=_t(13, 0), bhog_end=_t(16, 30), open_evening=_t(16, 30), close_evening=_t(21, 0), is_current=True, verified_by="Community verification Apr 2026", notes_en="Winter hours.", notes_hi="Winter hours."),
        ],
        advisories=[
            TempleAdvisory(advisory_type="crowd", priority=1, message_en="Expect heavy crowds in the evening."),
            TempleAdvisory(advisory_type="mobile", priority=2, message_en="Mobile phones may be restricted inside."),
            TempleAdvisory(advisory_type="footwear", priority=3, message_en="Remove footwear before entering."),
        ],
        routes=[
            Route(from_point_id=mj.id, mode="e_rickshaw", duration_min_est=25, fare_min=30, fare_max=40, fare_currency="INR", route_text_en="Take a shared e-rickshaw to Loi Bazaar and walk the last few minutes.", last_mile_note="Final approach is by foot through narrow lanes."),
            Route(from_point_id=vg.id, mode="e_rickshaw", duration_min_est=15, fare_min=30, fare_max=60, fare_currency="INR", route_text_en="Take an e-rickshaw to Loi Bazaar and walk to the temple.", last_mile_note="Walk the final stretch."),
        ],
    )


def seed_prem_mandir(db: Session) -> None:
    mj = _get_route_point(db, "mathura_junction")
    _seed_temple(
        db,
        code="prem_mandir",
        name_en="Prem Mandir",
        area="Raman Reti",
        city="Vrindavan",
        latitude=27.5664,
        longitude=77.6900,
        notes="Illuminated marble temple with evening light show.",
        schedules=[
            Schedule(season="general", open_morning=_t(5, 30), close_morning=_t(12, 0), open_evening=_t(16, 30), close_evening=_t(21, 0), is_current=True, verified_by="Community verification Apr 2026", notes_en="Arrive before sunset for a calmer visit.", notes_hi="Arrive before sunset for a calmer visit.")
        ],
        advisories=[TempleAdvisory(advisory_type="crowd", priority=1, message_en="Crowds increase before the evening light show.")],
        routes=[
            Route(from_point_id=mj.id, mode="e_rickshaw", duration_min_est=30, fare_min=30, fare_max=40, fare_currency="INR", route_text_en="Take a shared e-rickshaw toward Raman Reti and get down at Prem Mandir.", last_mile_note="Ask for the main gate.")
        ],
    )


def seed_iskcon_vrindavan(db: Session) -> None:
    mj = _get_route_point(db, "mathura_junction")
    _seed_temple(
        db,
        code="iskcon_vrindavan",
        name_en="ISKCON Sri Krishna Balaram Mandir",
        area="Raman Reti",
        city="Vrindavan",
        latitude=27.5672,
        longitude=77.6895,
        notes="Popular international temple in Raman Reti.",
        schedules=[
            Schedule(season="general", open_morning=_t(4, 30), close_morning=_t(13, 0), open_evening=_t(16, 0), close_evening=_t(21, 0), is_current=True, verified_by="Community verification Apr 2026", notes_en="Mangala Aarti begins early morning.", notes_hi="Mangala Aarti begins early morning.")
        ],
        advisories=[TempleAdvisory(advisory_type="dress_code", priority=1, message_en="Dress modestly for entry.")],
        routes=[
            Route(from_point_id=mj.id, mode="e_rickshaw", duration_min_est=30, fare_min=30, fare_max=40, fare_currency="INR", route_text_en="Take a shared e-rickshaw toward Raman Reti and ask for ISKCON temple.", last_mile_note="The temple is on the main Raman Reti road.")
        ],
    )


def run_all(db: Session) -> None:
    seed_route_points(db)
    seed_partner_categories(db)
    seed_banke_bihari(db)
    seed_prem_mandir(db)
    seed_iskcon_vrindavan(db)
    db.commit()


def run_seed() -> None:
    db: Session = SessionLocal()
    try:
        run_all(db)
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()
