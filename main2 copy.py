from fastapi import Depends, FastAPI, HTTPException, status, Request
from routes import route
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
templates = Jinja2Templates(directory="views")
app.mount("/images", StaticFiles(directory="images"), name="images")
app.mount("/views/css", StaticFiles(directory="views/css"), name="css")

@app.get("/login")
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

app.include_router(route, prefix="")