from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))

from app.routers import login, register

app = FastAPI()

# API Routers
app.include_router(login.router)
app.include_router(register.router)

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR.parent.parent / "frontend"

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
        "front_page.html",
        {"request": request}
    )

# ---------------- USER ----------------

@app.get("/user/login", response_class=HTMLResponse)
async def user_login_page(request: Request):
    return templates.TemplateResponse(
        "userlogin.html",
        {"request": request}
    )

@app.get("/user/register", response_class=HTMLResponse)
async def user_register_page(request: Request):
    return templates.TemplateResponse(
        "userregister.html",
        {"request": request}
    )

# ---------------- ADMIN ----------------

@app.get("/admin/login", response_class=HTMLResponse)
async def admin_login_page(request: Request):
    return templates.TemplateResponse(
        "adminlogin.html",
        {"request": request}
    )

@app.get("/admin/register", response_class=HTMLResponse)
async def admin_register_page(request: Request):
    return templates.TemplateResponse(
        "adminregister.html",
        {"request": request}
    )