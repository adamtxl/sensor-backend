from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class SensorReading(BaseModel):
    sensor_id: str
    type: str
    value: float
    timestamp: Optional[datetime] = None
    rssi: Optional[float] = None
    snr: Optional[float] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    altitude: Optional[float] = None

class Sensor(BaseModel):
    sensor_id: str
    location_id: Optional[int] = None  
    description: Optional[str] = None
    installed_on: Optional[datetime] = None
    display_name: Optional[str] = None
    sensor_type: str = Field(..., alias="type")


class Location(BaseModel):
    name: str
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[str] = None
    franchise_id: Optional[int] = None  

class Franchise(BaseModel):
    name: str

class EnrichedReading(BaseModel):
    sensor_id: str
    type: str
    value: float
    timestamp: datetime
    facility: str