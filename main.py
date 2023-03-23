from fastapi import Depends, FastAPI,Request,Form, Cookie,Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session


from models import user as userModel
from models import item as itemModel
from database.database import engine

from routes.user import user
from routes.item import item
import usercons

userModel.Base.metadata.create_all(bind=engine)
itemModel.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user)
app.include_router(item)


templates = Jinja2Templates(directory="templates")
app.mount("/static",StaticFiles(directory="static"),name="static")

#------------------------------------------------------------
#Index page
#------------------------------------------------------------

@app.get("/index",response_class=HTMLResponse)
def get_index(request:Request, response:Response):
    return templates.TemplateResponse("index.html", {"request":request})

#, user: str = Form(...), password: str = Form(...),
@app.post("/index", response_class=HTMLResponse)
def form_post(request: Request, response:Response):
    return templates.TemplateResponse("index.html", {"request": request})
#------------------------------------------------------------
#login page
#------------------------------------------------------------
@app.get("/login",response_class=HTMLResponse)
def get_login(request:Request, response:Response, ):
    return templates.TemplateResponse("login.html", {"request":request})

@app.post("/login",response_class=HTMLResponse)
def post_login(request:Request, response:Response):
    return templates.TemplateResponse("login.html", {"request":request})
#------------------------------------------------------------
#user-items page
#------------------------------------------------------------

@app.get("/user-items",response_class=HTMLResponse)
def get_login(request:Request, response:Response):
    user = ""
    print(user)
    context = {"request":request,"user":""}
    return templates.TemplateResponse("login.html", context)
