import os
import secrets
from pathlib import Path

from fastapi import Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader

from backend.domain.services.actor_context import ActorContext, ActorRole

TOKEN_FILE_PATH = Path(".lisan_owner_token")

def _get_or_create_owner_token() -> str:
    """Gets or creates the secure local owner token."""
    # Allow environment override for tests
    if "LISAN_OWNER_TOKEN" in os.environ:
        return os.environ["LISAN_OWNER_TOKEN"]
        
    if TOKEN_FILE_PATH.exists():
        return TOKEN_FILE_PATH.read_text(encoding="utf-8").strip()
    
    token = secrets.token_urlsafe(32)
    try:
        TOKEN_FILE_PATH.write_text(token, encoding="utf-8")
    except Exception:
        raise RuntimeError("Failed to read or create local owner token file.")
    return token

LOCAL_OWNER_TOKEN = _get_or_create_owner_token()

API_KEY_NAME = "X-Lisan-Owner-Token"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def require_owner_token(api_key: str = Security(api_key_header)) -> str:
    if not api_key:
        raise HTTPException(status_code=403, detail="Missing owner authority token")
    if api_key != LOCAL_OWNER_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid owner authority token")
    return api_key

def get_owner_actor(api_key: str = Depends(require_owner_token)) -> ActorContext:
    return ActorContext(role=ActorRole.OWNER_OPERATOR, identity="TRUSTED_LOCAL_OWNER")

def get_verifier_actor(api_key: str = Depends(require_owner_token)) -> ActorContext:
    return ActorContext(role=ActorRole.VERIFIER, identity="TRUSTED_LOCAL_INDEPENDENT_VERIFIER")

def get_researcher_actor(api_key: str = Depends(require_owner_token)) -> ActorContext:
    return ActorContext(role=ActorRole.RESEARCHER, identity="TRUSTED_LOCAL_RESEARCHER")
