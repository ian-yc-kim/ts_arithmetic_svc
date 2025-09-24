"""Custom exceptions for the arithmetic service."""

from fastapi import HTTPException, status


class ArithmeticServiceError(HTTPException):
    """Base exception class for arithmetic service errors.
    
    Inherits directly from fastapi.HTTPException to ensure compatibility
    with FastAPI's exception handling mechanism.
    """
    status_code: int = status.HTTP_400_BAD_REQUEST
    detail: str = "Arithmetic service error"
    
    def __init__(
        self,
        detail: str | None = None,
        status_code: int | None = None,
        headers: dict[str, str] | None = None
    ) -> None:
        """Initialize ArithmeticServiceError.
        
        Args:
            detail: Error detail message. Uses class attribute if None.
            status_code: HTTP status code. Uses class attribute if None.
            headers: Optional HTTP headers.
        """
        resolved_status = status_code if status_code is not None else self.status_code
        resolved_detail = detail if detail is not None else self.detail
        super().__init__(status_code=resolved_status, detail=resolved_detail, headers=headers)


class DivisionByZeroError(ArithmeticServiceError):
    """Exception raised when attempting division by zero."""
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Division by zero is not allowed"


class CalculationOverflowError(ArithmeticServiceError):
    """Exception raised when calculation result exceeds supported range."""
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Calculation result exceeds supported range"


class UnsupportedOperationError(ArithmeticServiceError):
    """Exception raised for unsupported operations."""
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Unsupported operation"


__all__ = [
    "ArithmeticServiceError",
    "DivisionByZeroError",
    "CalculationOverflowError",
    "UnsupportedOperationError"
]
