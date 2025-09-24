import decimal
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from ts_arithmetic_svc.exceptions import ArithmeticServiceError
from ts_arithmetic_svc.routers import calculate_router

# Set global decimal context precision for high precision arithmetic
decimal.getcontext().prec = 28

app = FastAPI(
    title="Arithmetic Service API",
    description="A high-precision arithmetic service using FastAPI.",
    version="1.0.0",
    debug=True
)


@app.exception_handler(ArithmeticServiceError)
async def arithmetic_service_error_handler(
    request: Request, exc: ArithmeticServiceError
) -> JSONResponse:
    """Exception handler for ArithmeticServiceError.
    
    Args:
        request: The incoming request
        exc: The ArithmeticServiceError instance
        
    Returns:
        JSONResponse: Response with status code and detail from the exception
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint for health checks.
    
    Returns:
        dict: A message indicating the service is running
    """
    return {"message": "Arithmetic Service is running"}

# add routers
app.include_router(calculate_router)
