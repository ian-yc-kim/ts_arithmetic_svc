"""Pydantic models for arithmetic service API requests and responses."""

from decimal import Decimal
from enum import Enum
from typing import List

from pydantic import BaseModel, Field, field_serializer


# Define constant for maximum absolute operand value
MAX_ABS_OPERAND = Decimal(10) ** 10


class OperationType(str, Enum):
    """Enum for supported arithmetic operations.
    
    Each operation type corresponds to a specific arithmetic calculation:
    - ADD: Addition operation
    - SUBTRACT: Subtraction operation  
    - MULTIPLY: Multiplication operation
    - DIVIDE: Division operation
    """
    ADD = "add"
    SUBTRACT = "subtract"
    MULTIPLY = "multiply"
    DIVIDE = "divide"


class CalculationRequest(BaseModel):
    """Request model for arithmetic calculations.
    
    Contains the operation type and two operands for performing
    arithmetic calculations with high precision using Decimal types.
    """
    
    operation: OperationType = Field(
        ...,
        description="The arithmetic operation to perform"
    )
    
    a: Decimal = Field(
        ...,
        ge=-MAX_ABS_OPERAND,
        le=MAX_ABS_OPERAND,
        description="First operand for the calculation (range: -10^10 to 10^10)"
    )
    
    b: Decimal = Field(
        ...,
        ge=-MAX_ABS_OPERAND, 
        le=MAX_ABS_OPERAND,
        description="Second operand for the calculation (range: -10^10 to 10^10)"
    )


class CalculationResponse(BaseModel):
    """Response model for arithmetic calculations.
    
    Contains the calculation result along with the operation performed
    and the input operands for verification purposes.
    """
    
    result: Decimal = Field(
        ...,
        description="The calculated result of the arithmetic operation"
    )
    
    operation: OperationType = Field(
        ...,
        description="The arithmetic operation that was performed"
    )
    
    operands: List[Decimal] = Field(
        ...,
        description="List containing the input operands [a, b]"
    )
    
    @field_serializer('result', when_used='json')
    def serialize_result(self, v: Decimal) -> str:
        """Serialize result as string to maintain precision in JSON.
        
        Args:
            v: The Decimal value to serialize
            
        Returns:
            String representation of the Decimal value
        """
        return str(v)
    
    @field_serializer('operands', when_used='json')
    def serialize_operands(self, v: List[Decimal]) -> List[str]:
        """Serialize operands list as strings to maintain precision in JSON.
        
        Args:
            v: List of Decimal values to serialize
            
        Returns:
            List of string representations of the Decimal values
        """
        return [str(x) for x in v]
