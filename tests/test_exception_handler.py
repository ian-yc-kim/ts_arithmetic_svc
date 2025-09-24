"""Integration tests for the FastAPI exception handler."""

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from ts_arithmetic_svc.exceptions import (
    ArithmeticServiceError,
    DivisionByZeroError,
    CalculationOverflowError,
    UnsupportedOperationError
)


class TestExceptionHandlerIntegration:
    """Integration tests for exception handler behavior in FastAPI app."""

    def test_arithmetic_service_error_response_format(self, client: TestClient) -> None:
        """Test that exception handler returns properly formatted JSON response.
        
        Args:
            client: TestClient fixture from conftest.py
        """
        from fastapi import APIRouter
        from ts_arithmetic_svc.app import app
        
        # Create test route
        test_router = APIRouter()
        
        @test_router.get("/test-error-format")
        async def test_error_format():
            raise ArithmeticServiceError(
                detail="Formatted error message",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        app.include_router(test_router)
        
        response = client.get("/test-error-format")
        
        # Verify response structure
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        response_data = response.json()
        
        # Verify response has correct structure
        assert isinstance(response_data, dict)
        assert "detail" in response_data
        assert response_data["detail"] == "Formatted error message"
        
        # Verify response has correct content type
        assert "application/json" in response.headers["content-type"]

    def test_all_exception_types_handled_consistently(self, client: TestClient) -> None:
        """Test that all exception types are handled with consistent format.
        
        Args:
            client: TestClient fixture from conftest.py
        """
        from fastapi import APIRouter
        from ts_arithmetic_svc.app import app
        
        exception_test_cases = [
            ("division-by-zero", DivisionByZeroError, "Division by zero is not allowed"),
            ("overflow", CalculationOverflowError, "Calculation result exceeds supported range"),
            ("unsupported", UnsupportedOperationError, "Unsupported operation"),
        ]
        
        test_router = APIRouter()
        
        # Create test routes for each exception type
        for route_name, exception_class, expected_detail in exception_test_cases:
            def create_handler(exc_class):
                async def handler():
                    raise exc_class()
                return handler
            
            test_router.add_api_route(
                f"/test-{route_name}",
                create_handler(exception_class),
                methods=["GET"]
            )
        
        app.include_router(test_router)
        
        # Test each exception type
        for route_name, exception_class, expected_detail in exception_test_cases:
            response = client.get(f"/test-{route_name}")
            
            # Verify consistent response format
            assert response.status_code == status.HTTP_400_BAD_REQUEST
            response_data = response.json()
            
            assert isinstance(response_data, dict)
            assert "detail" in response_data
            assert response_data["detail"] == expected_detail

    def test_exception_handler_preserves_custom_status_codes(self, client: TestClient) -> None:
        """Test that custom status codes are preserved by the exception handler.
        
        Args:
            client: TestClient fixture from conftest.py
        """
        from fastapi import APIRouter
        from ts_arithmetic_svc.app import app
        
        test_router = APIRouter()
        
        custom_status_codes = [
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            status.HTTP_409_CONFLICT,
            status.HTTP_503_SERVICE_UNAVAILABLE
        ]
        
        for i, custom_status in enumerate(custom_status_codes):
            def create_handler(status_code):
                async def handler():
                    raise ArithmeticServiceError(
                        detail=f"Error with status {status_code}",
                        status_code=status_code
                    )
                return handler
            
            test_router.add_api_route(
                f"/test-status-{i}",
                create_handler(custom_status),
                methods=["GET"]
            )
        
        app.include_router(test_router)
        
        for i, expected_status in enumerate(custom_status_codes):
            response = client.get(f"/test-status-{i}")
            
            # Verify custom status code is preserved
            assert response.status_code == expected_status
            response_data = response.json()
            assert response_data["detail"] == f"Error with status {expected_status}"

    def test_exception_handler_does_not_affect_other_http_exceptions(self, client: TestClient) -> None:
        """Test that the handler only affects ArithmeticServiceError and its subclasses.
        
        Args:
            client: TestClient fixture from conftest.py
        """
        from fastapi import APIRouter, HTTPException
        from ts_arithmetic_svc.app import app
        
        test_router = APIRouter()
        
        @test_router.get("/test-http-exception")
        async def test_http_exception():
            # Raise a regular HTTPException (not ArithmeticServiceError)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Regular HTTP exception"
            )
        
        app.include_router(test_router)
        
        # Test regular HTTPException - should work normally
        response = client.get("/test-http-exception")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Regular HTTP exception"

    def test_exception_handler_with_none_detail(self, client: TestClient) -> None:
        """Test exception handler behavior when detail is None.
        
        Args:
            client: TestClient fixture from conftest.py
        """
        from fastapi import APIRouter
        from ts_arithmetic_svc.app import app
        
        test_router = APIRouter()
        
        @test_router.get("/test-none-detail")
        async def test_none_detail():
            # Create exception with None detail (should use class default)
            raise ArithmeticServiceError(detail=None)
        
        app.include_router(test_router)
        
        response = client.get("/test-none-detail")
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        response_data = response.json()
        # Should use the class default detail
        assert response_data["detail"] == "Arithmetic service error"
