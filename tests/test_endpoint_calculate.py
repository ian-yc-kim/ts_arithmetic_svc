"""Comprehensive unit and integration tests for the POST /calculate endpoint.

This module contains comprehensive tests covering:
- All arithmetic operations with successful scenarios
- Division by zero error handling
- Real calculation overflow scenarios (not mocked)
- Invalid operation type validation
- Operand range violations
- Malformed JSON request handling
- Concurrency testing for robust parallel request handling
"""

import json
import concurrent.futures
from decimal import Decimal
from typing import Dict, Any, List

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from ts_arithmetic_svc.api.models import (
    OperationType,
    CalculationRequest, 
    CalculationResponse,
    MAX_ABS_OPERAND
)
from ts_arithmetic_svc.app import app


class TestCalculateEndpointSuccess:
    """Test successful calculation scenarios for all operations."""

    def test_calculate_add_success_endpoint(self, client: TestClient) -> None:
        """Test successful addition operation via endpoint.
        
        Verifies:
        - HTTP status code 200
        - Correct result, operation, and operands in response
        - Decimal values serialized as strings in JSON
        """
        request_data = {
            "operation": "add",
            "a": "12.75",
            "b": "8.25"
        }
        
        response = client.post("/calculate", json=request_data)
        
        # Verify response status and structure
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        
        # Verify response fields and types
        assert isinstance(response_data, dict)
        assert "result" in response_data
        assert "operation" in response_data
        assert "operands" in response_data
        
        # Verify calculation correctness
        expected_result = str(Decimal("12.75") + Decimal("8.25"))
        assert response_data["result"] == expected_result
        assert response_data["operation"] == "add"
        assert response_data["operands"] == ["12.75", "8.25"]
        
        # Verify Decimal serialization as strings
        assert isinstance(response_data["result"], str)
        assert isinstance(response_data["operands"], list)
        assert all(isinstance(op, str) for op in response_data["operands"])

    def test_calculate_subtract_success_endpoint(self, client: TestClient) -> None:
        """Test successful subtraction operation via endpoint.
        
        Verifies:
        - HTTP status code 200
        - Correct result, operation, and operands in response
        - Decimal values serialized as strings in JSON
        """
        request_data = {
            "operation": "subtract", 
            "a": "15.5",
            "b": "6.25"
        }
        
        response = client.post("/calculate", json=request_data)
        
        # Verify response status and structure
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        
        # Verify calculation correctness
        expected_result = str(Decimal("15.5") - Decimal("6.25"))
        assert response_data["result"] == expected_result
        assert response_data["operation"] == "subtract"
        assert response_data["operands"] == ["15.5", "6.25"]
        
        # Verify Decimal serialization as strings
        assert isinstance(response_data["result"], str)
        assert all(isinstance(op, str) for op in response_data["operands"])

    def test_calculate_multiply_success_endpoint(self, client: TestClient) -> None:
        """Test successful multiplication operation via endpoint.
        
        Verifies:
        - HTTP status code 200
        - Correct result, operation, and operands in response
        - Decimal values serialized as strings in JSON
        """
        request_data = {
            "operation": "multiply",
            "a": "4.5",
            "b": "3.2"
        }
        
        response = client.post("/calculate", json=request_data)
        
        # Verify response status and structure
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        
        # Verify calculation correctness
        expected_result = str(Decimal("4.5") * Decimal("3.2"))
        assert response_data["result"] == expected_result
        assert response_data["operation"] == "multiply"
        assert response_data["operands"] == ["4.5", "3.2"]
        
        # Verify Decimal serialization as strings
        assert isinstance(response_data["result"], str)
        assert all(isinstance(op, str) for op in response_data["operands"])

    def test_calculate_divide_success_endpoint(self, client: TestClient) -> None:
        """Test successful division operation via endpoint.
        
        Verifies:
        - HTTP status code 200
        - Correct result, operation, and operands in response
        - Decimal values serialized as strings in JSON
        """
        request_data = {
            "operation": "divide",
            "a": "15.0",
            "b": "3.0"
        }
        
        response = client.post("/calculate", json=request_data)
        
        # Verify response status and structure
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        
        # Verify calculation correctness
        expected_result = str(Decimal("15.0") / Decimal("3.0"))
        assert response_data["result"] == expected_result
        assert response_data["operation"] == "divide"
        assert response_data["operands"] == ["15.0", "3.0"]
        
        # Verify Decimal serialization as strings
        assert isinstance(response_data["result"], str)
        assert all(isinstance(op, str) for op in response_data["operands"])


