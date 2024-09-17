from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from apps.admin.payments import router as admin_router
from apps.events import startup_events, shutdown_events
from config import settings


def init_routers(_app: FastAPI) -> None:
    """
    Initialize all routers.
    """
    _app.include_router(admin_router)

def root_health_path(_app: FastAPI) -> None:
    """
    Health Check Endpoint.
    """

    @_app.get("/", include_in_schema=False)
    def root() -> JSONResponse:
        """

        :return:
        """
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "SUCCESS"})

    @_app.get("/healthcheck", include_in_schema=False)
    def healthcheck() -> JSONResponse:
        """

        :return:
        """
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "SUCCESS"})


def init_middlewares(_app: FastAPI) -> None:
    """
    Middleware initialization.
    """
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOW_ORIGINS.split(","),
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
        allow_headers=["*"],
    )


def create_app(debug: bool = False) -> FastAPI:
    """
    Create a Initialize the FastAPI app.
    """
    _app = FastAPI(
        title=settings.APP_NAME, version=settings.APP_VERSION, docs_url="/docs", redoc_url="/redoc" if debug else None
    )
    init_routers(_app)
    root_health_path(_app)
    startup_events(_app)
    shutdown_events(_app)
    return _app


debug_app = create_app(debug=True)
production_app = create_app()
