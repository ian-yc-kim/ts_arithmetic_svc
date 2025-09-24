"""Calculate endpoint router for arithmetic operations."""

import logging
from typing import Dict, Callable
from decimal import Decimal

from fastapi import APIRouter, status

from ts_arithmetic_svc.api.models import (
    CalculationRequest,
    CalculationResponse,
    OperationType
)
from ts_arithmetic_svc.core.calculator import add, subtract, multiply, divide
from ts_arithmetic_svc.exceptions import (
    DivisionByZeroError,
    CalculationOverflowError,
    UnsupportedOperationError
)

logger = logging.getLogger(__name__)

calculate_router = APIRouter()


@calculate_router.post(
    "/calculate",
    response_model=CalculationResponse,
    status_code=status.HTTP_200_OK
)
async def calculate(request: CalculationRequest) -> CalculationResponse:
    """Perform arithmetic calculation based on the request.
    
    Args:
        request: CalculationRequest containing operation type and operands
        
    Returns:
        CalculationResponse: Result of the calculation along with operation and operands
        
    Raises:
        DivisionByZeroError: When attempting to divide by zero
        CalculationOverflowError: When calculation result exceeds supported range
        UnsupportedOperationError: When operation type is not supported
    """
    # Operation mapping from OperationType to calculator functions
    # Moved inside function so it's created at runtime and picks up mocked functions
    operation_map: Dict[OperationType, Callable[[Decimal, Decimal], Decimal]] = {
        OperationType.ADD: add,
        OperationType.SUBTRACT: subtract,
        OperationType.MULTIPLY: multiply,
        OperationType.DIVIDE: divide,
    }
    
    try:
        # Get the calculator function for the requested operation
        if request.operation not in operation_map:
            raise UnsupportedOperationError(
                detail=f"Unsupported operation: {request.operation}"
            )
        
        calculator_func = operation_map[request.operation]
        
        # Perform the calculation
        result = calculator_func(request.a, request.b)
        
        # Return the response
        return CalculationResponse(
            result=result,
            operation=request.operation,
            operands=[request.a, request.b]
        )
        
    except (DivisionByZeroError, CalculationOverflowError, UnsupportedOperationError) as e:
        # Log the error with full traceback
        logging.error(e, exc_info=True)
        # Re-raise the exception to be handled by the global exception handler
        raise
    except Exception as e:
        # Log unexpected errors
        logging.error(f"Unexpected error in calculate endpoint: {e}", exc_info=True)
        # Convert unexpected errors to UnsupportedOperationError
        raise UnsupportedOperationError(
            detail="An unexpected error occurred during calculation"
        )
