import os

import pickle # для сериализации модели
import time

from fastapi import FastAPI # для создания API
from fastapi import BackgroundTasks # для выполнения задач в фоне

from pydantic import BaseModel # для валидации данных, которые приходят в запросах


from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.datasets import load_digits

app = FastAPI()

MODELS_DIR = "backend/ml"

class Item(BaseModel):
    x: float
    y: float 
    
class TrainRequest(BaseModel):
    max_iter: int
    name: str
      
@app.get("/")
def root():
    return {"message": "Сервер работает!"}

@app.post("/sum")
def calc_sum(item: Item):
    res = item.x + item.y
    return {"message": res}

#
def train_model(req):
    data = load_digits()
    X, y = data.data, data.target
    
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        train_size=0.7,
        random_state=None
    )
    
    model = LogisticRegression(max_iter=100)
    
    time.sleep(10) # имитация долгой работы модели
    model.fit(X_train, y_train)
    
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    
    # путь для сохранения модели
    model_path = os.path.join(MODELS_DIR, f"{req.name}.pkl")
    
    # сериализация модели
    with open(model_path, "wb") as f:
        # выгружает модель в сериализованный вид
        pickle.dump(model, f)
    

@app.post("/train")# эндпоинт для обучения модели
def train(req: TrainRequest, background_tasks: BackgroundTasks): # принимает запрос на обучение модели и выполняет его в фоне
    
    background_tasks.add_task(train_model, req) # добавляем задачу на обучение модели в очередь задач в фоне
    
    return {
        "model_name": req.name,
        "message": "Model saved"
    }        
