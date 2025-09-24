"""Unit tests for API Pydantic models."""

from decimal import Decimal
from typing import Any, Dict, List

import pytest
from pydantic import ValidationError

from ts_arithmetic_svc.api.models import (
    CalculationRequest,
    CalculationResponse,
    OperationType,
    MAX_ABS_OPERAND,
)


class TestOperationType:
    """Test cases for OperationType enum."""

    def test_operation_type_enum_values(self) -> None:
        """Test that OperationType enum has correct string values."""
        assert OperationType.ADD == "add"
        assert OperationType.SUBTRACT == "subtract"
        assert OperationType.MULTIPLY == "multiply"
        assert OperationType.DIVIDE == "divide"

    def test_operation_type_enum_membership(self) -> None:
        """Test that all expected operations are defined in enum."""
        expected_operations = {"add", "subtract", "multiply", "divide"}
        actual_operations = {op.value for op in OperationType}
        assert actual_operations == expected_operations

    def test_operation_type_invalid_construction(self) -> None:
        """Test that constructing OperationType with invalid value raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            OperationType("power")
        
        # Verify error message contains information about invalid value
        assert "power" in str(exc_info.value)


class TestCalculationRequest:
    """Test cases for CalculationRequest model."""

    def test_valid_calculation_request(self) -> None:
        """Test creating valid CalculationRequest instances."""
        # Test with each operation type
        test_cases = [
            (OperationType.ADD, Decimal("1.5"), Decimal("2.5")),
            (OperationType.SUBTRACT, Decimal("10"), Decimal("3")),
            (OperationType.MULTIPLY, Decimal("2.5"), Decimal("4")),
            (OperationType.DIVIDE, Decimal("8"), Decimal("2")),
        ]
        
        for operation, a, b in test_cases:
            request = CalculationRequest(operation=operation, a=a, b=b)
            assert request.operation == operation
            assert request.a == a
            assert request.b == b

    def test_calculation_request_with_string_operation(self) -> None:
        """Test that string operation values are correctly converted to enum."""
        request = CalculationRequest(
            operation="add", a=Decimal("1"), b=Decimal("2")
        )
        assert request.operation == OperationType.ADD
        assert isinstance(request.operation, OperationType)

    def test_calculation_request_invalid_operation(self) -> None:
        """Test that invalid operation raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            CalculationRequest(
                operation="invalid_op", a=Decimal("1"), b=Decimal("2")
            )
        
        errors = exc_info.value.errors()
        assert len(errors) == 1
        assert "operation" in errors[0]["loc"]

    def test_calculation_request_operand_boundary_values(self) -> None:
        """Test operands at boundary values (exactly at limits)."""
        # Test maximum positive values
        request = CalculationRequest(
            operation=OperationType.ADD,
            a=MAX_ABS_OPERAND,
            b=MAX_ABS_OPERAND
        )
        assert request.a == MAX_ABS_OPERAND
        assert request.b == MAX_ABS_OPERAND
        
        # Test maximum negative values
        request = CalculationRequest(
            operation=OperationType.SUBTRACT,
            a=-MAX_ABS_OPERAND,
            b=-MAX_ABS_OPERAND
        )
        assert request.a == -MAX_ABS_OPERAND
        assert request.b == -MAX_ABS_OPERAND

    def test_calculation_request_operand_out_of_range(self) -> None:
        """Test that operands outside valid range raise ValidationError."""
        # Test operand 'a' too large
        with pytest.raises(ValidationError) as exc_info:
            CalculationRequest(
                operation=OperationType.ADD,
                a=MAX_ABS_OPERAND + 1,
                b=Decimal("1")
            )
        
        errors = exc_info.value.errors()
        assert any("a" in error["loc"] for error in errors)
        
        # Test operand 'b' too small
        with pytest.raises(ValidationError) as exc_info:
            CalculationRequest(
                operation=OperationType.ADD,
                a=Decimal("1"),
                b=-MAX_ABS_OPERAND - 1
            )
        
        errors = exc_info.value.errors()
        assert any("b" in error["loc"] for error in errors)

    def test_calculation_request_operand_out_of_range_complete(self) -> None:
        """Test complete coverage of out-of-range operand validation."""
        # Test operand 'a' too small (negative direction)
        with pytest.raises(ValidationError) as exc_info:
            CalculationRequest(
                operation=OperationType.ADD,
                a=-MAX_ABS_OPERAND - 1,
                b=Decimal("1")
            )
        
        errors = exc_info.value.errors()
        assert any("a" in error["loc"] for error in errors)
        
        # Test operand 'b' too large (positive direction)
        with pytest.raises(ValidationError) as exc_info:
            CalculationRequest(
                operation=OperationType.ADD,
                a=Decimal("1"),
                b=MAX_ABS_OPERAND + 1
            )
        
        errors = exc_info.value.errors()
        assert any("b" in error["loc"] for error in errors)

    def test_calculation_request_invalid_operand_types(self) -> None:
        """Test that non-numeric string operands raise ValidationError."""
        # Test operand 'a' as non-numeric string
        with pytest.raises(ValidationError) as exc_info:
            CalculationRequest(
                operation=OperationType.ADD,
                a="invalid",  # type: ignore
                b=Decimal("5")
            )
        
        errors = exc_info.value.errors()
        assert any("a" in error["loc"] for error in errors)
        # Check for decimal parsing error type or relevant error message
        assert any(
            error.get("type") == "decimal_parsing" or
            "decimal" in error.get("msg", "").lower()
            for error in errors
        )
        
        # Test operand 'b' as non-numeric string
        with pytest.raises(ValidationError) as exc_info:
            CalculationRequest(
                operation=OperationType.ADD,
                a=Decimal("10"),
                b="invalid"  # type: ignore
            )
        
        errors = exc_info.value.errors()
        assert any("b" in error["loc"] for error in errors)
        # Check for decimal parsing error type or relevant error message
        assert any(
            error.get("type") == "decimal_parsing" or
            "decimal" in error.get("msg", "").lower()
            for error in errors
        )

    def test_calculation_request_decimal_conversion(self) -> None:
        """Test that numeric values are properly converted to Decimal."""
        # Test with int
        request = CalculationRequest(
            operation=OperationType.ADD, a=10, b=20
        )
        assert isinstance(request.a, Decimal)
        assert isinstance(request.b, Decimal)
        assert request.a == Decimal("10")
        assert request.b == Decimal("20")
        
        # Test with float (should work but may have precision issues)
        request = CalculationRequest(
            operation=OperationType.ADD, a=1.5, b=2.5
        )
        assert isinstance(request.a, Decimal)
        assert isinstance(request.b, Decimal)

    def test_calculation_request_missing_fields(self) -> None:
        """Test that missing required fields raise ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            CalculationRequest()  # type: ignore
        
        errors = exc_info.value.errors()
        required_fields = {"operation", "a", "b"}
        error_fields = {error["loc"][0] for error in errors}
        assert required_fields.issubset(error_fields)


class TestCalculationResponse:
    """Test cases for CalculationResponse model."""

    def test_valid_calculation_response(self) -> None:
        """Test creating valid CalculationResponse instances."""
        response = CalculationResponse(
            result=Decimal("4.0"),
            operation=OperationType.ADD,
            operands=[Decimal("1.5"), Decimal("2.5")]
        )
        
        assert response.result == Decimal("4.0")
        assert response.operation == OperationType.ADD
        assert response.operands == [Decimal("1.5"), Decimal("2.5")]

    def test_calculation_response_json_serialization(self) -> None:
        """Test that Decimal fields are serialized as strings in JSON."""
        response = CalculationResponse(
            result=Decimal("123.456789"),
            operation=OperationType.MULTIPLY,
            operands=[Decimal("12.34"), Decimal("10.01")]
        )
        
        # Test JSON serialization
        json_str = response.model_dump_json()
        
        # Parse back to verify string serialization
        import json
        parsed = json.loads(json_str)
        
        # Check that result is serialized as string
        assert isinstance(parsed["result"], str)
        assert parsed["result"] == "123.456789"
        
        # Check that operation remains as string
        assert isinstance(parsed["operation"], str)
        assert parsed["operation"] == "multiply"
        
        # Check that operands are serialized as list of strings
        assert isinstance(parsed["operands"], list)
        assert len(parsed["operands"]) == 2
        assert isinstance(parsed["operands"][0], str)
        assert isinstance(parsed["operands"][1], str)
        assert parsed["operands"][0] == "12.34"
        assert parsed["operands"][1] == "10.01"

    def test_calculation_response_model_dump_vs_json(self) -> None:
        """Test difference between regular model_dump and JSON serialization."""
        response = CalculationResponse(
            result=Decimal("5.5"),
            operation=OperationType.DIVIDE,
            operands=[Decimal("11"), Decimal("2")]
        )
        
        # Regular model dump should keep Decimal types
        regular_dump = response.model_dump()
        assert isinstance(regular_dump["result"], Decimal)
        assert isinstance(regular_dump["operands"][0], Decimal)
        
        # JSON dump should convert to strings
        json_dump = response.model_dump(mode="json")
        assert isinstance(json_dump["result"], str)
        assert isinstance(json_dump["operands"][0], str)

    def test_calculation_response_large_decimal_serialization(self) -> None:
        """Test JSON serialization with large Decimal values."""
        large_result = Decimal("999999999999999999.123456789")
        large_operands = [
            Decimal("-888888888888888888.987654321"),
            Decimal("777777777777777777.111111111")
        ]
        
        response = CalculationResponse(
            result=large_result,
            operation=OperationType.SUBTRACT,
            operands=large_operands
        )
        
        json_str = response.model_dump_json()
        
        import json
        parsed = json.loads(json_str)
        
        # Verify large numbers are preserved as strings
        assert parsed["result"] == str(large_result)
        assert parsed["operands"][0] == str(large_operands[0])
        assert parsed["operands"][1] == str(large_operands[1])

    def test_calculation_response_with_string_operation(self) -> None:
        """Test creating response with string operation value."""
        response = CalculationResponse(
            result=Decimal("6"),
            operation="multiply",  # type: ignore
            operands=[Decimal("2"), Decimal("3")]
        )
        
        assert response.operation == OperationType.MULTIPLY
        assert isinstance(response.operation, OperationType)

    def test_calculation_response_empty_operands_list(self) -> None:
        """Test response with empty operands list."""
        response = CalculationResponse(
            result=Decimal("0"),
            operation=OperationType.ADD,
            operands=[]
        )
        
        json_str = response.model_dump_json()
        import json
        parsed = json.loads(json_str)
        
        assert parsed["operands"] == []

    def test_calculation_response_missing_fields(self) -> None:
        """Test that missing required fields raise ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            CalculationResponse()  # type: ignore
        
        errors = exc_info.value.errors()
        required_fields = {"result", "operation", "operands"}
        error_fields = {error["loc"][0] for error in errors}
        assert required_fields.issubset(error_fields)


