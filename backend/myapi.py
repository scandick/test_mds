import asyncio

from fastapi import FastAPI 

from pydantic import BaseModel # основа моделей данных

app = FastAPI()
#
@app.get("/")
def root():
    return {'text' : 'Hello world'}

    # Параметры через путь URL
@app.get("/users/{user_id}")
def get_user_1(user_id: int):
    return {"user_id": user_id,
            "name": f"User {user_id}"}
    
# uvicorn backend.myapi:app --reload

# -------------------------------------------------------------------------
# Параметры через Query (ключ-значение после ? в URL)
@app.get("/search")
def search(q: str, skip: int = 0, limit: int = 10):
    return {
        "query": q,
        "skip": skip,
        "limit": limit
    }
    
# -------------------------------------------------------------------------    
# GET /search?q=python&skip=5&limit=20

class Item(BaseModel):
    name: str
    price: float
    description: str = None
    
@app.post("/items")
def create_item(item: Item):
    return {
        "created" : item.name,
        "price" : item.price,
        "description" : item.description
    }
# POST /items
# Body (JSON): {"name": "Apple", "price": 10.99}

# -------------------------------------------------------------------------
   
from pydantic import BaseModel, Field # поля с дополнительными параметрами
from typing import Optional # для указания необязательных полей   

class User(BaseModel):
    id: int
    username: str
    email: str
    age: Optional[int] = None
    is_active: bool = True
    
@app.post("/users")
def create_user(user: User):
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "age": user.age,
        "is_active": user.is_active
    }
    
class Product(BaseModel):
    name: str = Field(..., min_length=3, max_length=50) # атрибуты строк
    price: float = Field(..., gt=0) # greater than 0
    quantity: int = Field(default=1, ge=0) # greater or equal to 0
    
@app.post("/products")
def create_product(product: Product):
    return {
        "name": product.name,
        "price": product.price,
        "quantity": product.quantity
    }
    
# ---------------------------------------------------------------------------

# Вложенные модели данных + списки и множества
from typing import List, Set

class Address(BaseModel):
    street: str
    city: str
    postal_code: str

class Person(BaseModel):
    name: str
    age: int
    address: Address  # вложенная модель
    hobbies: List[str] = []  # список хобби
    tags: Set[str] = set()  # множество тегов

@app.post("/persons")
def create_person(person: Person):
    return person

# ----------------------------------------------------------------------------
# async эндпоинт 
import time

@app.get("/async")
async def async_endpoint():
    await asyncio.sleep(10) # неблокирующая задержка
    return {"message": "async"}

# VS
# остальные запросы встают в очередь
@app.get("/sync")
def sync_endpoint():
    time.sleep(10) # блокирующая задержка
    return {"message": "sync"}
    
# ------------------------------------------------------------------------------
# Background Tasks - выполнение задач в фоне после ответа клиенту
from fastapi import BackgroundTasks

def send_email(email: str, message: str):
    time.sleep(5) # имитация отправки письма
    print(f"Email sent to {email} with message: {message}")

@app.post("/send-email")
def send_email_endpoint(email: str, 
                        message: str,
                        background_tasks: BackgroundTasks):
    background_tasks.add_task(send_email, email, message)
    return {"message": "Email будет отправлена в фоне"}
