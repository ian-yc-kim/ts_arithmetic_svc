"""Unit tests for custom arithmetic service exceptions."""

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from ts_arithmetic_svc.exceptions import (
    ArithmeticServiceError,
    DivisionByZeroError,
    CalculationOverflowError,
    UnsupportedOperationError
)


class TestArithmeticServiceError:
    """Test cases for the base ArithmeticServiceError class."""

    def test_default_initialization(self) -> None:
        """Test ArithmeticServiceError with default values."""
        exc = ArithmeticServiceError()
        assert exc.status_code == status.HTTP_400_BAD_REQUEST
        assert exc.detail == "Arithmetic service error"
        assert exc.headers is None

    def test_custom_detail_initialization(self) -> None:
        """Test ArithmeticServiceError with custom detail message."""
        custom_detail = "Custom error message"
        exc = ArithmeticServiceError(detail=custom_detail)
        assert exc.status_code == status.HTTP_400_BAD_REQUEST
        assert exc.detail == custom_detail
        assert exc.headers is None

    def test_custom_status_code_initialization(self) -> None:
        """Test ArithmeticServiceError with custom status code."""
        custom_status = status.HTTP_500_INTERNAL_SERVER_ERROR
        exc = ArithmeticServiceError(status_code=custom_status)
        assert exc.status_code == custom_status
        assert exc.detail == "Arithmetic service error"
        assert exc.headers is None

    def test_custom_headers_initialization(self) -> None:
        """Test ArithmeticServiceError with custom headers."""
        custom_headers = {"X-Error-Code": "ARITHMETIC_001"}
        exc = ArithmeticServiceError(headers=custom_headers)
        assert exc.status_code == status.HTTP_400_BAD_REQUEST
        assert exc.detail == "Arithmetic service error"
        assert exc.headers == custom_headers

    def test_full_custom_initialization(self) -> None:
        """Test ArithmeticServiceError with all custom parameters."""
        custom_detail = "Custom error"
        custom_status = status.HTTP_422_UNPROCESSABLE_ENTITY
        custom_headers = {"X-Custom": "value"}
        
        exc = ArithmeticServiceError(
            detail=custom_detail,
            status_code=custom_status,
            headers=custom_headers
        )
        
        assert exc.status_code == custom_status
        assert exc.detail == custom_detail
        assert exc.headers == custom_headers

    def test_inheritance_from_http_exception(self) -> None:
        """Test that ArithmeticServiceError inherits from HTTPException."""
        from fastapi import HTTPException
        
        exc = ArithmeticServiceError()
        assert isinstance(exc, HTTPException)


class TestDivisionByZeroError:
    """Test cases for DivisionByZeroError."""

    def test_default_initialization(self) -> None:
        """Test DivisionByZeroError with default values."""
        exc = DivisionByZeroError()
        assert exc.status_code == status.HTTP_400_BAD_REQUEST
        assert exc.detail == "Division by zero is not allowed"
        assert exc.headers is None

    def test_custom_detail_override(self) -> None:
        """Test DivisionByZeroError with custom detail message."""
        custom_detail = "Custom division by zero error"
        exc = DivisionByZeroError(detail=custom_detail)
        assert exc.status_code == status.HTTP_400_BAD_REQUEST
        assert exc.detail == custom_detail

    def test_inheritance(self) -> None:
        """Test that DivisionByZeroError inherits from ArithmeticServiceError."""
        exc = DivisionByZeroError()
        assert isinstance(exc, ArithmeticServiceError)
        assert isinstance(exc, type(ArithmeticServiceError()))

    def test_class_attributes(self) -> None:
        """Test that class attributes are set correctly."""
        assert DivisionByZeroError.status_code == status.HTTP_400_BAD_REQUEST
        assert DivisionByZeroError.detail == "Division by zero is not allowed"


class TestCalculationOverflowError:
    """Test cases for CalculationOverflowError."""

    def test_default_initialization(self) -> None:
        """Test CalculationOverflowError with default values."""
        exc = CalculationOverflowError()
        assert exc.status_code == status.HTTP_400_BAD_REQUEST
        assert exc.detail == "Calculation result exceeds supported range"
        assert exc.headers is None

    def test_custom_detail_override(self) -> None:
        """Test CalculationOverflowError with custom detail message."""
        custom_detail = "Custom overflow error"
        exc = CalculationOverflowError(detail=custom_detail)
        assert exc.status_code == status.HTTP_400_BAD_REQUEST
        assert exc.detail == custom_detail

    def test_inheritance(self) -> None:
        """Test that CalculationOverflowError inherits from ArithmeticServiceError."""
        exc = CalculationOverflowError()
        assert isinstance(exc, ArithmeticServiceError)

    def test_class_attributes(self) -> None:
        """Test that class attributes are set correctly."""
        assert CalculationOverflowError.status_code == status.HTTP_400_BAD_REQUEST
        assert CalculationOverflowError.detail == "Calculation result exceeds supported range"


