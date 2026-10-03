from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from model import predict_price


app = FastAPI(title="Laptop Price Predictor API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LaptopData(BaseModel):
    company: str
    type: str
    ram: int
    weight: float
    touchscreen: str
    ips: str
    screen_size: float
    resolution: str
    cpu: str
    hdd: int
    ssd: int
    gpu: str
    os: str


@app.get("/")
def home():
    return {"message": "Laptop Price Predictor API is running"}


@app.post("/predict")
def predict(data: LaptopData):
    price = predict_price(data.dict())

    return {
        "predicted_price": price
    }