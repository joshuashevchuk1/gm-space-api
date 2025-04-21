# routes/__init__.py

from .home import router as home_router
from .health import router as health_router

routers = [home_router, health_router]
