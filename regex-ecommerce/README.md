# REGEX — Premium Clothing Store

A React + Vite storefront and Python FastAPI API scaffold for REGEX, using Supabase PostgreSQL/Auth/Storage. The UI includes home, catalogue, product detail, cart, checkout request flow, informational pages and an admin placeholder.

## Quick start
1. Copy `frontend/.env.local.example` to `frontend/.env.local` and configure the Supabase URL/key and API URL.
2. Configure `backend/.env` from `backend/.env.example`.
3. Apply `supabase/migrations/001_initial_schema.sql` in Supabase SQL Editor.
4. In one terminal: `cd frontend && npm install && npm run dev`.
5. In another: `cd backend && python -m venv .venv` then activate it, install `pip install -r requirements.txt`, and run `uvicorn app.main:app --reload --port 8000`.
6. Open `http://localhost:5173`; API docs are at `http://localhost:8000/docs`.

See [setup.md](setup.md) for full setup and production limitations. Demo products are display fallback only. Order creation intentionally returns HTTP 501 until the secure transactional order RPC and payment flow are implemented and verified; do not accept live orders yet.
