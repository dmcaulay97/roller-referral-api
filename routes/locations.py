from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from db.models import Location
from schemas.location import LocationCreate, LocationUpdate, LocationResponse
from services.auth import verify_token
from services.encryption import encrypt

router = APIRouter(tags=["locations"])

@router.get("", response_model=list[LocationResponse])
def get_locations(token_data: dict = Depends(verify_token), db: Session = Depends(get_db)):
    return db.query(Location).filter(Location.user_id == token_data["id"]).all()

@router.post("", response_model=LocationResponse)
def create_location(location: LocationCreate, token_data: dict = Depends(verify_token), db: Session = Depends(get_db)):
    new_location = Location(
        name=location.name,
        encrypted_api_key=encrypt(location.roller_api_key),
        user_id=token_data["id"]
    )
    db.add(new_location)
    db.commit()
    db.refresh(new_location)
    return new_location

@router.patch("/{location_id}", response_model=LocationResponse)
def update_location(
    location_id: int,
    body: LocationUpdate,
    token_data: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    location = db.query(Location).filter(
        Location.id == location_id,
        Location.user_id == token_data["id"]
    ).first()

    if not location:
        raise HTTPException(status_code=404, detail="Location not found")

    if body.name:
        location.name = body.name
    if body.roller_api_key:
        location.encrypted_api_key = encrypt(body.roller_api_key)

    db.commit()
    db.refresh(location)
    return location

@router.delete("/{location_id}")
def delete_location(location_id: int, token_data: dict = Depends(verify_token), db: Session = Depends(get_db)):
    location = db.query(Location).filter(
        Location.id == location_id,
        Location.user_id == token_data["id"]
    ).first()
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    db.delete(location)
    db.commit()
    return {"message": "Location deleted"}