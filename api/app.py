from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.schemas import HouseModel
from SRC.inference.predict import PredictPipeline

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"],)
predictor = PredictPipeline()


@app.get("/")
def home():
    return {
        "message" : "House price prediction API running"
    }

@app.post("/predict")
def predict(data:HouseModel):
    price = predictor.predict(data.model_dump())
    return{
        "preidicted price" : price
    }