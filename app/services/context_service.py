from __future__ import annotations

import json
from typing import Any, Optional

from pydantic import BaseModel, Field


class SessionContext(BaseModel):
    """
    Structured context data for a user session.
    Used for Context Engineering to provide more relevant responses.
    """
    last_visited_area: Optional[str] = None
    last_visited_temple: Optional[str] = None
    preferred_city: Optional[str] = None
    interaction_history: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def from_json(cls, data: Optional[str]) -> SessionContext:
        if not data:
            return cls()
        try:
            return cls.model_validate_json(data)
        except Exception:
            return cls()

    def to_json(self) -> str:
        return self.model_dump_json()


class ContextManager:
    """
    Manages the context for a given user session.
    Provides methods to update user history and retrieve context-aware suggestions.
    """
    def __init__(self, session: Any):
        """Initialize with a SQLAlchemy session object."""
        self.session = session
        self.context = SessionContext.from_json(session.context_data)

    def update_visited_area(self, area: str):
        """Update the last visited area in the session context."""
        self.context.last_visited_area = area
        self._sync()

    def update_visited_temple(self, temple_code: str):
        """Update the last visited temple in the session context."""
        self.context.last_visited_temple = temple_code
        self._sync()

    def add_interaction(self, intent: str):
        """Record a user interaction intent for behavior tracking."""
        self.context.interaction_history.append(intent)
        # Keep only last 10 interactions
        if len(self.context.interaction_history) > 10:
            self.context.interaction_history.pop(0)
        self._sync()

    def _sync(self):
        """Sync the pydantic model back to the SQLAlchemy session object."""
        self.session.context_data = self.context.to_json()

    def get_suggested_area(self) -> Optional[str]:
        """Context-aware suggestion for the user's area."""
        return self.context.last_visited_area or self.context.preferred_city
