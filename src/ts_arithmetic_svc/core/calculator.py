"""Core arithmetic calculation functions with high precision decimal support.

This module provides the fundamental arithmetic operations (add, subtract, multiply, divide)
using Python's decimal module for high precision calculations. Includes overflow detection
and division-by-zero handling.
"""

from decimal import Decimal

from ts_arithmetic_svc.exceptions import DivisionByZeroError, CalculationOverflowError
from ts_arithmetic_svc.api.models import MAX_ABS_OPERAND


def add(a: Decimal, b: Decimal) -> Decimal:
    """Add two decimal numbers with overflow detection.
    
    Args:
        a: First operand as Decimal
        b: Second operand as Decimal
        
    Returns:
        Decimal: Sum of a and b
        
    Raises:
        CalculationOverflowError: If result exceeds MAX_ABS_OPERAND range
    """
    result = a + b
    if abs(result) > MAX_ABS_OPERAND:
        raise CalculationOverflowError(detail="Calculation result exceeds supported range")
    return result


def subtract(a: Decimal, b: Decimal) -> Decimal:
    """Subtract two decimal numbers with overflow detection.
    
    Args:
        a: First operand as Decimal
        b: Second operand as Decimal
        
    Returns:
        Decimal: Difference of a and b
        
    Raises:
        CalculationOverflowError: If result exceeds MAX_ABS_OPERAND range
    """
    result = a - b
    if abs(result) > MAX_ABS_OPERAND:
        raise CalculationOverflowError(detail="Calculation result exceeds supported range")
    return result


def multiply(a: Decimal, b: Decimal) -> Decimal:
    """Multiply two decimal numbers with overflow detection.
    
    Args:
        a: First operand as Decimal
        b: Second operand as Decimal
        
    Returns:
        Decimal: Product of a and b
        
    Raises:
        CalculationOverflowError: If result exceeds MAX_ABS_OPERAND range
    """
    result = a * b
    if abs(result) > MAX_ABS_OPERAND:
        raise CalculationOverflowError(detail="Calculation result exceeds supported range")
    return result


def divide(a: Decimal, b: Decimal) -> Decimal:
    """Divide two decimal numbers with division-by-zero and overflow detection.
    
    Args:
        a: First operand as Decimal (dividend)
        b: Second operand as Decimal (divisor)
        
    Returns:
        Decimal: Quotient of a divided by b
        
    Raises:
        DivisionByZeroError: If b is exactly zero
        CalculationOverflowError: If result exceeds MAX_ABS_OPERAND range
    """
    if b == Decimal(0):
        raise DivisionByZeroError(detail="Division by zero is not allowed")
    
    result = a / b
    if abs(result) > MAX_ABS_OPERAND:
        raise CalculationOverflowError(detail="Calculation result exceeds supported range")
    return result
