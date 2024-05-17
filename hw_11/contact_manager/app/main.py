import os
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from contact_manager.app import schemas, database, crud, models
from contact_manager.app.config import DevelopmentConfig, TestingConfig, ProductionConfig

# Вибір конфігурації залежно від середовища
def get_config():
    env = os.getenv("ENV", "development")
    if env == "production":
        return ProductionConfig
    elif env == "testing":
        return TestingConfig
    else:
        return DevelopmentConfig

config = get_config()

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

@app.post("/contacts/", response_model=schemas.Contact)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(database.get_db)):
    return crud.create_contact(db=db, contact=contact)

@app.get("/contacts/", response_model=list[schemas.Contact])
def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    contacts = crud.get_contacts(db, skip=skip, limit=limit)
    return contacts

@app.get("/contacts/{contact_id}", response_model=schemas.Contact)
def read_contact(contact_id: int, db: Session = Depends(database.get_db)):
    db_contact = crud.get_contact(db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@app.put("/contacts/{contact_id}", response_model=schemas.Contact)
def update_contact(contact_id: int, contact: schemas.ContactUpdate, db: Session = Depends(database.get_db)):
    db_contact = crud.update_contact(db, contact_id=contact_id, contact=contact)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@app.delete("/contacts/{contact_id}", response_model=schemas.Contact)
def delete_contact(contact_id: int, db: Session = Depends(database.get_db)):
    db_contact = crud.delete_contact(db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@app.get("/contacts/search/", response_model=list[schemas.Contact])
def search_contacts(query: str, db: Session = Depends(database.get_db)):
    return crud.search_contacts(db=db, query=query)

@app.get("/contacts/upcoming_birthdays/", response_model=list[schemas.Contact])
def upcoming_birthdays(db: Session = Depends(database.get_db)):
    return crud.get_upcoming_birthdays(db=db)



