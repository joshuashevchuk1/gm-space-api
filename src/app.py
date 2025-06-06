# main.py

from fastapi import FastAPI
import uvicorn
from handlers import handlers
from src.config import config


class GMApp:
    def __init__(self):
        self.config = config.Config()
        self.port = self.config.get_g_space_port()
        self.app = FastAPI(
            title="GM Space API",
            description="A modular FastAPI for handling google meet sessions and recording transcripts",
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
    app = GMApp()
    app.run_server()
