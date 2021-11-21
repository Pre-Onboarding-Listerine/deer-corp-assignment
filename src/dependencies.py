from src.configs.database import SessionLocal


def get_session_factory():
    return SessionLocal
