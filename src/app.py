# main.py

from fastapi import FastAPI
import uvicorn
from handlers import handlers

class GMApp:
    def __init__(self, port: int):
        self.port = port
        self.app = FastAPI(
            title="GM Base API",
            description="A modular FastAPI app with home and health check endpoints.",
            version="1.0.0",
        )
        self._include_routes()
        self.db = None

    def _include_routes(self):
        for route in handlers:
            self.app.include_router(route)

    def run_server(self):
        uvicorn.run(self.app, host="0.0.0.0", port=self.port)

if __name__ == "__main__":
    app = GMApp(port=8000)
    app.run_server()
