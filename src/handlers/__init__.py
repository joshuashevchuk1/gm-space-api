# handlers/__init__.py

from .home import router as home
from .health import router as health
from .auth import router as auth

handlers = [
    home,
    health,
    auth
]
