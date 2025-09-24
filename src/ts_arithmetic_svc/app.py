import decimal
from fastapi import FastAPI

# Set global decimal context precision for high precision arithmetic
decimal.getcontext().prec = 28

app = FastAPI(
    title="Arithmetic Service API",
    description="A high-precision arithmetic service using FastAPI.",
    version="1.0.0",
    debug=True
)


@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint for health checks.
    
    Returns:
        dict: A message indicating the service is running
    """
    return {"message": "Arithmetic Service is running"}

# add routers
