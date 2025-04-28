from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SensorReading(BaseModel):
    sensor_id: str
    type: str
    value: float
    timestamp: Optional[datetime] = None

class Sensor(BaseModel):
    sensor_id: str
    location_id: Optional[int] = None  
    description: Optional[str] = None
    installed_on: Optional[datetime] = None

class Location(BaseModel):
    name: str
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[str] = None
    franchise_id: Optional[int] = None  

class Franchise(BaseModel):
    name: str
