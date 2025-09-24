"""Unit tests for custom arithmetic service exceptions."""

import pytest
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
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


# Self-contained temporary FastAPI app for integration testing
# This follows the action item requirements exactly
test_app = FastAPI()

@test_app.exception_handler(ArithmeticServiceError)
async def arithmetic_exception_handler(request: Request, exc: ArithmeticServiceError) -> JSONResponse:
    """Exception handler for ArithmeticServiceError in test app.
    
    Args:
        request: The incoming request
        exc: The ArithmeticServiceError instance
        
    Returns:
        JSONResponse: Response with status code and detail from the exception
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@test_app.get("/test-exception/{exception_type}")
async def handle_exception_route(exception_type: str) -> dict[str, str]:
    """Route handler that raises different exception types based on path parameter.
    
    Args:
        exception_type: Type of exception to raise
        
    Returns:
        dict: Success message if no exception is raised
        
    Raises:
        DivisionByZeroError: When exception_type is 'division_by_zero'
        CalculationOverflowError: When exception_type is 'overflow'
        UnsupportedOperationError: When exception_type is 'unsupported'
    """
    if exception_type == "division_by_zero":
        raise DivisionByZeroError()
    elif exception_type == "overflow":
        raise CalculationOverflowError()
    elif exception_type == "unsupported":
        raise UnsupportedOperationError()
    return {"message": "No exception raised"}


class TestFastAPIExceptionHandlerIntegration:
    """Integration tests using self-contained temporary FastAPI app.
    
    These tests use a temporary FastAPI app as required by the action item,
    rather than the global app and client fixture.
    """

    def test_division_by_zero_error_integration(self) -> None:
        """Test that DivisionByZeroError is handled correctly by FastAPI.
        
        Uses self-contained TestClient with temporary FastAPI app as required.
        """
        with TestClient(test_app) as client:
            response = client.get("/test-exception/division_by_zero")
            
            assert response.status_code == 400
            response_data = response.json()
            assert response_data == {"detail": "Division by zero is not allowed"}

    def test_calculation_overflow_error_integration(self) -> None:
        """Test that CalculationOverflowError is handled correctly by FastAPI.
        
        Uses self-contained TestClient with temporary FastAPI app as required.
        """
        with TestClient(test_app) as client:
            response = client.get("/test-exception/overflow")
            
            assert response.status_code == 400
            response_data = response.json()
            assert response_data == {"detail": "Calculation result exceeds supported range"}

    def test_unsupported_operation_error_integration(self) -> None:
        """Test that UnsupportedOperationError is handled correctly by FastAPI.
        
        Uses self-contained TestClient with temporary FastAPI app as required.
        """
        with TestClient(test_app) as client:
            response = client.get("/test-exception/unsupported")
            
            assert response.status_code == 400
            response_data = response.json()
            assert response_data == {"detail": "Unsupported operation"}

    def test_no_exception_raised_returns_success(self) -> None:
        """Test that route returns success message when no exception is raised.
        
        Uses self-contained TestClient with temporary FastAPI app as required.
        """
        with TestClient(test_app) as client:
            response = client.get("/test-exception/no_error")
            
            assert response.status_code == 200
            response_data = response.json()
            assert response_data == {"message": "No exception raised"}

    def test_exception_handler_response_format(self) -> None:
        """Test that exception handler returns properly formatted JSON response.
        
        Uses self-contained TestClient with temporary FastAPI app as required.
        """
        with TestClient(test_app) as client:
            # Test all exception types to verify consistent formatting
            test_cases = [
                ("division_by_zero", "Division by zero is not allowed"),
                ("overflow", "Calculation result exceeds supported range"),
                ("unsupported", "Unsupported operation")
            ]
            
            for exception_type, expected_detail in test_cases:
                response = client.get(f"/test-exception/{exception_type}")
                
                # Verify response structure and content
                assert response.status_code == 400
                response_data = response.json()
                assert isinstance(response_data, dict)
                assert "detail" in response_data
                assert response_data["detail"] == expected_detail
                
                # Verify response has correct content type
                assert "application/json" in response.headers["content-type"]

    def test_exception_handler_preserves_status_codes(self) -> None:
        """Test that exception handler preserves the status_code from exceptions.
        
        Uses self-contained TestClient with temporary FastAPI app as required.
        """
        with TestClient(test_app) as client:
            # All our custom exceptions use HTTP 400 by default
            exception_types = ["division_by_zero", "overflow", "unsupported"]
            
            for exception_type in exception_types:
                response = client.get(f"/test-exception/{exception_type}")
                assert response.status_code == 400
