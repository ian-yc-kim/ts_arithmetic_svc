# Arithmetic Service (ts_arithmetic_svc)

A high-precision arithmetic service built with FastAPI that provides REST API endpoints for basic arithmetic operations using Python's decimal module for accurate calculations.

## Prerequisites

- Python 3.11 or higher
- Poetry (Python dependency management tool)
  - Install via: `pipx install poetry` or follow the [official installation guide](https://python-poetry.org/docs/#installation)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd ts_arithmetic_svc
   ```

2. Install project dependencies using Poetry:
   ```bash
   poetry install
   ```

## Configuration (Optional)

The service can be configured using environment variables. Create a `.env` file in the project root:

```bash
# Service port (default: 8000)
SERVICE_PORT=8000

# Database URL (default: in-memory SQLite for development)
DATABASE_URL=sqlite:///:memory:
```

## Running the Application

### Primary Method
Start the FastAPI service using the Poetry script:
```bash
poetry run ts_arithmetic_svc
```

### Alternative Method
Run directly with uvicorn:
```bash
poetry run uvicorn ts_arithmetic_svc.app:app --host 0.0.0.0 --port 8000
```

### Default Configuration
- **Host:** 0.0.0.0 (accessible from all network interfaces)
- **Port:** 8000 (configurable via `SERVICE_PORT` environment variable)
- **Access URL:** http://0.0.0.0:8000

## API Endpoints

### Health Check / Root Endpoint

**GET /** 

**Purpose:** Service health check to verify the arithmetic service is running.

**Response Example:**
```json
{
  "message": "Arithmetic Service is running"
}
```

**Usage:**
```bash
curl http://0.0.0.0:8000/
```

### Calculate Endpoint

**POST /calculate**

**Purpose:** Perform high-precision arithmetic calculations (add, subtract, multiply, divide) using Python's Decimal module to preserve precision. Operands must be within the range of ±10^10.

**Request Body:**
- `operation`: One of ["add", "subtract", "multiply", "divide"]
- `a`: Decimal number (string or number), between -10000000000 and 10000000000
- `b`: Decimal number (string or number), between -10000000000 and 10000000000

**Responses:**
- **200 OK**: JSON object containing result, operation, and operands (all decimal values serialized as strings to preserve precision)
- **400 Bad Request**: For domain errors such as division by zero. Returns `{"detail": "..."}`
- **422 Unprocessable Entity**: Pydantic validation errors (e.g., operand out of range)

**Examples:**

#### 1. Successful Addition (HTTP 200)
```bash
curl -X POST \
  http://0.0.0.0:8000/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "add",
    "a": "1.25",
    "b": "2.75"
  }'
```

**Expected Response (HTTP 200):**
```json
{
  "result": "4.00",
  "operation": "add",
  "operands": ["1.25", "2.75"]
}
```

#### 2. Successful Division (HTTP 200)
```bash
curl -X POST \
  http://0.0.0.0:8000/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "divide",
    "a": "10",
    "b": "4"
  }'
```

**Expected Response (HTTP 200):**
```json
{
  "result": "2.5",
  "operation": "divide",
  "operands": ["10", "4"]
}
```

#### 3. Division by Zero Error (HTTP 400)
```bash
curl -X POST \
  http://0.0.0.0:8000/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "divide",
    "a": "5",
    "b": "0"
  }'
```

**Expected Response (HTTP 400):**
```json
{
  "detail": "Division by zero is not allowed"
}
```

#### 4. Operand Out of Range Error (HTTP 422)
```bash
# Here, operand 'a' exceeds the maximum allowed absolute value (10^10)
curl -X POST \
  http://0.0.0.0:8000/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "add",
    "a": "10000000001",
    "b": "1"
  }'
```

**Expected Response (HTTP 422):**
```json
{
  "detail": [
    {
      "type": "less_than_equal",
      "loc": ["body", "a"],
      "msg": "Input should be less than or equal to 10000000000",
      "input": "10000000001",
      "ctx": {"le": 10000000000}
    }
  ]
}
```

### API Documentation

Once the service is running, you can access:
- **Interactive API docs (Swagger UI):** http://0.0.0.0:8000/docs
- **Alternative API docs (ReDoc):** http://0.0.0.0:8000/redoc

> **Note:** Additional arithmetic operation endpoints (addition, subtraction, multiplication, division) will be added in subsequent development tasks.

## Development

### Running Tests
```bash
poetry run pytest
```

### Using Make Commands
The project includes a Makefile with common development tasks:
```bash
make build      # Install dependencies
make setup      # Run database migrations
make unittest   # Run tests
make run        # Start the service
```

## Project Structure

- `src/ts_arithmetic_svc/` - Main application source code
  - `app.py` - FastAPI application setup and configuration
  - `main.py` - Application entry point
  - `config.py` - Configuration management
- `tests/` - Unit tests
- `migrations/` - Database migration files (Alembic)

## Technology Stack

- **Framework:** FastAPI
- **ASGI Server:** Uvicorn
- **Build Tool:** Poetry
- **Database:** SQLAlchemy with PostgreSQL (SQLite for development)
- **Testing:** pytest
- **Precision Arithmetic:** Python's decimal module (28-digit precision)