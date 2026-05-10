from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routes import orders, refunds, error_logs, manual_reviews, scheduled_emails, leads, auth, users
from app.routes.dashboard import router as dashboard_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully.")
    print("📦 Tables: users, orders, refunds, error_logs, manual_reviews, scheduled_emails")
    yield


app = FastAPI(
    title="BizLink B2B Workflow Automation",
    description="Backend API for BizLink platform - CSE 314 Group 3",
    version="1.0.0",
    lifespan=lifespan
)

# ✅ FIXED: CORS configuration - MUST be added BEFORE routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500", "*"],  # Allow Live Server
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],  # ✅ Explicitly allow OPTIONS
    allow_headers=["*"],
)

# Include routes
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(orders.router)
app.include_router(refunds.router)
app.include_router(error_logs.router)
app.include_router(manual_reviews.router)
app.include_router(scheduled_emails.router)
app.include_router(leads.router)
app.include_router(dashboard_router)

@app.get("/", operation_id="root_health_check")
def root():
    return {
        "message": "BizLink backend is running",
        "endpoints": {
            "auth": "/auth",
            "users": "/users",
            "orders": "/orders",
            "refunds": "/refunds",
            "error_logs": "/error-logs",
            "manual_reviews": "/manual-reviews",
            "scheduled_emails": "/scheduled-emails",
            "docs": "/docs"
        }
    }