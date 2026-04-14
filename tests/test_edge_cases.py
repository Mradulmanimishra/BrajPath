"""
Edge case and validation tests for BrajPath.
Tests phone validation, language fallback, and error handling.
"""
import re
import pytest
from sqlalchemy.orm import Session

from app.services.state_machine import LANG_MAP, process_message


# ── Phone Validation Tests ──────────────────────────────────────────────────

class TestPhoneValidation:
    """Test phone number format validation with various edge cases.
    
    Uses the same regex pattern as webhook.py: r"^\\+?[0-9]{1,15}$"
    """

    PHONE_PATTERN = r"^\+?[0-9]{1,15}$"

    def _validate_phone(self, wa_number: str) -> bool:
        """Replicate phone validation logic from webhook.py"""
        cleaned = wa_number.replace("-", "").replace(" ", "")
        return bool(re.match(self.PHONE_PATTERN, cleaned))

    def test_valid_indian_with_plus(self) -> None:
        """Accept Indian number with + prefix (E.164 format)."""
        assert self._validate_phone("+919876543210") is True

    def test_valid_indian_without_plus(self) -> None:
        """Accept Indian number without + prefix."""
        assert self._validate_phone("919876543210") is True

    def test_valid_international_with_plus(self) -> None:
        """Accept international format with +."""
        assert self._validate_phone("+1234567890") is True

    def test_valid_with_spaces(self) -> None:
        """Accept numbers with spaces (should be normalized)."""
        assert self._validate_phone("+91 9876 543210") is True

    def test_valid_with_hyphen(self) -> None:
        """Accept numbers with hyphens (should be normalized)."""
        assert self._validate_phone("+91-9876-543210") is True

    def test_invalid_empty_string(self) -> None:
        """Reject empty string."""
        assert self._validate_phone("") is False

    def test_valid_single_digit(self) -> None:
        """Accept single digit (meets minimum requirement)."""
        assert self._validate_phone("1") is True

    def test_valid_plus_single_digit(self) -> None:
        """Accept plus with single digit."""
        assert self._validate_phone("+9") is True

    def test_invalid_too_long(self) -> None:
        """Reject number longer than 15 digits."""
        assert self._validate_phone("+919876543210123456") is False

    def test_invalid_with_letters(self) -> None:
        """Reject number containing letters."""
        assert self._validate_phone("+91abc123456") is False

    def test_invalid_with_special_chars(self) -> None:
        """Reject number with special characters (not hyphen/space)."""
        assert self._validate_phone("+91#9876543210") is False

    def test_invalid_only_plus_sign(self) -> None:
        """Reject just + sign without digits."""
        assert self._validate_phone("+") is False

    def test_maximum_valid_length(self) -> None:
        """Accept maximum valid length (15 digits)."""
        assert self._validate_phone("+123456789012345") is True


# ── Language Fallback Tests ─────────────────────────────────────────────────

class TestLanguageFallback:
    """Test language code validation and fallback behavior."""

    def test_all_supported_languages(self) -> None:
        """Verify all supported language codes are valid."""
        for code in LANG_MAP.values():
            assert code in ("en", "hi", "bn", "ta"), f"Unsupported language: {code}"

    def test_language_mapping(self) -> None:
        """Verify language menu input maps to correct codes."""
        assert LANG_MAP["1"] == "en"
        assert LANG_MAP["2"] == "hi"
        assert LANG_MAP["3"] == "bn"
        assert LANG_MAP["4"] == "ta"

    def test_language_count(self) -> None:
        """Verify exact number of supported languages."""
        assert len(LANG_MAP) == 4


# ── State Machine Edge Cases ─────────────────────────────────────────────────

class TestStateValidation:
    """Test state machine handles edge case inputs gracefully."""

    def test_empty_message_input(self, db_session: Session) -> None:
        """State machine should handle empty message gracefully."""
        reply = process_message("+919876543210", "", db_session)
        # Should not crash; returns help_escalation or similar
        assert isinstance(reply, str)

    def test_very_long_message(self, db_session: Session) -> None:
        """State machine should handle very long messages gracefully."""
        long_message = "A" * 2000  # Very long input
        reply = process_message("+919876543210", long_message, db_session)
        # Should not crash; might hit message truncation in _safe()
        assert isinstance(reply, str)
        assert len(reply) <= 1600  # _safe() max length

    def test_unicode_hindi_input(self, db_session: Session) -> None:
        """State machine should handle Unicode Hindi input gracefully."""
        unicode_message = "नमस्ते"  # Hindi text
        reply = process_message("+919876543210", unicode_message, db_session)
        assert isinstance(reply, str)

    def test_unicode_bengali_input(self, db_session: Session) -> None:
        """State machine should handle Unicode Bengali input gracefully."""
        unicode_message = "নমস্কার"  # Bengali text
        reply = process_message("+919876543210", unicode_message, db_session)
        assert isinstance(reply, str)

    def test_special_characters_only(self, db_session: Session) -> None:
        """State machine should handle special characters gracefully."""
        special_message = "!@#$%^&*()"
        reply = process_message("+919876543210", special_message, db_session)
        # Should not crash
        assert isinstance(reply, str)

    def test_whitespace_only_input(self, db_session: Session) -> None:
        """State machine should handle whitespace-only input gracefully."""
        whitespace_message = "     "
        reply = process_message("+919876543210", whitespace_message, db_session)
        # After stripping, becomes empty; should handle gracefully
        assert isinstance(reply, str)

    def test_newline_in_message(self, db_session: Session) -> None:
        """State machine should handle newlines in input gracefully."""
        message_with_newline = "hello\nworld"
        reply = process_message("+919876543210", message_with_newline, db_session)
        assert isinstance(reply, str)
