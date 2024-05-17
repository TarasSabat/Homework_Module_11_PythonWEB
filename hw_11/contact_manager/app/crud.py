from sqlalchemy.orm import Session
from . import models, schemas
from datetime import timedelta, date
from sqlalchemy import or_, extract




def get_contact(db: Session, contact_id: int):
    return db.query(models.Contact).filter(models.Contact.id == contact_id).first()

def get_contacts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Contact).offset(skip).limit(limit).all()

def create_contact(db: Session, contact: schemas.ContactCreate):
    db_contact = models.Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def update_contact(db: Session, contact_id: int, contact: schemas.ContactUpdate):
    db_contact = get_contact(db, contact_id)
    if db_contact:
        for key, value in contact.dict().items():
            setattr(db_contact, key, value)
        db.commit()
        db.refresh(db_contact)
    return db_contact

def delete_contact(db: Session, contact_id: int):
    db_contact = get_contact(db, contact_id)
    if db_contact:
        db.delete(db_contact)
        db.commit()
    return db_contact

def search_contacts(db: Session, query: str):
    return db.query(models.Contact).filter(
        (models.Contact.first_name.contains(query)) |
        (models.Contact.last_name.contains(query)) |
        (models.Contact.email.contains(query))
    ).all()

def get_upcoming_birthdays(db: Session):
    today = date.today()
    upcoming = today + timedelta(days=7)

    # Querying contacts with upcoming birthdays
    contacts = db.query(models.Contact).filter(
        or_(
            # For birthdays in the same year
            (extract('month', models.Contact.birthday) == today.month) & (extract('day', models.Contact.birthday) >= today.day) & (extract('day', models.Contact.birthday) <= upcoming.day),
            # For birthdays in the next year
            (extract('month', models.Contact.birthday) == upcoming.month) & (extract('day', models.Contact.birthday) <= upcoming.day),
            # For birthdays in the previous year
            (extract('month', models.Contact.birthday) == today.month) & (extract('day', models.Contact.birthday) < today.day)
        )
    ).all()

    return contacts


