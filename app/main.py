from fastapi import APIRouter
from fastapi import FastAPI
from fastapi import Request
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from starlette.middleware.cors import CORSMiddleware

from app.api.routes.v1.auth_route import auth_route
from app.api.routes.v1.user_route import user_route
from app.api.routes.v1.query_route import query_route
from app.core.config import settings
from app.core.security import request_limiter


print(
    r"""
 ██████╗ ██╗   ██╗███████╗██████╗ ██╗   ██╗      █████╗ ██████╗ ██╗
██╔═══██╗██║   ██║██╔════╝██╔══██╗╚██╗ ██╔╝     ██╔══██╗██╔══██╗██║
██║   ██║██║   ██║█████╗  ██████╔╝ ╚████╔╝█████╗███████║██████╔╝██║
██║▄▄ ██║██║   ██║██╔══╝  ██╔══██╗  ╚██╔╝ ╚════╝██╔══██║██╔═══╝ ██║
╚██████╔╝╚██████╔╝███████╗██║  ██║   ██║        ██║  ██║██║     ██║
 ╚══▀▀═╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝   ╚═╝        ╚═╝  ╚═╝╚═╝     ╚═╝
    
 developed by @josehenriqueroveda
    """
)

limiter = request_limiter.get_limiter()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description=settings.DESCRIPTION,
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
api_router.include_router(auth_route, tags=["Authentication"])
api_router.include_router(user_route, tags=["User"])
api_router.include_router(query_route, tags=["Query"])
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/health-check", tags=["Monitoring"])
@limiter.limit("60/minute")
async def health_check(request: Request):
    return {"status": "ok"}
