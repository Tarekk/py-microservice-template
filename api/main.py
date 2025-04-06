from fastapi import FastAPI

from api.api import api_router
from api.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    generate_unique_id_function=lambda router: f"{router.tags[0]}-{router.name}",
)


# Include routers
app.include_router(api_router)
