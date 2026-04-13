from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, Numeric, String, Text, Time
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


def _utcnow() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


class Temple(Base):
    __tablename__ = "temples"

    id = Column(Integer, primary_key=True)
    code = Column(String(60), unique=True, nullable=False)
    name_en = Column(String(200), nullable=False)
    name_hi = Column(String(200))
    name_bn = Column(String(200))
    name_ta = Column(String(200))
    area = Column(String(120))
    city = Column(String(80), default="Vrindavan")
    latitude = Column(Numeric(9, 6))
    longitude = Column(Numeric(9, 6))
    notes = Column(Text)
    source_url = Column(Text)
    source_type = Column(String(30))
    confidence_level = Column(String(20))
    entry_fee_note = Column(Text)
    footwear_note_en = Column(Text)
    mobile_note_en = Column(Text)
    dress_code_en = Column(Text)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=_utcnow)
    updated_at = Column(DateTime, default=_utcnow, onupdate=_utcnow)

    schedules = relationship("Schedule", back_populates="temple", cascade="all, delete-orphan")
    advisories = relationship("TempleAdvisory", back_populates="temple", cascade="all, delete-orphan")
    festival_overrides = relationship("FestivalOverride", back_populates="temple", cascade="all, delete-orphan")
    routes = relationship("Route", back_populates="temple", cascade="all, delete-orphan")

    def display_name(self, lang: str = "en") -> str:
        return {"hi": self.name_hi, "bn": self.name_bn, "ta": self.name_ta}.get(lang) or self.name_en


class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True)
    temple_id = Column(Integer, ForeignKey("temples.id", ondelete="CASCADE"))
    season = Column(String(30))
    open_morning = Column(Time)
    close_morning = Column(Time)
    bhog_start = Column(Time)
    bhog_end = Column(Time)
    open_evening = Column(Time)
    close_evening = Column(Time)
    notes_en = Column(Text)
    notes_hi = Column(Text)
    source_url = Column(Text)
    verified_by = Column(String(100))
    verified_at = Column(DateTime)
    is_current = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=_utcnow)

    temple = relationship("Temple", back_populates="schedules")


class FestivalOverride(Base):
    __tablename__ = "festival_overrides"

    id = Column(Integer, primary_key=True)
    temple_id = Column(Integer, ForeignKey("temples.id", ondelete="CASCADE"))
    festival_name = Column(String(120))
    date_from = Column(Date, nullable=False)
    date_to = Column(Date, nullable=False)
    open_morning = Column(Time)
    close_morning = Column(Time)
    open_evening = Column(Time)
    close_evening = Column(Time)
    notice_text_en = Column(Text)
    notice_text_hi = Column(Text)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=_utcnow)

    temple = relationship("Temple", back_populates="festival_overrides")


class TempleAdvisory(Base):
    __tablename__ = "temple_advisories"

    id = Column(Integer, primary_key=True)
    temple_id = Column(Integer, ForeignKey("temples.id", ondelete="CASCADE"))
    advisory_type = Column(String(50))
    message_en = Column(Text, nullable=False)
    message_hi = Column(Text)
    message_bn = Column(Text)
    message_ta = Column(Text)
    priority = Column(Integer, default=1, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    temple = relationship("Temple", back_populates="advisories")


class RoutePoint(Base):
    __tablename__ = "route_points"

    id = Column(Integer, primary_key=True)
    code = Column(String(60), unique=True, nullable=False)
    name_en = Column(String(150), nullable=False)
    name_hi = Column(String(150))
    name_bn = Column(String(150))
    name_ta = Column(String(150))
    area = Column(String(120))
    city = Column(String(80))
    point_type = Column(String(40))
    latitude = Column(Numeric(9, 6))
    longitude = Column(Numeric(9, 6))

    routes = relationship("Route", back_populates="from_point")


class Route(Base):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True)
    from_point_id = Column(Integer, ForeignKey("route_points.id"))
    temple_id = Column(Integer, ForeignKey("temples.id"))
    mode = Column(String(30))
    duration_min_est = Column(Integer)
    fare_min = Column(Integer)
    fare_max = Column(Integer)
    fare_currency = Column(String(5), default="INR")
    route_text_en = Column(Text, nullable=False)
    route_text_hi = Column(Text)
    route_text_bn = Column(Text)
    route_text_ta = Column(Text)
    map_link = Column(Text)
    last_mile_note = Column(Text)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    verified_at = Column(DateTime)

    from_point = relationship("RoutePoint", back_populates="routes")
    temple = relationship("Temple", back_populates="routes")


