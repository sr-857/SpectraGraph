from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy.exc import OperationalError
import os
import time
import logging
from dotenv import load_dotenv

load_dotenv()

# Remplace avec ton URL de BDD
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost:5432/spectragraph")

logger = logging.getLogger(__name__)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class DatabaseUnavailableError(RuntimeError):
    pass


def _mask_password(dsn: str) -> str:
    try:
        # naive mask: replace password between : and @ in the authority
        if "@" in dsn and ":" in dsn.split("@")[0]:
            left, rest = dsn.split("@", 1)
            if ":" in left:
                user, _ = left.split(":", 1)
                return f"{user}:****@{rest}"
    except Exception:
        pass
    return dsn




def ensure_db_connection(max_retries: int = 5, base_delay: float = 1.0) -> None:
    """Try connecting to Postgres with exponential backoff. Raises DatabaseUnavailableError.

    Designed for local/dev startup checks to provide actionable feedback when DB is missing.
    """
    env = os.getenv("ENV", "development")
    masked = _mask_password(DATABASE_URL)

    for attempt in range(1, max_retries + 1):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            if env != "production":
                logger.info("✓ Database connection established: %s", masked)
            return
        except OperationalError as exc:
            if env != "production":
                if attempt < max_retries:
                    wait_time = base_delay * (2 ** (attempt - 1))
                    logger.warning(
                        "Database connection attempt %s/%s failed. Retrying in %.1fs... (Error: %s)",
                        attempt,
                        max_retries,
                        wait_time,
                        str(exc)[:100],
                    )
                else:
                    # All retries exhausted - log helpful error
                    error_msg = f"""
{'='*70}
❌ Cannot connect to Postgres database

Connection string: {masked}

Possible causes and solutions:

  1. Docker is not running
     → Check Docker status: docker ps
     → Start Docker Desktop or run: sudo systemctl start docker

  2. Database services not started
     → Start all services: make dev
     → Or just Postgres: docker-compose up -d postgres
     → Wait 5-10 seconds for Postgres to initialize

  3. Wrong database credentials in .env file
     → Check DATABASE_URL matches docker-compose.yml
     → Verify: cat .env | grep DATABASE_URL

  4. Port 5432/5433 already in use
     → Check port usage: lsof -i :5432
     → Or: netstat -tlnp | grep 5432
     → Change port in docker-compose.yml if needed

  5. Postgres container failed to start
     → Check logs: docker-compose logs postgres
     → Restart: docker-compose restart postgres

Troubleshooting commands:
  docker ps                    # Check running containers
  docker-compose logs postgres # View Postgres logs
  make dev                     # Start development environment

Original error: {type(exc).__name__}: {str(exc)[:200]}
{'='*70}
"""
                    logger.error(error_msg)
            
            # Short exponential backoff
            if attempt < max_retries:
                time.sleep(base_delay * (2 ** (attempt - 1)))
            else:
                raise DatabaseUnavailableError(
                    f"Unable to connect to the database at {masked} after {max_retries} retries."
                ) from exc


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