class TestCalculateEndpointErrors:
    """Test error handling scenarios for the calculate endpoint."""

    def test_calculate_division_by_zero_endpoint(self, client: TestClient) -> None:
        """Test division by zero error handling.
        
        Verifies:
        - HTTP status code 400
        - Exact error detail message
        """
        request_data = {
            "operation": "divide",
            "a": "8",
            "b": "0"
        }
        
        response = client.post("/calculate", json=request_data)
        
        # Verify error response
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        response_data = response.json()
        assert response_data["detail"] == "Division by zero is not allowed"

    def test_calculate_overflow_add_endpoint(self, client: TestClient) -> None:
        """Test addition overflow with real operands (not mocked).
        
        Uses actual operands that cause overflow: MAX_ABS_OPERAND + 1
        
        Verifies:
        - HTTP status code 400
        - Exact overflow error detail message
        """
        request_data = {
            "operation": "add",
            "a": str(MAX_ABS_OPERAND),
            "b": "1"
        }
        
        response = client.post("/calculate", json=request_data)
        
        # Verify overflow error response
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        response_data = response.json()
        assert response_data["detail"] == "Calculation result exceeds supported range"

    def test_calculate_overflow_multiply_endpoint(self, client: TestClient) -> None:
        """Test multiplication overflow with real operands (not mocked).
        
        Uses actual operands that cause overflow: MAX_ABS_OPERAND * 1.0000000001
        
        Verifies:
        - HTTP status code 400
        - Exact overflow error detail message
        """
        request_data = {
            "operation": "multiply",
            "a": str(MAX_ABS_OPERAND),
            "b": "1.0000000001"
        }
        
        response = client.post("/calculate", json=request_data)
        
        # Verify overflow error response
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        response_data = response.json()
        assert response_data["detail"] == "Calculation result exceeds supported range"

    def test_calculate_overflow_divide_endpoint(self, client: TestClient) -> None:
        """Test division overflow with real operands (not mocked).
        
        Uses actual operands that cause overflow: MAX_ABS_OPERAND / 0.9999999999
        
        Verifies:
        - HTTP status code 400
        - Exact overflow error detail message
        """
        request_data = {
            "operation": "divide",
            "a": str(MAX_ABS_OPERAND),
            "b": "0.9999999999"
        }
        
        response = client.post("/calculate", json=request_data)
        
        # Verify overflow error response
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        response_data = response.json()
        assert response_data["detail"] == "Calculation result exceeds supported range"

    def test_calculate_invalid_operation_type_422(self, client: TestClient) -> None:
        """Test invalid operation type validation.
        
        Uses operation type not present in OperationType enum.
        
        Verifies:
        - HTTP status code 422 (Unprocessable Entity)
        - Pydantic validation error response structure
        """
        request_data = {
            "operation": "power",  # Not in OperationType enum
            "a": "2",
            "b": "3"
        }
        
        response = client.post("/calculate", json=request_data)
        
        # Verify Pydantic validation error
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        response_data = response.json()
        
        # Verify error structure (Pydantic validation error format)
        assert "detail" in response_data
        assert isinstance(response_data["detail"], list)
        assert len(response_data["detail"]) > 0
        
        # Verify the error relates to the operation field
        operation_error = next(
            (error for error in response_data["detail"] 
             if "operation" in str(error.get("loc", []))), 
            None
        )
        assert operation_error is not None

    def test_calculate_operand_range_violation_a_too_large_422(self, client: TestClient) -> None:
        """Test operand 'a' exceeding maximum allowed range.
        
        Verifies:
        - HTTP status code 422 (Unprocessable Entity)
        - Pydantic validation error for operand 'a'
        """
        request_data = {
            "operation": "add",
            "a": str(MAX_ABS_OPERAND + 1),  # Exceeds maximum
            "b": "1"
        }
        
        response = client.post("/calculate", json=request_data)
        
        # Verify Pydantic validation error
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        response_data = response.json()
        
        # Verify error structure and operand 'a' validation
        assert "detail" in response_data
        assert isinstance(response_data["detail"], list)
        
        # Check that error relates to operand 'a'
        a_error = next(
            (error for error in response_data["detail"] 
             if "a" in str(error.get("loc", []))), 
            None
        )
        assert a_error is not None

    def test_calculate_operand_range_violation_b_too_small_422(self, client: TestClient) -> None:
        """Test operand 'b' below minimum allowed range.
        
        Verifies:
        - HTTP status code 422 (Unprocessable Entity)
        - Pydantic validation error for operand 'b'
        """
        request_data = {
            "operation": "add",
            "a": "1",
            "b": str(-MAX_ABS_OPERAND - 1)  # Below minimum
        }
        
        response = client.post("/calculate", json=request_data)
        
        # Verify Pydantic validation error
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        response_data = response.json()
        
        # Verify error structure and operand 'b' validation
        assert "detail" in response_data
        assert isinstance(response_data["detail"], list)
        
        # Check that error relates to operand 'b'
        b_error = next(
            (error for error in response_data["detail"] 
             if "b" in str(error.get("loc", []))), 
            None
        )
        assert b_error is not None

    def test_calculate_malformed_json_body(self, client: TestClient) -> None:
        """Test malformed JSON request body handling.
        
        Sends invalid JSON string and verifies appropriate error response.
        
        Verifies:
        - HTTP status code 400 or 422 (depending on FastAPI/Pydantic version)
        - JSON response with 'detail' field
        """
        # Send malformed JSON as raw data with correct content type
        malformed_json = '{"operation": "add", "a": "1", "b":}'
        
        response = client.post(
            "/calculate",
            data=malformed_json,
            headers={"Content-Type": "application/json"}
        )
        
        # FastAPI/Pydantic may return either 400 or 422 for malformed JSON
        assert response.status_code in {status.HTTP_400_BAD_REQUEST, status.HTTP_422_UNPROCESSABLE_ENTITY}
        
        response_data = response.json()
        
        # Verify response has error detail structure
        assert isinstance(response_data, dict)
        assert "detail" in response_data
        assert response_data["detail"] is not None


