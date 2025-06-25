from fastapi import FastAPI
from routers import auth
from fastapi.middleware.cors import CORSMiddleware
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
import logging
import socket
from communications.email import lifespan
from routers.auth import router as auth_router
from scripts import data_seed, truncate_tables
from config import config
from routers.user import router as user_router
from routers.session import router as session_router

logger = logging.getLogger(__name__)

smtp_client = None  # Global variable to hold the SMTP connection


def start_server():
    app = FastAPI(lifespan=lifespan)

    FastAPIInstrumentor.instrument_app(app)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(user_router)
    app.include_router(auth_router)
    app.include_router(session_router)

    @app.get("/")
    async def read_item():
        logger.info(socket.gethostname())
        return {"home_page": f"hello {socket.gethostname()}"}

    @app.get("/healthz")
    async def healthz():
        logger.info(f"health check done, {socket.gethostname()}")
        return {"ping": f"health check done {socket.gethostname()}"}

    @app.post("/initdata")
    async def initialize_tables():
        logger.info(f"initialize_tables requested, {socket.gethostname()}")
        data_seed.main()
        return {"message": "data seeded successfully"}

    @app.post("/droptables")
    async def droptables():
        logger.info(f"initialize_tables requested, {socket.gethostname()}")
        truncate_tables.drop_tables()
        return {"message": "tables dropped successfully"}

    return app
