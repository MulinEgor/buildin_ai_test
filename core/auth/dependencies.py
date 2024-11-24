from core.auth.respository import AuthRepository
from core.auth.service import AuthService


def get_auth_service() -> AuthService:
    return AuthService(AuthRepository())