class FareGuide(Base):
    __tablename__ = "fare_guides"

    id = Column(Integer, primary_key=True)
    from_label = Column(String(120))
    to_label = Column(String(120))
    service_type = Column(String(60))
    fare_min = Column(Integer)
    fare_max = Column(Integer)
    currency = Column(String(5), default="INR")
    fare_note_en = Column(Text)
    is_official = Column(Boolean, default=False, nullable=False)
    source_label = Column(String(100))
    verified_at = Column(DateTime)


class PartnerCategory(Base):
    __tablename__ = "partner_categories"

    id = Column(Integer, primary_key=True)
    code = Column(String(60), unique=True, nullable=False)
    name = Column(String(80), nullable=False)
    name_en = Column(String(80))
    name_hi = Column(String(80))
    icon_emoji = Column(String(16))
    slug = Column(String(60), unique=True, nullable=False)
    priority_order = Column(Integer, default=10, nullable=False)

    partners = relationship("Partner", back_populates="category")


class Partner(Base):
    __tablename__ = "partners"

    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey("partner_categories.id"))
    name = Column(String(200), nullable=False)
    phone = Column(String(30))
    whatsapp = Column(String(30))
    area = Column(String(120))
    temple_focus = Column(String(80))
    short_desc_en = Column(Text)
    price_note = Column(Text)
    verified = Column(Boolean, default=False, nullable=False)
    verified_by = Column(String(100))
    verified_at = Column(DateTime)
    plan_type = Column(String(20))
    monthly_fee = Column(Integer)
    subscription_end = Column(Date)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=_utcnow)

    category = relationship("PartnerCategory", back_populates="partners")


class UserSession(Base):
    __tablename__ = "user_sessions"

    id = Column(Integer, primary_key=True)
    wa_number = Column(String(30), unique=True, nullable=False)
    language_code = Column(String(10), default="en", nullable=False)
    current_state = Column(String(60), default="language_select", nullable=False)
    prev_state = Column(String(60))
    last_intent = Column(String(60))
    last_entity = Column(String(80))
    selected_temple = Column(String(60))
    selected_route_from = Column(String(60))
    pending_action = Column(String(20))
    selected_area = Column(String(50))
    message_count = Column(Integer, default=0, nullable=False)
    updated_at = Column(DateTime, default=_utcnow, onupdate=_utcnow)
    created_at = Column(DateTime, default=_utcnow)


class SupportRequest(Base):
    __tablename__ = "support_requests"

    id = Column(Integer, primary_key=True)
    wa_number = Column(String(30))
    language_code = Column(String(10))
    request_type = Column(String(60))
    temple_id = Column(Integer, ForeignKey("temples.id"))
    message_text = Column(Text)
    status = Column(String(30), default="open", nullable=False)
    assigned_to = Column(String(100))
    notes = Column(Text)
    created_at = Column(DateTime, default=_utcnow)
    resolved_at = Column(DateTime)


class QueryLog(Base):
    __tablename__ = "query_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    wa_number = Column(String(30))
    language_code = Column(String(10))
    incoming_text = Column(Text)
    detected_state = Column(String(60))
    detected_intent = Column(String(60))
    detected_entity = Column(String(80))
    response_status = Column(String(30), default="ok", nullable=False)
    processing_ms = Column(Integer)
    created_at = Column(DateTime, default=_utcnow)
