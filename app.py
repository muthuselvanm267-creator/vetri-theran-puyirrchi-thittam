from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from auth import register_user, authenticate, make_token, current_user
from state import HISTORY
from routers.home import router as home_router
from routers.party import router as party_router
from routers.jewelry import router as jewelry_router

load_dotenv()
app = FastAPI(title="PocketSmart AI", version="1.0.0")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(home_router)
app.include_router(party_router)
app.include_router(jewelry_router)

@app.get("/", response_class=HTMLResponse)
async def landing(request: Request):
    return templates.TemplateResponse(request, "home.html", {"user": current_user(request)})

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(request, "login.html", {"error": None})

@app.post("/login")
async def login(request: Request, email: str = Form(...), password: str = Form(...)):
    if not authenticate(email, password):
        return templates.TemplateResponse(request, "login.html", {"error": "Invalid email or password"}, status_code=401)
    response = RedirectResponse("/dashboard", status_code=303)
    response.set_cookie("pocketsmart_token", make_token(email), httponly=True, samesite="lax")
    return response

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse(request, "register.html", {"error": None})

@app.post("/register")
async def register(request: Request, email: str = Form(...), password: str = Form(...), confirm_password: str = Form(...)):
    if password != confirm_password:
        return templates.TemplateResponse(request, "register.html", {"error": "Passwords do not match"}, status_code=400)
    if len(password) < 6:
        return templates.TemplateResponse(request, "register.html", {"error": "Password must be at least 6 characters"}, status_code=400)
    try:
        register_user(email, password)
    except Exception as exc:
        return templates.TemplateResponse(request, "register.html", {"error": str(exc.detail if hasattr(exc, 'detail') else exc)}, status_code=400)
    response = RedirectResponse("/login", status_code=303)
    return response

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    user = current_user(request)
    if not user:
        return RedirectResponse("/login", status_code=303)
    return templates.TemplateResponse(request, "dashboard.html", {"user": user})

@app.get("/history", response_class=HTMLResponse)
async def history(request: Request):
    user = current_user(request)
    if not user:
        return RedirectResponse("/login", status_code=303)
    rows = [x for x in HISTORY if x["user"] == user]
    return templates.TemplateResponse(request, "history.html", {"user": user, "history": rows})

@app.get("/logout")
async def logout():
    response = RedirectResponse("/", status_code=303)
    response.delete_cookie("pocketsmart_token")
    return response