class TestModelIntegration:
    """Integration tests for model interactions."""

    def test_request_response_workflow(self) -> None:
        """Test typical request-response workflow."""
        # Create a request
        request = CalculationRequest(
            operation=OperationType.ADD,
            a=Decimal("3.14"),
            b=Decimal("2.86")
        )
        
        # Simulate calculation (would be done by service)
        result = request.a + request.b
        
        # Create response
        response = CalculationResponse(
            result=result,
            operation=request.operation,
            operands=[request.a, request.b]
        )
        
        # Verify the workflow
        assert response.result == Decimal("6.00")
        assert response.operation == OperationType.ADD
        assert len(response.operands) == 2
        
        # Verify JSON serialization works end-to-end
        json_output = response.model_dump_json()
        assert "6.00" in json_output
        assert "add" in json_output
        assert "3.14" in json_output
        assert "2.86" in json_output

    def test_max_abs_operand_constant(self) -> None:
        """Test that MAX_ABS_OPERAND constant is correctly defined."""
        assert MAX_ABS_OPERAND == Decimal("10000000000")  # 10^10
        
        # Verify it's used correctly in validation
        with pytest.raises(ValidationError):
            CalculationRequest(
                operation=OperationType.ADD,
                a=MAX_ABS_OPERAND + 1,
                b=Decimal("1")
            )
