"""Unit tests for core arithmetic calculation functions.

This module contains comprehensive tests for the calculator functions including:
- Basic arithmetic operations
- Decimal precision maintenance
- Division by zero detection
- Overflow condition handling
- Boundary and edge case testing
"""

import pytest
from decimal import Decimal

from ts_arithmetic_svc.core.calculator import add, subtract, multiply, divide
from ts_arithmetic_svc.exceptions import DivisionByZeroError, CalculationOverflowError
from ts_arithmetic_svc.api.models import MAX_ABS_OPERAND


class TestBasicOperations:
    """Test basic arithmetic operations with various input combinations."""
    
    @pytest.mark.parametrize("a, b, expected", [
        (Decimal('10'), Decimal('5'), Decimal('15')),
        (Decimal('-10'), Decimal('5'), Decimal('-5')),
        (Decimal('10'), Decimal('-5'), Decimal('5')),
        (Decimal('-10'), Decimal('-5'), Decimal('-15')),
        (Decimal('0'), Decimal('0'), Decimal('0')),
        (Decimal('0'), Decimal('100'), Decimal('100')),
        (Decimal('100'), Decimal('0'), Decimal('100')),
        (Decimal('123.456'), Decimal('789.012'), Decimal('912.468')),
    ])
    def test_add(self, a, b, expected):
        """Test addition with various decimal inputs."""
        result = add(a, b)
        assert result == expected
        assert isinstance(result, Decimal)
    
    @pytest.mark.parametrize("a, b, expected", [
        (Decimal('10'), Decimal('5'), Decimal('5')),
        (Decimal('-10'), Decimal('5'), Decimal('-15')),
        (Decimal('10'), Decimal('-5'), Decimal('15')),
        (Decimal('-10'), Decimal('-5'), Decimal('-5')),
        (Decimal('0'), Decimal('0'), Decimal('0')),
        (Decimal('0'), Decimal('100'), Decimal('-100')),
        (Decimal('100'), Decimal('0'), Decimal('100')),
        (Decimal('789.012'), Decimal('123.456'), Decimal('665.556')),
    ])
    def test_subtract(self, a, b, expected):
        """Test subtraction with various decimal inputs."""
        result = subtract(a, b)
        assert result == expected
        assert isinstance(result, Decimal)
    
    @pytest.mark.parametrize("a, b, expected", [
        (Decimal('10'), Decimal('5'), Decimal('50')),
        (Decimal('-10'), Decimal('5'), Decimal('-50')),
        (Decimal('10'), Decimal('-5'), Decimal('-50')),
        (Decimal('-10'), Decimal('-5'), Decimal('50')),
        (Decimal('0'), Decimal('100'), Decimal('0')),
        (Decimal('100'), Decimal('0'), Decimal('0')),
        (Decimal('1.5'), Decimal('2.5'), Decimal('3.75')),
        (Decimal('12.34'), Decimal('5.67'), Decimal('69.9678')),
    ])
    def test_multiply(self, a, b, expected):
        """Test multiplication with various decimal inputs."""
        result = multiply(a, b)
        assert result == expected
        assert isinstance(result, Decimal)
    
    @pytest.mark.parametrize("a, b, expected", [
        (Decimal('10'), Decimal('5'), Decimal('2')),
        (Decimal('-10'), Decimal('5'), Decimal('-2')),
        (Decimal('10'), Decimal('-5'), Decimal('-2')),
        (Decimal('-10'), Decimal('-5'), Decimal('2')),
        (Decimal('0'), Decimal('100'), Decimal('0')),
        (Decimal('15'), Decimal('3'), Decimal('5')),
        (Decimal('7.5'), Decimal('2.5'), Decimal('3')),
        (Decimal('22'), Decimal('7'), Decimal('3.142857142857142857142857143')),
    ])
    def test_divide(self, a, b, expected):
        """Test division with various decimal inputs."""
        result = divide(a, b)
        assert result == expected
        assert isinstance(result, Decimal)


class TestDecimalPrecision:
    """Test decimal precision maintenance in calculations."""
    
    def test_add_decimal_precision(self):
        """Test that addition maintains decimal precision without float artifacts."""
        result = add(Decimal('0.1'), Decimal('0.2'))
        assert result == Decimal('0.3')
        # Verify this is NOT equal to the float result which would be imprecise
        assert result != Decimal(str(0.1 + 0.2))
    
    def test_subtract_decimal_precision(self):
        """Test that subtraction maintains decimal precision."""
        result = subtract(Decimal('1.0'), Decimal('0.9'))
        assert result == Decimal('0.1')
        assert result != Decimal(str(1.0 - 0.9))
    
    def test_multiply_decimal_precision(self):
        """Test that multiplication maintains decimal precision."""
        result = multiply(Decimal('0.1'), Decimal('0.1'))
        assert result == Decimal('0.01')
        assert result != Decimal(str(0.1 * 0.1))
    
    def test_divide_decimal_precision(self):
        """Test that division maintains decimal precision."""
        result = divide(Decimal('1'), Decimal('3'))
        # Should maintain high precision, not float precision
        expected = Decimal('0.3333333333333333333333333333')
        assert result == expected
        assert str(result).count('3') > 10  # Verify high precision


