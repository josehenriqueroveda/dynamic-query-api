from core.config import settings
from core.security import request_limiter
from fastapi import APIRouter
from fastapi import FastAPI
from fastapi import Request
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from starlette.middleware.cors import CORSMiddleware
from uvicorn import run


limiter = request_limiter.get_limiter()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    version=settings.VERSION,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


api_router = APIRouter()
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/", tags=["Monitoring"])
@limiter.limit("60/minute")
async def health_check(request: Request):
    return {"status": "ok"}


if __name__ == "__main__":
    print(
        r"""
    """
    )
    port = settings.API_PORT
    run(app, host="0.0.0.0", port=port)
