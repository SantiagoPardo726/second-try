from fastapi import Depends, FastAPI, HTTPException,Request,Form, Cookie
from fastapi.responses import HTMLResponse , RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from models import user as userModel
from models import item as itemModel
from database.database import SessionLocal, engine

from routes.user import user
from routes.item import item

userModel.Base.metadata.create_all(bind=engine)
itemModel.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user)
app.include_router(item)

templates = Jinja2Templates(directory="templates")
app.mount("/static",StaticFiles(directory="static"),name="static")

@app.get("/index",response_class=HTMLResponse)
def get_index(request:Request):
    return templates.TemplateResponse("index.html", {"request":request})

@app.post("/index", response_class=HTMLResponse)
def form_post(request: Request, user: str = Form(...), password: str = Form(...)):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login",response_class=HTMLResponse)
def get_login(request:Request):
    return templates.TemplateResponse("login.html", {"request":request})

@app.post("/login",response_class=HTMLResponse)
def post_login(request:Request):
    return templates.TemplateResponse("login.html", {"request":request})

