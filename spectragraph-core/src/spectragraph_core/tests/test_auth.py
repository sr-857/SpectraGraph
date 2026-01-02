"""Tests for authentication module."""
import os
import pytest
from datetime import datetime, timedelta

# Set AUTH_SECRET for testing before importing auth module
os.environ['AUTH_SECRET'] = 'test_secret_for_testing_only'

from jose import jwt
from spectragraph_core.core.auth import (
    create_access_token,
    verify_password,
    get_password_hash,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    AUTH_SECRET,
    ALGORITHM,
)


class TestPasswordHashing:
    """Test password hashing and verification."""

    def test_password_hash_and_verify(self):
        """Test that password hashing and verification works correctly."""
        password = "test_password_123"
        hashed = get_password_hash(password)
        
        # Hashed password should be different from plain password
        assert hashed != password
        
        # Verification should succeed with correct password
        assert verify_password(password, hashed) is True
        
        # Verification should fail with incorrect password
        assert verify_password("wrong_password", hashed) is False


class TestTokenGeneration:
    """Test JWT token generation and expiration."""

    def test_token_expiration_is_60_minutes(self):
        """
        Test that ACCESS_TOKEN_EXPIRE_MINUTES is set to 60 minutes (1 hour).
        
        This is a security requirement - tokens should not be valid for too long.
        Previously this was incorrectly set to 3600 minutes (60 hours).
        """
        assert ACCESS_TOKEN_EXPIRE_MINUTES == 60, (
            f"Token expiration should be 60 minutes, but is set to "
            f"{ACCESS_TOKEN_EXPIRE_MINUTES} minutes"
        )

    def test_token_contains_required_claims(self):
        """Test that generated token contains required claims."""
        test_data = {"sub": "test@example.com", "custom":  "data"}
        token = create_access_token(data=test_data)
        
        decoded = jwt.decode(token, AUTH_SECRET, algorithms=[ALGORITHM])
        
        # Check required claims
        assert "sub" in decoded
        assert "exp" in decoded
        assert decoded["sub"] == "test@example.com"
        assert decoded["custom"] == "data"
    
    def test_token_has_expiration(self):
        """Test that tokens have an expiration time set."""
        test_data = {"sub": "test@example.com"}
        token = create_access_token(data=test_data)
        
        decoded = jwt.decode(token, AUTH_SECRET, algorithms=[ALGORITHM])
        
        # Token should have expiration
        assert "exp" in decoded
        
        # Expiration should be in the future
        exp_timestamp = decoded["exp"]
        current_timestamp = datetime.utcnow().timestamp()
        assert exp_timestamp > current_timestamp, "Token expiration should be in the future"