class TestDivisionByZero:
    """Test division by zero detection and error handling."""
    
    def test_divide_by_zero_positive(self):
        """Test division by zero with positive dividend."""
        with pytest.raises(DivisionByZeroError) as exc_info:
            divide(Decimal('1'), Decimal('0'))
        assert exc_info.value.detail == "Division by zero is not allowed"
    
    def test_divide_by_zero_negative(self):
        """Test division by zero with negative dividend."""
        with pytest.raises(DivisionByZeroError) as exc_info:
            divide(Decimal('-10'), Decimal('0'))
        assert exc_info.value.detail == "Division by zero is not allowed"
    
    def test_divide_zero_by_zero(self):
        """Test division of zero by zero."""
        with pytest.raises(DivisionByZeroError) as exc_info:
            divide(Decimal('0'), Decimal('0'))
        assert exc_info.value.detail == "Division by zero is not allowed"
    
    def test_divide_by_exact_zero_string(self):
        """Test division by zero created from string."""
        with pytest.raises(DivisionByZeroError) as exc_info:
            divide(Decimal('5'), Decimal('0.0'))
        assert exc_info.value.detail == "Division by zero is not allowed"


class TestCalculationOverflow:
    """Test overflow condition detection for results exceeding MAX_ABS_OPERAND."""
    
    def test_add_overflow_positive(self):
        """Test addition overflow with positive result just above limit."""
        overflow_value = MAX_ABS_OPERAND + Decimal('1')
        with pytest.raises(CalculationOverflowError) as exc_info:
            add(overflow_value, Decimal('0'))
        assert exc_info.value.detail == "Calculation result exceeds supported range"
    
    def test_add_overflow_negative(self):
        """Test addition overflow with negative result just below limit."""
        overflow_value = -MAX_ABS_OPERAND - Decimal('1')
        with pytest.raises(CalculationOverflowError) as exc_info:
            add(overflow_value, Decimal('0'))
        assert exc_info.value.detail == "Calculation result exceeds supported range"
    
    def test_subtract_overflow_positive(self):
        """Test subtraction overflow with positive result."""
        large_positive = MAX_ABS_OPERAND
        large_negative = -Decimal('1')
        with pytest.raises(CalculationOverflowError) as exc_info:
            subtract(large_positive, large_negative)
        assert exc_info.value.detail == "Calculation result exceeds supported range"
    
    def test_subtract_overflow_negative(self):
        """Test subtraction overflow with negative result."""
        large_negative = -MAX_ABS_OPERAND
        large_positive = Decimal('1')
        with pytest.raises(CalculationOverflowError) as exc_info:
            subtract(large_negative, large_positive)
        assert exc_info.value.detail == "Calculation result exceeds supported range"
    
    def test_multiply_overflow_positive(self):
        """Test multiplication overflow with positive result."""
        multiplier = Decimal('1.000000000000000000000000001')
        with pytest.raises(CalculationOverflowError) as exc_info:
            multiply(MAX_ABS_OPERAND, multiplier)
        assert exc_info.value.detail == "Calculation result exceeds supported range"
    
    def test_multiply_overflow_negative(self):
        """Test multiplication overflow with negative result."""
        multiplier = Decimal('-1.000000000000000000000000001')
        with pytest.raises(CalculationOverflowError) as exc_info:
            multiply(MAX_ABS_OPERAND, multiplier)
        assert exc_info.value.detail == "Calculation result exceeds supported range"
    
    def test_divide_overflow_positive(self):
        """Test division overflow with positive result."""
        small_divisor = Decimal('0.999999999999999999999999999')
        with pytest.raises(CalculationOverflowError) as exc_info:
            divide(MAX_ABS_OPERAND, small_divisor)
        assert exc_info.value.detail == "Calculation result exceeds supported range"
    
    def test_divide_overflow_negative(self):
        """Test division overflow with negative result."""
        small_negative_divisor = Decimal('-0.999999999999999999999999999')
        with pytest.raises(CalculationOverflowError) as exc_info:
            divide(MAX_ABS_OPERAND, small_negative_divisor)
        assert exc_info.value.detail == "Calculation result exceeds supported range"


