"""Tests for FastAPI application setup and configuration."""

import decimal

import pytest
from fastapi.testclient import TestClient

from ts_arithmetic_svc.app import app


class TestAppSetup:
    """Test class for FastAPI application setup verification."""

    def test_app_starts_successfully(self, client: TestClient) -> None:
        """Test that the FastAPI application starts successfully without errors.
        
        Args:
            client: TestClient fixture from conftest.py
        """
        # The fact that we can create a client and make a request means the app started successfully
        response = client.get("/")
        assert response is not None

    def test_root_endpoint_status_code(self, client: TestClient) -> None:
        """Test that GET request to root endpoint returns HTTP status code 200.
        
        Args:
            client: TestClient fixture from conftest.py
        """
        response = client.get("/")
        assert response.status_code == 200

    def test_root_endpoint_response_content(self, client: TestClient) -> None:
        """Test that root endpoint returns correct JSON response.
        
        Args:
            client: TestClient fixture from conftest.py
        """
        response = client.get("/")
        expected_response = {"message": "Arithmetic Service is running"}
        assert response.json() == expected_response

    def test_decimal_context_precision(self) -> None:
        """Test that global decimal context precision is set to at least 28."""
        # Import the app module to ensure decimal context is set
        import ts_arithmetic_svc.app  # noqa: F401
        
        current_precision = decimal.getcontext().prec
        assert current_precision >= 28, f"Expected precision >= 28, got {current_precision}"

    def test_fastapi_metadata(self) -> None:
        """Test that FastAPI application metadata matches specified values."""
        assert app.title == "Arithmetic Service API"
        assert app.description == "A high-precision arithmetic service using FastAPI."
        assert app.version == "1.0.0"
