from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from schemas.item import Item, ItemCreate
from models.item import Item as ItemModel
from database.database import SessionLocal, engine

item = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@item.get("/items/", response_model=list[Item])
def read_items(db: Session = Depends(get_db)):
    items = db.query(ItemModel).all()
    return items

@item.get("/items/{item_id}", response_model=Item)
def read_user(item_id: int, db: Session = Depends(get_db)):
    db_items = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if db_items is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_items

@item.post("/items/", response_model=Item)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = ItemModel(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@item.delete("/items/{item_id}", response_model=Item)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    return db_item

@item.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: Item, db: Session = Depends(get_db)):
    db_item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    for field, value in item:
        setattr(db_item, field, value)
    db.commit()
    db.refresh(db_item)
    return db_item