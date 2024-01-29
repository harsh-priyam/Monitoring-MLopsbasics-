from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
import os
import numpy as np
from src.src.IRIS_MLops.pipeline.prediction import PredictionPipeline
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
import uvicorn

app = FastAPI()

templates = Jinja2Templates(directory=os.path.join(os.path.dirname(os.path.abspath(__file__)), "src/templates"))

port = int(os.environ.get("PORT", 8005))

# CORS settings
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)



@app.get("/")
def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/train")
def training():
    os.system("python src/driver.py")
    return "Training Completed"

@app.post("/predict")
async def index(request: Request, sepal_length: float = Form(...), sepal_width: float = Form(...), 
                petal_length: float = Form(...), petal_width: float = Form(...)):

    try:
        data = np.array([[sepal_length, sepal_width, petal_length, petal_width]])

        obj = PredictionPipeline()
        predict = obj.predict(data)

        return templates.TemplateResponse("results.html", {"request": request, "prediction": str(predict)})

    except Exception as e:
        print('The Exception message is: ', e)
        return 'Something went wrong'

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=port,reload=False)

Instrumentator().instrument(app).expose(app)
