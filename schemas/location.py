from pydantic import BaseModel

class LocationCreate(BaseModel):
    name: str
    roller_api_key: str

class LocationUpdate(BaseModel):
    name: str | None = None
    roller_api_key: str | None = None

class LocationResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True