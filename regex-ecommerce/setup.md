# REGEX setup and deployment guide

## 1. Overview
REGEX is a React/Vite storefront with a Python FastAPI API and Supabase PostgreSQL/Auth/Storage. The current deliverable is a runnable UI and initial API/database foundation. Demo catalogue entries are fallback examples, not real inventory. The order endpoint deliberately does not create orders or report payment success: a secure transaction/RPC and verified payment gateway flow are required before production sales.

## 2. Prerequisites
- Node.js 20+ and npm
- Python 3.11+
- Git
- Supabase account/project
- Optional Razorpay merchant account for payment activation

## 3. Structure
- `frontend/`: React, Vite, routes, styling and cart state
- `backend/`: FastAPI app and API routes
- `supabase/migrations/`: SQL schema and RLS policies

## 4. Frontend — Windows PowerShell
```powershell
cd frontend
Copy-Item .env.local.example .env.local
npm install
npm run dev
```
Set values in `frontend/.env.local`. `VITE_SUPABASE_URL` and `VITE_SUPABASE_ANON_KEY` are browser-safe project values; do not put a service-role key here. `VITE_API_BASE_URL=http://localhost:8000` for local development. Build with `npm run build`.

macOS/Linux: `cp .env.local.example .env.local` then use the same npm commands.

## 5. Backend — Windows PowerShell
```powershell
cd backend
Copy-Item .env.example .env
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:PYTHONPATH="."
uvicorn app.main:app --reload --port 8000
```
If PowerShell blocks activation, use `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` for the current terminal, or invoke `.venv\Scripts\python.exe -m pip install -r requirements.txt` and `.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000`.

macOS/Linux:
```bash
cd backend
cp .env.example .env
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=. uvicorn app.main:app --reload --port 8000
```
API health: `GET http://localhost:8000/health`; interactive docs: `/docs`.

## 6. Supabase database
1. Create a Supabase project and copy its project URL and anon/publishable key into frontend env.
2. Copy project URL and service-role key into backend `.env` only. The service-role key bypasses RLS and must never be exposed in browser code or Git.
3. Open Supabase Dashboard → SQL Editor, paste and run `supabase/migrations/001_initial_schema.sql`.
4. Create an Auth user through Supabase Auth. Provision profile role through a trusted SQL editor only after verifying the user's UUID. Never allow public self-registration to set `role=admin`.
5. Create a Storage bucket named `product-images`. Keep uploads admin-only. Configure bucket policies to allow public reads only if product image URLs are intended to be public, and restrict writes/deletes to authorized admins.
6. Confirm RLS is enabled and test access using separate customer and admin accounts. SQL policies are a starting baseline and require review before launch.

## 7. Supabase Auth
Enable email/password authentication in Supabase Auth. Configure the allowed site URL and redirect URLs for local (`http://localhost:5173`) and production domains. The storefront currently contains auth/database scaffolding but full customer auth UI, session enforcement and admin authorization integration remain to be completed before launch.

## 8. Inventory and product data
Insert real categories, products, images and product variants into the corresponding tables. Products need at least one image and one variant for a useful catalogue. The current frontend displays local demo examples if the API is unavailable; replace these with verified product data before launch. Confirm image URLs are accessible and accurate, and provide factual fabric, fit and care details from the brand.

## 9. Orders and payments — production gate
The order API currently responds with `501` intentionally. Before launch, implement a Postgres function/RPC or equivalent transaction that re-reads product prices, locks/checks inventory, calculates shipping/discounts, inserts order/order_items and decrements stock atomically. Validate authenticated identity and customer data server-side. Add idempotency and prevent duplicate checkout submissions.

For Razorpay, configure credentials only in backend environment, create payment orders server-side, verify signatures server-side, validate webhook signatures and make webhook processing idempotent. Never mark an order paid from a browser callback alone. Do not store card data. Test in gateway sandbox before enabling live mode. COD must remain disabled unless the merchant explicitly supports it. Coupons also require server-side validation and calculation.

## 10. GitHub
From the project root:
```bash
git init
git add .
git commit -m "Initial REGEX storefront"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/regex-ecommerce.git
git push -u origin main
```
Create the repository on GitHub first and replace the URL. Check `git status` and ensure `.env`, `.env.local`, service-role keys and payment secrets are not staged. If a secret was committed, revoke/rotate it immediately; deleting it from a later commit is not sufficient.

## 11. Vercel frontend deployment
1. Import the GitHub repository in Vercel.
2. Set Root Directory to `frontend`.
3. Framework preset: Vite; build command `npm run build`; output directory `dist`.
4. Add `VITE_SUPABASE_URL`, `VITE_SUPABASE_ANON_KEY`, `VITE_API_BASE_URL`, and `VITE_SITE_URL` in Vercel Project Settings → Environment Variables for Preview and Production as appropriate.
5. Deploy, then set Supabase Auth redirect URLs to the live domain.
6. Update backend `FRONTEND_URL` and CORS allowed origins to the exact deployed domain.

## 12. FastAPI deployment
The backend is separately deployable. Vercel Python runtime support and function constraints may change; verify current Vercel Python runtime documentation and test the deployment configuration against the selected account/region. If FastAPI routing, dependencies, execution limits or persistent task needs are unsuitable, deploy the API to a Python application host instead. Configure `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`, `FRONTEND_URL`, `ENVIRONMENT` and payment secrets in the backend host's secret manager. Set `VITE_API_BASE_URL` in Vercel to the HTTPS API origin and redeploy frontend.

## 13. Domain and launch checklist
- Connect a domain in Vercel and configure DNS exactly as shown by Vercel.
- Use HTTPS and correct canonical/site URLs.
- Replace placeholder email, policy, delivery, returns and support content with the actual merchant terms; have legal text reviewed for the business and jurisdiction.
- Add real product photos, names, descriptions, sizes, variants, prices and stock.
- Implement customer auth, admin UI/API permissions, transactional orders, Razorpay/COD decision, email/WhatsApp notifications and order tracking.
- Test mobile and desktop, accessibility, RLS, API validation, inventory race conditions, payment success/failure/cancel/webhook replay and refunds.
- Configure monitoring, backups, error reporting and support contact.
- Verify all pages, metadata, sitemap and robots rules on production.

## 14. Testing
Frontend: `cd frontend && npm install && npm run build`.
Backend: activate virtual environment, install requirements, then run `PYTHONPATH=. uvicorn app.main:app --reload --port 8000`; check `/health`, `/docs`, `/api/products` after Supabase configuration. Add automated pytest and frontend interaction tests before launch. A successful local build does not certify payment, security, policy or production readiness.

## 15. Troubleshooting
- Frontend cannot reach API: verify backend is running, `VITE_API_BASE_URL`, browser console and CORS origin.
- Catalogue empty: verify SQL migration, active product rows, related image/variant records, credentials and backend logs.
- Supabase permission denied: inspect RLS and policies using a customer session; do not solve by exposing service-role key.
- Auth redirect failure: add exact local/live URLs to Supabase Auth redirect allowlist.
- Vercel 404 on deep routes: configure SPA rewrite to `/index.html` if needed for the Vite frontend.
- Backend deploy fails: check runtime support, Python version, import path, requirements and host logs.
- Payment/order disabled: expected until secure transactional order flow and payment verification are implemented.

## 16. Cost notes
₹10,000 is the project development target, not a guarantee of zero operating costs. Domain renewal, payment gateway fees, hosting/storage over free-tier limits, email/SMS and maintenance may cost extra. Check provider pricing before production use.
