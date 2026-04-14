"""
Timezone utilities for BrajPath.
Ensures all timestamps are stored in UTC internally.
Display times converted to Indian Standard Time (IST) as needed.

Design:
- Database: All timestamps stored as UTC (naive)
- Internal processing: Use UTC for consistency
- User display: Convert to IST (UTC+5:30) for temple timings
- External APIs: Accept UTC, return UTC
"""
from datetime import datetime, timedelta, timezone

# IST is UTC+5:30
IST = timezone(timedelta(hours=5, minutes=30))
UTC = timezone.utc


def now_utc() -> datetime:
    """Get current UTC time as naive datetime (database format)."""
    return datetime.now(UTC).replace(tzinfo=None)


def now_ist() -> datetime:
    """Get current IST time as naive datetime (for display/logic)."""
    return datetime.now(IST).replace(tzinfo=None)


def utc_to_ist(utc_dt: datetime) -> datetime:
    """Convert UTC naive datetime to IST naive datetime.
    
    Args:
        utc_dt: Naive datetime in UTC
        
    Returns:
        Naive datetime in IST (UTC+5:30)
    """
    if utc_dt.tzinfo is not None:
        utc_dt = utc_dt.replace(tzinfo=None)
    # Add IST offset
    ist_dt = utc_dt + timedelta(hours=5, minutes=30)
    return ist_dt.replace(tzinfo=None)


def ist_to_utc(ist_dt: datetime) -> datetime:
    """Convert IST naive datetime to UTC naive datetime.
    
    Args:
        ist_dt: Naive datetime in IST
        
    Returns:
        Naive datetime in UTC
    """
    if ist_dt.tzinfo is not None:
        ist_dt = ist_dt.replace(tzinfo=None)
    # Subtract IST offset
    utc_dt = ist_dt - timedelta(hours=5, minutes=30)
    return utc_dt.replace(tzinfo=None)


def format_ist_time(utc_dt: datetime | None, fmt: str = "%I:%M %p") -> str:
    """Format UTC datetime as IST for display.
    
    Args:
        utc_dt: Naive datetime in UTC
        fmt: Strftime format string
        
    Returns:
        Formatted IST time string
    """
    if utc_dt is None:
        return "—"
    ist_dt = utc_to_ist(utc_dt)
    return ist_dt.strftime(fmt).lstrip("0")