class TestBoundaryConditions:
    """Test boundary conditions at exactly MAX_ABS_OPERAND limits."""
    
    def test_add_at_positive_boundary(self):
        """Test addition result exactly at positive MAX_ABS_OPERAND."""
        result = add(MAX_ABS_OPERAND, Decimal('0'))
        assert result == MAX_ABS_OPERAND
        assert isinstance(result, Decimal)
    
    def test_add_at_negative_boundary(self):
        """Test addition result exactly at negative MAX_ABS_OPERAND."""
        result = add(-MAX_ABS_OPERAND, Decimal('0'))
        assert result == -MAX_ABS_OPERAND
        assert isinstance(result, Decimal)
    
    def test_subtract_at_positive_boundary(self):
        """Test subtraction result exactly at positive MAX_ABS_OPERAND."""
        result = subtract(MAX_ABS_OPERAND, Decimal('0'))
        assert result == MAX_ABS_OPERAND
        assert isinstance(result, Decimal)
    
    def test_subtract_at_negative_boundary(self):
        """Test subtraction result exactly at negative MAX_ABS_OPERAND."""
        result = subtract(-MAX_ABS_OPERAND, Decimal('0'))
        assert result == -MAX_ABS_OPERAND
        assert isinstance(result, Decimal)
    
    def test_multiply_at_positive_boundary(self):
        """Test multiplication result exactly at positive MAX_ABS_OPERAND."""
        result = multiply(MAX_ABS_OPERAND, Decimal('1'))
        assert result == MAX_ABS_OPERAND
        assert isinstance(result, Decimal)
    
    def test_multiply_at_negative_boundary(self):
        """Test multiplication result exactly at negative MAX_ABS_OPERAND."""
        result = multiply(MAX_ABS_OPERAND, Decimal('-1'))
        assert result == -MAX_ABS_OPERAND
        assert isinstance(result, Decimal)
    
    def test_divide_at_positive_boundary(self):
        """Test division result exactly at positive MAX_ABS_OPERAND."""
        result = divide(MAX_ABS_OPERAND, Decimal('1'))
        assert result == MAX_ABS_OPERAND
        assert isinstance(result, Decimal)
    
    def test_divide_at_negative_boundary(self):
        """Test division result exactly at negative MAX_ABS_OPERAND."""
        result = divide(MAX_ABS_OPERAND, Decimal('-1'))
        assert result == -MAX_ABS_OPERAND
        assert isinstance(result, Decimal)


class TestEdgeCases:
    """Test edge cases with very small and very large numbers."""
    
    def test_very_small_numbers(self):
        """Test operations with very small decimal numbers."""
        tiny = Decimal('1e-25')
        result = add(tiny, tiny)
        assert result == Decimal('2e-25')
        
        result = multiply(tiny, Decimal('2'))
        assert result == Decimal('2e-25')
    
    def test_large_numbers_within_limit(self):
        """Test operations with large numbers that stay within limits."""
        large = MAX_ABS_OPERAND - Decimal('1')
        
        result = add(large, Decimal('1'))
        assert result == MAX_ABS_OPERAND
        
        result = subtract(large, Decimal('-1'))
        assert result == MAX_ABS_OPERAND
    
    def test_precision_with_many_decimals(self):
        """Test operations maintaining precision with many decimal places."""
        precise_a = Decimal('123.123456789012345678901234567')
        precise_b = Decimal('456.987654321098765432109876543')
        
        result = add(precise_a, precise_b)
        expected = Decimal('580.1111111101111111110111111')
        assert result == expected
    
    def test_zero_operations(self):
        """Test various operations involving zero."""
        # Zero with itself
        assert add(Decimal('0'), Decimal('0')) == Decimal('0')
        assert subtract(Decimal('0'), Decimal('0')) == Decimal('0')
        assert multiply(Decimal('0'), Decimal('0')) == Decimal('0')
        
        # Zero with large numbers
        large = MAX_ABS_OPERAND / Decimal('2')
        assert add(Decimal('0'), large) == large
        assert subtract(large, large) == Decimal('0')
        assert multiply(Decimal('0'), large) == Decimal('0')
        assert divide(Decimal('0'), large) == Decimal('0')
    
    def test_one_operations(self):
        """Test operations with one as operand."""
        test_value = Decimal('42.42')
        
        assert add(test_value, Decimal('0')) == test_value
        assert subtract(test_value, Decimal('0')) == test_value
        assert multiply(test_value, Decimal('1')) == test_value
        assert divide(test_value, Decimal('1')) == test_value
