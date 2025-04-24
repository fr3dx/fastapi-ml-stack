from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import numpy as np
import joblib

app = FastAPI()

# Load the pre-trained model
model = joblib.load('regression_model.pkl')

# Templates directory setup
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")  # optional if you use static files

class Features(BaseModel):
    features: list[float]

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict")
async def predict(data: Features):
    try:
        x1 = float(data.features[0])
        x2 = float(data.features[1])
        input_data = np.array([[x1, x2]])
        prediction = model.predict(input_data)
        prediction = np.round(prediction, 6)

        return {
            'y1': prediction[0][0],
            'y2': prediction[0][1],
            'y3': prediction[0][2],
            'x1': x1,
            'x2': x2
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