class TestCalculateEndpointConcurrency:
    """Test concurrent request handling for the calculate endpoint."""

    def test_calculate_concurrent_requests(self, client: TestClient) -> None:
        """Test concurrent requests to ensure robust parallel handling.
        
        Uses ThreadPoolExecutor to simulate multiple concurrent requests
        across various operations with valid operands.
        
        Verifies:
        - All requests are processed correctly and independently
        - No data corruption or unexpected errors occur
        - Each response is validated for correctness
        """
        def make_request(request_data: Dict[str, Any]) -> Dict[str, Any]:
            """Make a single request and return response data with request info.
            
            Args:
                request_data: The request payload
                
            Returns:
                Dict containing response data and original request for validation
            """
            response = client.post("/calculate", json=request_data)
            return {
                "status_code": response.status_code,
                "response_data": response.json(),
                "request_data": request_data
            }
        
        # Define various test scenarios for concurrent execution
        test_scenarios = [
            {"operation": "add", "a": "10.5", "b": "5.25"},
            {"operation": "subtract", "a": "20.0", "b": "8.5"},
            {"operation": "multiply", "a": "3.5", "b": "4.0"},
            {"operation": "divide", "a": "15.0", "b": "3.0"},
            {"operation": "add", "a": "100.123", "b": "200.456"},
            {"operation": "subtract", "a": "500.0", "b": "250.75"},
            {"operation": "multiply", "a": "7.5", "b": "8.0"},
            {"operation": "divide", "a": "24.0", "b": "6.0"},
            {"operation": "add", "a": "0.1", "b": "0.2"},
            {"operation": "subtract", "a": "1.0", "b": "0.9"},
            {"operation": "multiply", "a": "12.5", "b": "2.5"},
            {"operation": "divide", "a": "50.0", "b": "10.0"},
            {"operation": "add", "a": "-5.5", "b": "3.25"},
            {"operation": "subtract", "a": "-10.0", "b": "-5.0"},
            {"operation": "multiply", "a": "-2.5", "b": "4.0"},
            {"operation": "divide", "a": "-20.0", "b": "-4.0"},
            {"operation": "add", "a": "999.999", "b": "0.001"},
            {"operation": "subtract", "a": "1000.0", "b": "999.999"},
            {"operation": "multiply", "a": "1.5", "b": "1.5"},
            {"operation": "divide", "a": "9.0", "b": "3.0"}
        ]
        
        # Execute requests concurrently using ThreadPoolExecutor
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            # Submit all requests concurrently
            future_to_request = {
                executor.submit(make_request, scenario): scenario 
                for scenario in test_scenarios
            }
            
            # Collect results as they complete
            results = []
            for future in concurrent.futures.as_completed(future_to_request):
                original_request = future_to_request[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as exc:
                    pytest.fail(f"Request {original_request} generated exception: {exc}")
        
        # Verify all requests completed successfully
        assert len(results) == len(test_scenarios)
        
        # Validate each result individually
        for result in results:
            status_code = result["status_code"]
            response_data = result["response_data"]
            request_data = result["request_data"]
            
            # All test scenarios should succeed (no division by zero or overflow)
            assert status_code == status.HTTP_200_OK, f"Request {request_data} failed with status {status_code}"
            
            # Verify response structure
            assert "result" in response_data
            assert "operation" in response_data
            assert "operands" in response_data
            
            # Verify operation matches request
            assert response_data["operation"] == request_data["operation"]
            
            # Verify operands match request
            expected_operands = [request_data["a"], request_data["b"]]
            assert response_data["operands"] == expected_operands
            
            # Verify result is a string (Decimal serialization)
            assert isinstance(response_data["result"], str)
            
            # Verify calculation correctness by recomputing expected result
            a = Decimal(request_data["a"])
            b = Decimal(request_data["b"])
            operation = request_data["operation"]
            
            if operation == "add":
                expected_result = str(a + b)
            elif operation == "subtract":
                expected_result = str(a - b)
            elif operation == "multiply":
                expected_result = str(a * b)
            elif operation == "divide":
                expected_result = str(a / b)
            else:
                pytest.fail(f"Unexpected operation: {operation}")
            
            assert response_data["result"] == expected_result, (
                f"Incorrect result for {operation}({a}, {b}): "
                f"expected {expected_result}, got {response_data['result']}"
            )
