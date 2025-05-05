# handlers/__init__.py

from .home import router as home
from .health import router as health
from .space import router as space
from .session import router as session

handlers = [
    home,
    health,
    space
]
