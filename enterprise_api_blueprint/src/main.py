from fastapi import FastAPI

from enterprise_api_blueprint.src.config import settings


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        debug=settings.app_debug,
        version="0.1.0",
    )

    @app.get("/")
    def root() -> dict[str, str]:
        return {
            "service": settings.app_name,
            "environment": settings.app_env,
            "status": "bootstrapped",
        }

    return app


app = create_app()
