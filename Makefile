.PHONY: dev-backend dev-frontend test lint typecheck

dev-backend:
	cd backend && uvicorn app.main:app --reload --port 8000

dev-frontend:
	cd frontend && npm run dev

test:
	cd backend && python -m pytest tests/ -v --cov=app --cov-report=term-missing

lint:
	cd backend && python -m ruff check app/ tests/

typecheck:
	cd backend && python -m mypy app/
