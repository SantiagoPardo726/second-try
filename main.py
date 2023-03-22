from fastapi import Depends, FastAPI, HTTPException
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

