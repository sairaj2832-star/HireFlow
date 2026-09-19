verify:
	powershell -ExecutionPolicy Bypass -File scripts/verify.ps1

migrate:
	cd backend && python -m app.db.migrate

dev-be:
	cd backend && uvicorn app.main:app --reload --port 8000

dev-fe:
	cd frontend && npm run dev
