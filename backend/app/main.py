"""FastAPI application for the chemical process flowsheet simulator."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import components, distillation, flash, reactor

app = FastAPI(
    title="Flowsheet Simulator",
    version="0.1.0",
    description="Browser-based chemical process simulation wrapping chemeng-toolkit and sepflows.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(components.router, prefix="/api/components", tags=["components"])
app.include_router(flash.router, prefix="/api/flash", tags=["flash"])
app.include_router(distillation.router, prefix="/api/distillation", tags=["distillation"])
app.include_router(reactor.router, prefix="/api/reactor", tags=["reactor"])


@app.get("/api/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}
