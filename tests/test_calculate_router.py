"""Unit tests for the calculate router endpoint."""

import pytest
from decimal import Decimal
from fastapi.testclient import TestClient
from unittest.mock import patch

from ts_arithmetic_svc.api.models import OperationType
from ts_arithmetic_svc.exceptions import (
    DivisionByZeroError,
    CalculationOverflowError,
    UnsupportedOperationError
)


class TestCalculateRouter:
    """Test class for the calculate router endpoint."""

    def test_calculate_add_success(self, client: TestClient) -> None:
        """Test successful addition operation.
        
        Args:
            client: TestClient fixture from conftest.py
        """
        request_data = {
            "operation": "add",
            "a": "10.5",
            "b": "5.25"
        }
        
        response = client.post("/calculate", json=request_data)
        
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["result"] == "15.75"
        assert response_data["operation"] == "add"
        assert response_data["operands"] == ["10.5", "5.25"]

    def test_calculate_subtract_success(self, client: TestClient) -> None:
        """Test successful subtraction operation.
        
        Args:
            client: TestClient fixture from conftest.py
        """
        request_data = {
            "operation": "subtract",
            "a": "10.5",
            "b": "3.25"
        }
        
        response = client.post("/calculate", json=request_data)
        
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["result"] == "7.25"
        assert response_data["operation"] == "subtract"
        assert response_data["operands"] == ["10.5", "3.25"]

    def test_calculate_multiply_success(self, client: TestClient) -> None:
        """Test successful multiplication operation.
        
        Args:
            client: TestClient fixture from conftest.py
        """
        request_data = {
            "operation": "multiply",
            "a": "4.0",
            "b": "2.5"
        }
        
        response = client.post("/calculate", json=request_data)
        
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["result"] == "10.00"  # Decimal precision: 4.0 * 2.5 = 10.00
        assert response_data["operation"] == "multiply"
        assert response_data["operands"] == ["4.0", "2.5"]

    def test_calculate_divide_success(self, client: TestClient) -> None:
        """Test successful division operation.
        
        Args:
            client: TestClient fixture from conftest.py
        """
        request_data = {
            "operation": "divide",
            "a": "10.0",
            "b": "2.0"
        }
        
        response = client.post("/calculate", json=request_data)
        
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["result"] == "5"  # Decimal precision: 10.0 / 2.0 = 5
        assert response_data["operation"] == "divide"
        assert response_data["operands"] == ["10.0", "2.0"]

    def test_calculate_division_by_zero_error(self, client: TestClient) -> None:
        """Test division by zero error handling.
        
        Args:
            client: TestClient fixture from conftest.py
        """
        request_data = {
            "operation": "divide",
            "a": "10.0",
            "b": "0.0"
        }
        
        response = client.post("/calculate", json=request_data)
        
        assert response.status_code == 400
        response_data = response.json()
        assert response_data["detail"] == "Division by zero is not allowed"

    @patch('ts_arithmetic_svc.api.routers.calculate.add')
    def test_calculate_overflow_error(self, mock_add, client: TestClient) -> None:
        """Test calculation overflow error handling.
        
        Args:
            mock_add: Mock for the add function
            client: TestClient fixture from conftest.py
        """
        # Mock the add function to raise CalculationOverflowError
        mock_add.side_effect = CalculationOverflowError()
        
        request_data = {
            "operation": "add",
            "a": "1.0",
            "b": "1.0"
        }
        
        response = client.post("/calculate", json=request_data)
        
        assert response.status_code == 400
        response_data = response.json()
        assert response_data["detail"] == "Calculation result exceeds supported range"

    def test_calculate_invalid_operation_pydantic_validation(self, client: TestClient) -> None:
        """Test invalid operation handled by Pydantic validation.
        
        Args:
            client: TestClient fixture from conftest.py
        """
        request_data = {
            "operation": "invalid_operation",
            "a": "10.0",
            "b": "5.0"
        }
        
        response = client.post("/calculate", json=request_data)
        
        # Pydantic validation should catch this before it reaches our handler
        assert response.status_code == 422

    def test_calculate_missing_required_fields(self, client: TestClient) -> None:
        """Test missing required fields in request.
        
        Args:
            client: TestClient fixture from conftest.py
        """
        request_data = {
            "operation": "add",
            "a": "10.0"
            # missing 'b' field
        }
        
        response = client.post("/calculate", json=request_data)
        
        # Pydantic validation should catch this
        assert response.status_code == 422

    def test_calculate_invalid_operand_type(self, client: TestClient) -> None:
        """Test invalid operand type in request.
        
        Args:
            client: TestClient fixture from conftest.py
        """
        request_data = {
            "operation": "add",
            "a": "not_a_number",
            "b": "5.0"
        }
        
        response = client.post("/calculate", json=request_data)
        
        # Pydantic validation should catch this
        assert response.status_code == 422

    def test_calculate_operand_out_of_range(self, client: TestClient) -> None:
        """Test operand value exceeding allowed range.
        
        Args:
            client: TestClient fixture from conftest.py
        """
        # MAX_ABS_OPERAND is 10^10
        request_data = {
            "operation": "add",
            "a": "99999999999",  # > 10^10
            "b": "5.0"
        }
        
        response = client.post("/calculate", json=request_data)
        
        # Pydantic validation should catch this
        assert response.status_code == 422

    def test_calculate_negative_operands(self, client: TestClient) -> None:
        """Test calculation with negative operands.
        
        Args:
            client: TestClient fixture from conftest.py
        """
        request_data = {
            "operation": "add",
            "a": "-10.5",
            "b": "5.25"
        }
        
        response = client.post("/calculate", json=request_data)
        
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["result"] == "-5.25"
        assert response_data["operation"] == "add"
        assert response_data["operands"] == ["-10.5", "5.25"]

    def test_calculate_zero_operands(self, client: TestClient) -> None:
        """Test calculation with zero operands.
        
        Args:
            client: TestClient fixture from conftest.py
        """
        request_data = {
            "operation": "multiply",
            "a": "0.0",
            "b": "5.25"
        }
        
        response = client.post("/calculate", json=request_data)
        
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["result"] == "0.000"  # Decimal precision: 0.0 * 5.25 = 0.000
        assert response_data["operation"] == "multiply"
        assert response_data["operands"] == ["0.0", "5.25"]

    @patch('ts_arithmetic_svc.api.routers.calculate.add')
    def test_calculate_unexpected_error(self, mock_add, client: TestClient) -> None:
        """Test unexpected error handling.
        
        Args:
            mock_add: Mock for the add function
            client: TestClient fixture from conftest.py
        """
        # Mock the add function to raise an unexpected error
        mock_add.side_effect = RuntimeError("Unexpected error")
        
        request_data = {
            "operation": "add",
            "a": "1.0",
            "b": "1.0"
        }
        
        response = client.post("/calculate", json=request_data)
        
        assert response.status_code == 400
        response_data = response.json()
        assert response_data["detail"] == "An unexpected error occurred during calculation"

    def test_calculate_high_precision_decimals(self, client: TestClient) -> None:
        """Test calculation with high precision decimal values.
        
        Args:
            client: TestClient fixture from conftest.py
        """
        request_data = {
            "operation": "add",
            "a": "1.123456789012345678901234567890",
            "b": "2.987654321098765432109876543210"
        }
        
        response = client.post("/calculate", json=request_data)
        
        assert response.status_code == 200
        response_data = response.json()
        # Result should maintain precision
        expected_result = str(Decimal("1.123456789012345678901234567890") + 
                            Decimal("2.987654321098765432109876543210"))
        assert response_data["result"] == expected_result
        assert response_data["operation"] == "add"
        assert response_data["operands"] == ["1.123456789012345678901234567890", "2.987654321098765432109876543210"]
