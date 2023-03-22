from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from schemas.user import User,UserCreate
from schemas.item import Item,ItemCreate

from models.user import User as UserModel
from models.item import Item as ItemModel
from database.database import SessionLocal, engine

user = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@user.get("/users/", response_model=list[User])
def read_users(db: Session = Depends(get_db)):
    users = db.query(UserModel).all()
    return users

@user.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@user.post("/users/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = UserModel(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@user.post("/users/{user_id}/items/", response_model=Item)
def create_user_item(item: ItemCreate, user_id, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_item = ItemModel(**item.dict(),owner_id= user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@user.delete("/users/{user_id}", response_model=User)
def delete_item(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_user)
    db.commit()
    return db_user

@user.put("/users/{user_id}", response_model=User)
def update_item(user_id: int, user: User, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    for field, value in user:
        setattr(db_user, field, value)
    db.commit()
    db.refresh(db_user)
    return db_user