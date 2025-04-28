from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import readings, sensors, locations, franchises

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(readings.router)
app.include_router(sensors.router)
app.include_router(locations.router)
app.include_router(franchises.router)

@app.get("/")
def root():
    return {"message": "Sensor backend is running!"}
