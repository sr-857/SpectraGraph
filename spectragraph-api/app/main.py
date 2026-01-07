from fastapi import FastAPI
from spectragraph_core.core.graph_db import Neo4jConnection
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import logging
import sys
import time
from sqlalchemy import text
from spectragraph_core.core.postgre_db import ensure_db_connection, engine, DatabaseUnavailableError

# Routes to be included
from app.api.routes import auth
from app.api.routes import investigations
from app.api.routes import sketches
try:
    from app.api.routes import transforms
except Exception as _exc:  # optional dev-only router, keep startup robust
    transforms = None
    logging.getLogger(__name__).warning("Transforms routes unavailable: %s", _exc)
from app.api.routes import flows
from app.api.routes import events
from app.api.routes import analysis
from app.api.routes import chat
from app.api.routes import scan
from app.api.routes import keys
from app.api.routes import types
from app.api.routes import custom_types

load_dotenv()

URI = os.getenv("NEO4J_URI_BOLT")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")

origins = [
    "*",
]


app = FastAPI()
neo4j_connection = Neo4jConnection(URI, USERNAME, PASSWORD)


@app.on_event("startup")
async def startup_db_check():
    logger = logging.getLogger(__name__)
    try:
        ensure_db_connection()
    except DatabaseUnavailableError as exc:
        logger.error("Database unavailable on startup: %s", exc)
        # exit cleanly for local/dev environment
        sys.exit(1)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    """Health check endpoint for Docker healthcheck"""
    return {"status": "ok"}


@app.get("/health/db")
async def health_db():
    start_time = time.time()
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        latency = (time.time() - start_time) * 1000
        return {"status": "ok", "latency_ms": round(latency, 2)}
    except Exception as exc:
        return {"status": "unhealthy", "error": str(exc)}


app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(sketches.router, prefix="/api/sketches", tags=["sketches"])
app.include_router(
    investigations.router, prefix="/api/investigations", tags=["investigations"]
)
if transforms is not None:
    app.include_router(transforms.router, prefix="/api/transforms", tags=["transforms"])
else:
    logging.getLogger(__name__).info("Skipping /api/transforms router (optional dependency missing)")
app.include_router(flows.router, prefix="/api/flows", tags=["flows"])
app.include_router(events.router, prefix="/api/events", tags=["events"])
app.include_router(analysis.router, prefix="/api/analyses", tags=["analyses"])
app.include_router(chat.router, prefix="/api/chats", tags=["chats"])
app.include_router(scan.router, prefix="/api/scans", tags=["scans"])
app.include_router(keys.router, prefix="/api/keys", tags=["keys"])
app.include_router(types.router, prefix="/api/types", tags=["types"])
app.include_router(custom_types.router, prefix="/api/custom-types", tags=["custom-types"])
