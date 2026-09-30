from supabase import create_client
from app.core.config import SUPABASE_URL,SUPABASE_SERVICE_ROLE_KEY

def client():
    if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
        raise RuntimeError('Supabase is not configured. Set backend/.env from .env.example.')
    return create_client(SUPABASE_URL,SUPABASE_SERVICE_ROLE_KEY)
