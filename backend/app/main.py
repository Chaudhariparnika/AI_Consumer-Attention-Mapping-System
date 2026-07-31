import os
import sys
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from database.database import Base, engine
from app.routers import analytics, camera, dashboard, google_auth, login, register  #, users, stores, cameras, etc.

# Create DB tables
Base.metadata.create_all(bind=engine)

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))


BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR.parent.parent / "frontend"


app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SECRET_KEY", "SUPER_SECRET_GLASSMORPHISM_KEY_CHANGE_IN_PROD"),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routers
app.include_router(login.router)
app.include_router(register.router)
app.include_router(dashboard.router)
app.include_router(camera.router)
app.include_router(analytics.router)
app.include_router(google_auth.router)


app.mount(
    "/static",
    StaticFiles(directory=FRONTEND_DIR / "static"),
    name="static"
)

templates = Jinja2Templates(
    directory=FRONTEND_DIR / "templates"
)

# Home Page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {"request": request}
    )

# ---------------- USER ----------------

@app.get("/register", response_class=HTMLResponse)
async def user_register_page(request: Request):
    return templates.TemplateResponse(
        "register.html",
        {"request": request}
    )


@app.get("/admin/dashboard", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    return templates.TemplateResponse(
        "admin_dashboard.html",
        {"request": request}
    )


@app.get("/store/dashboard", response_class=HTMLResponse)
async def store_dashboard(request: Request):
    return templates.TemplateResponse(
        "store_dashboard.html",
        {"request": request}
    )


@app.get("/retail/dashboard", response_class=HTMLResponse)
async def retail_dashboard(request: Request):
    return templates.TemplateResponse(
        "retail_dashboard.html",
        {"request": request}
    )


@app.get("/marketing/dashboard", response_class=HTMLResponse)
async def marketing_dashboard(request: Request):
    return templates.TemplateResponse(
        "marketing_dashboard.html",
        {"request": request}
    )


@app.get("/camera_management", response_class=HTMLResponse)
@app.get("/camera_management.html", response_class=HTMLResponse)
async def camera_management_page(request: Request):
    return templates.TemplateResponse(
        "camera_management.html",
        {"request": request}
    )