class TestUnsupportedOperationError:
    """Test cases for UnsupportedOperationError."""

    def test_default_initialization(self) -> None:
        """Test UnsupportedOperationError with default values."""
        exc = UnsupportedOperationError()
        assert exc.status_code == status.HTTP_400_BAD_REQUEST
        assert exc.detail == "Unsupported operation"
        assert exc.headers is None

    def test_custom_detail_override(self) -> None:
        """Test UnsupportedOperationError with custom detail message."""
        custom_detail = "Custom unsupported operation error"
        exc = UnsupportedOperationError(detail=custom_detail)
        assert exc.status_code == status.HTTP_400_BAD_REQUEST
        assert exc.detail == custom_detail

    def test_inheritance(self) -> None:
        """Test that UnsupportedOperationError inherits from ArithmeticServiceError."""
        exc = UnsupportedOperationError()
        assert isinstance(exc, ArithmeticServiceError)

    def test_class_attributes(self) -> None:
        """Test that class attributes are set correctly."""
        assert UnsupportedOperationError.status_code == status.HTTP_400_BAD_REQUEST
        assert UnsupportedOperationError.detail == "Unsupported operation"


class TestExceptionHandlerIntegration:
    """Test cases for FastAPI exception handler integration."""

    def test_exception_handler_registration(self, client: TestClient) -> None:
        """Test that ArithmeticServiceError exception handler is properly registered.
        
        This test verifies that when an ArithmeticServiceError is raised in a route,
        the custom exception handler catches it and returns the appropriate JSON response.
        
        Args:
            client: TestClient fixture from conftest.py
        """
        from fastapi import APIRouter
        from ts_arithmetic_svc.app import app
        
        # Create a temporary test route that raises ArithmeticServiceError
        test_router = APIRouter()
        
        @test_router.get("/test-arithmetic-error")
        async def test_arithmetic_error():
            raise ArithmeticServiceError(
                detail="Test arithmetic error",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        # Temporarily add the test router to the app
        app.include_router(test_router)
        
        # Make request to test route
        response = client.get("/test-arithmetic-error")
        
        # Verify response matches expected format from exception handler
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"detail": "Test arithmetic error"}

    def test_division_by_zero_error_handler(self, client: TestClient) -> None:
        """Test that DivisionByZeroError is handled correctly.
        
        Args:
            client: TestClient fixture from conftest.py
        """
        from fastapi import APIRouter
        from ts_arithmetic_svc.app import app
        
        test_router = APIRouter()
        
        @test_router.get("/test-division-by-zero")
        async def test_division_by_zero():
            raise DivisionByZeroError()
        
        app.include_router(test_router)
        
        response = client.get("/test-division-by-zero")
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"detail": "Division by zero is not allowed"}

    def test_calculation_overflow_error_handler(self, client: TestClient) -> None:
        """Test that CalculationOverflowError is handled correctly.
        
        Args:
            client: TestClient fixture from conftest.py
        """
        from fastapi import APIRouter
        from ts_arithmetic_svc.app import app
        
        test_router = APIRouter()
        
        @test_router.get("/test-overflow-error")
        async def test_overflow_error():
            raise CalculationOverflowError()
        
        app.include_router(test_router)
        
        response = client.get("/test-overflow-error")
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"detail": "Calculation result exceeds supported range"}

    def test_unsupported_operation_error_handler(self, client: TestClient) -> None:
        """Test that UnsupportedOperationError is handled correctly.
        
        Args:
            client: TestClient fixture from conftest.py
        """
        from fastapi import APIRouter
        from ts_arithmetic_svc.app import app
        
        test_router = APIRouter()
        
        @test_router.get("/test-unsupported-operation")
        async def test_unsupported_operation():
            raise UnsupportedOperationError()
        
        app.include_router(test_router)
        
        response = client.get("/test-unsupported-operation")
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"detail": "Unsupported operation"}

    def test_custom_exception_details_in_handler(self, client: TestClient) -> None:
        """Test that custom exception details are preserved in handler.
        
        Args:
            client: TestClient fixture from conftest.py
        """
        from fastapi import APIRouter
        from ts_arithmetic_svc.app import app
        
        test_router = APIRouter()
        
        @test_router.get("/test-custom-details")
        async def test_custom_details():
            raise DivisionByZeroError(
                detail="Custom division error message",
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        
        app.include_router(test_router)
        
        response = client.get("/test-custom-details")
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.json() == {"detail": "Custom division error message"}


class TestExceptionModuleExports:
    """Test cases for exception module exports."""

    def test_module_exports_all_exceptions(self) -> None:
        """Test that the exceptions module exports all expected exception classes."""
        from ts_arithmetic_svc import exceptions
        
        expected_exports = {
            "ArithmeticServiceError",
            "DivisionByZeroError", 
            "CalculationOverflowError",
            "UnsupportedOperationError"
        }
        
        # Check that __all__ is defined and contains expected items
        assert hasattr(exceptions, '__all__')
        assert set(exceptions.__all__) == expected_exports
        
        # Check that all items in __all__ are actually accessible
        for export_name in exceptions.__all__:
            assert hasattr(exceptions, export_name)
            export_class = getattr(exceptions, export_name)
            assert callable(export_class)  # Should be a class (callable)
