# 🚀 FastAPI — Полное руководство для начинающих

---

## 📌 Модуль 1: Основы (Endpoints, HTTP, Routing)

### Теория

**FastAPI** — это веб-фреймворк для создания API на Python. Он автоматически:
- генерирует документацию (Swagger UI)
- валидирует данные (Pydantic)
- работает с асинхроном (async/await)

**HTTP методы:**
- `GET` — получить данные
- `POST` — создать данные
- `PUT` — заменить данные
- `DELETE` — удалить данные
- `PATCH` — частично обновить

**Routing** — это связь пути в URL с функцией-обработчиком.

---

### Практика 1.1: Первый endpoint

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello, World!"}

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id, "name": f"User {user_id}"}

# Запуск: uvicorn main:app --reload
```

**Что происходит?**
- `@app.get("/")` — при GET запросе к `/` вызовется функция `root()`
- `@app.get("/users/{user_id}")` — `{user_id}` — параметр пути (path parameter)
- `user_id: int` — FastAPI сам парсит строку в число

**Документация:** http://localhost:8000/docs

---

### Практика 1.2: Query параметры

```python
@app.get("/search")
def search(q: str, skip: int = 0, limit: int = 10):
    return {
        "query": q,
        "skip": skip,
        "limit": limit
    }

# GET /search?q=python&skip=5&limit=20
```

**Path vs Query параметры:**
- **Path:** `@app.get("/users/{id}")` → `/users/123`
- **Query:** `@app.get("/users")` с `q: str` → `/users?q=test`

---

### Практика 1.3: POST запросы

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    description: str = None  # опциональный параметр

@app.post("/items")
def create_item(item: Item):
    return {
        "created": item.name,
        "price": item.price
    }

# POST /items
# Body (JSON): {"name": "Apple", "price": 10.99}
```

**Что происходит?**
- `item: Item` — FastAPI парсит JSON в объект `Item`
- если поле не указано — ошибка (если нет default значения)
- если указано лишнее поле — будет проигнорировано

---

## 📌 Модуль 2: Валидация данных (Pydantic)

### Теория

**Pydantic** — библиотека для валидации и сериализации данных. FastAPI встроенно её использует.

**Зачем нужна валидация?**
- Проверить типы данных
- Задать ограничения (диапазоны, длину строк)
- Генерировать ошибки автоматически
- Документировать API

---

### Практика 2.1: Базовые типы и constraints

```python
from pydantic import BaseModel, Field
from typing import Optional

class User(BaseModel):
    id: int
    username: str  # строка, обязательна
    email: str
    age: Optional[int] = None  # опциональная
    is_active: bool = True  # с значением по умолчанию

class Product(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0)  # gt = greater than
    quantity: int = Field(default=1, ge=0)  # ge = greater or equal

@app.post("/products")
def create_product(product: Product):
    return product

# POST /products
# Body: {
#   "name": "Python Book",
#   "price": 29.99,
#   "quantity": 5
# }
```

**Field параметры:**
- `min_length`, `max_length` — для строк
- `gt`, `ge`, `lt`, `le` — сравнение (>, >=, <, <=)
- `default` — значение по умолчанию
- `...` — поле обязательно

---

### Практика 2.2: Вложенные модели

```python
class Address(BaseModel):
    street: str
    city: str
    postal_code: str

class Person(BaseModel):
    name: str
    age: int
    address: Address  # вложенная модель

@app.post("/persons")
def create_person(person: Person):
    return person

# POST /persons
# Body: {
#   "name": "John",
#   "age": 30,
#   "address": {
#     "street": "123 Main St",
#     "city": "New York",
#     "postal_code": "10001"
#   }
# }
```

---

### Практика 2.3: Списки и множества

```python
from typing import List, Set

class Order(BaseModel):
    items: List[str]  # список строк
    tags: Set[str]  # множество уникальных значений
    quantities: List[int]

@app.post("/orders")
def create_order(order: Order):
    return order

# Body: {
#   "items": ["apple", "banana", "orange"],
#   "tags": ["urgent", "vip"],
#   "quantities": [5, 3, 2]
# }
```

---

## 📌 Модуль 3: Асинхронность (async/await, BackgroundTasks)

### Теория

**Async/await** позволяет серверу обрабатывать множество запросов параллельно.

**Синхронный код (блокирует):**
```
Запрос 1 (ждёт 5 сек) → Запрос 2 (ждёт 5 сек) → Запрос 3 (ждёт 5 сек)
Всего: 15 сек
```

**Асинхронный код (асинхронный ввод-вывод):**
```
Запрос 1 (ждёт) \
Запрос 2 (ждёт)  → Все выполняются параллельно
Запрос 3 (ждёт) /
Всего: 5 сек
```

**BackgroundTasks** — для задач, которые не нужно делать синхронно (они выполняют после возврата ответа).

---

### Практика 3.1: Базовый async endpoint

```python
import asyncio

@app.get("/async-endpoint")
async def async_endpoint():
    await asyncio.sleep(1)  # неблокирующая задержка
    return {"message": "Done"}

# vs 

@app.get("/sync-endpoint")
def sync_endpoint():
    time.sleep(1)  # БЛОКИРУЕТ сервер
    return {"message": "Done"}

# Правило: если внутри await — делай async def
```

---

### Практика 3.2: BackgroundTasks (как в вашем проекте)

```python
from fastapi import BackgroundTasks
import time

def send_email(email: str, message: str):
    time.sleep(2)  # имитация отправки
    print(f"Email sent to {email}: {message}")

@app.post("/send-email")
def send_email_endpoint(email: str, message: str, background_tasks: BackgroundTasks):
    # Возвращаем ответ сразу
    background_tasks.add_task(send_email, email, message)
    return {"status": "Email будет отправлена в фоне"}

# POST /send-email?email=user@example.com&message=Hello
# Ответ приходит сразу, а email отправляется в фоне
```

**Когда использовать BackgroundTasks:**
- отправка email
- запись в БД (если это долго)
- обработка больших файлов
- ML训练 (как в вашем проекте!)

---

### Практика 3.3: Async с внешними запросами

```python
import httpx  # async HTTP клиент

@app.get("/fetch-data")
async def fetch_data(url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()

# Это будет асинхронно и не будет блокировать сервер
```

**Важно:** 
- `async def` нужна, если внутри `await`
- `await httpx.AsyncClient().get(...)` — асинхронный, не блокирует
- `requests.get(...)` — синхронный, блокирует! Не используй с async

---

## 📌 Модуль 4: Авторизация и аутентификация

### Теория

**Аутентификация** — проверка что пользователь это именно он (логин/пароль)
**Авторизация** — проверка что пользователь имеет право это делать (роли/права)

**Способы:**
1. **Basic Auth** — username:password в заголовке (небезопасно без HTTPS)
2. **JWT Token** — токен, который проверяется на каждый запрос
3. **OAuth 2.0** — делегированная авторизация (Google, GitHub)

---

### Практика 4.1: Basic Authentication

```python
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()

@app.get("/protected")
def protected_route(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != "admin" or credentials.password != "secret":
        raise HTTPException(status_code=401, detail="Неверные учётные данные")
    return {"message": f"Welcome, {credentials.username}"}

# Запрос с Authentication заголовком:
# GET /protected
# Authorization: Basic YWRtaW46c2VjcmV0 (base64 encoded admin:secret)
```

---

### Практика 4.2: JWT токены (рекомендуется)

```python
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

# ═══════════════════════════════════════════════════════════════════════
# ШАГЕ 1: КОНФИГУРАЦИЯ БЕЗОПАСНОСТИ
# ═══════════════════════════════════════════════════════════════════════

SECRET_KEY = "your-secret-key"  # 🔐 Суперсекретный ключ! Кодируй случайную строку (используй: openssl rand -hex 32)
ALGORITHM = "HS256"  # 🔐 Алгоритм шифрования JWT (HS256 = HMAC-SHA256)

# CryptContext настроивает хеширование паролей
pwd_context = CryptContext(
    schemes=["bcrypt"],  # bcrypt = криптография с солью, защита от радужных таблиц
    deprecated="auto"   # Автоматически обновляет старые хеши при проверке
)

# ═══════════════════════════════════════════════════════════════════════
# ШАГЕ 2: ФУНКЦИИ РАБОТЫ С ПАРОЛЯМИ
# ═══════════════════════════════════════════════════════════════════════

def hash_password(password: str):
    """
    Превращает пароль в нечитаемый хеш.
    ✅ БЕЗОПАСНО: каждый раз разный результат (из-за соли)
    ❌ НЕЛЬЗЯ вернуть пароль из хеша (one-way функция)
    
    Пример:
    - password="secret" → hash="$2b$12$eIEZ.1..."
    - Даже если два раза хешировать "secret", будут разные результаты
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    """
    Сравнивает обычный пароль с хешем.
    ✅ Проверяет: совпадает ли password с тем, что был захеширован
    
    Пример:
    - plain_password="secret", hashed="$2b$12$eIEZ.1..." → True
    - plain_password="wrong", hashed="$2b$12$eIEZ.1..." → False
    """
    return pwd_context.verify(plain_password, hashed_password)

# ═══════════════════════════════════════════════════════════════════════
# ШАГЕ 3: ФУНКЦИЯ СОЗДАНИЯ JWT ТОКЕНА
# ═══════════════════════════════════════════════════════════════════════

def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Создаёт JWT токен (подписанную строку с данными).
    
    Что это такое?
    JWT = 3 части, разделённые точками:
    header.payload.signature
    
    Пример реального токена:
    eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.
    eyJzdWIiOiJhZG1pbiIsImV4cCI6MTcxMjAwMDAwMH0.
    SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
    
    Шаг 1: Копируем данные (чтобы не потеряться с исходным dict)
    """
    to_encode = data.copy()
    
    """
    Шаг 2: Добавляем время истечения (exp = expiration)
    Если expires_delta не задан → токен живёт 24 часа
    Иначе → живёт столько, сколько указали
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=24)  # По умолчанию 24 часа
    
    """
    Шаг 3: Добавляем "exp" в данные (это стандартное поле JWT)
    Сервер будет проверять: не истёк ли токен при проверке
    """
    to_encode.update({"exp": expire})
    
    """
    Шаг 4: Кодируем и подписываем (HMAC-SHA256)
    SECRET_KEY = подпись, которая доказывает, что токен создал именно мы
    Если строку внутри токена изменить → подпись не совпадёт → токен украдена!
    """
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt  # Возвращаем готовый токен (строку)

# ═══════════════════════════════════════════════════════════════════════
# ШАГЕ 4: ENDPOINT ЛОГИНА (выдаёт токен)
# ═══════════════════════════════════════════════════════════════════════

@app.post("/login")
def login(username: str, password: str):
    """
    Клиент отправляет username и password.
    Если верны → получает токен.
    Если неверны → ошибка 401 Unauthorized.
    
    ВАЖНО: Это БЕЗ Basic Auth, прямые параметры!
    """
    
    # Проверка в БД (упрощено, в реальности искали бы в БД)
    if username == "admin" and password == "secret":
        # Создаём токен с именем пользователя
        # "sub" = subject (стандартное имя в JWT для юзера)
        access_token = create_access_token({"sub": username})
        
        # Возвращаем объект с токеном
        return {
            "access_token": access_token,  # Сам токен (строка)
            "token_type": "bearer"          # Тип: "bearer" = используется в Authorization: Bearer <token>
        }
    
    # Неверные учётные данные → 401
    raise HTTPException(status_code=401, detail="Invalid credentials")

# ═══════════════════════════════════════════════════════════════════════
# ШАГЕ 5: ФУНКЦИЯ ПРОВЕРКИ ТОКЕНА
# ═══════════════════════════════════════════════════════════════════════

def verify_token(token: str = Depends(HTTPBearer())):
    """
    Проверяет JWT токен из заголовка Authorization.
    
    HTTPBearer() = FastAPI сам вытаскивает строку из:
    Authorization: Bearer eyJhbGc...
    (вытаскивает часть после "Bearer ")
    
    Возвращает: username, если токен валидный
    Ошибка 401, если недействительный
    """
    try:
        # Декодируем токен (проверяем подпись + формат)
        # jwt.decode автоматически проверит:
        # 1. Подпись правильная (SECRET_KEY совпадает)
        # 2. Время истечения (exp) не прошло
        payload = jwt.decode(
            token.credentials,      # Сам токен
            SECRET_KEY,             # Ключ подписи (если не совпадает → ошибка!)
            algorithms=[ALGORITHM]  # Какой алгоритм использовали
        )
        
        # Вытаскиваем username из payload ("sub" = subject)
        username = payload.get("sub")
        
        # Если username отсутствует → токен повреждён
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        return username  # Успех! Возвращаем username
    
    except JWTError:
        # Ошибка при декодировании (неверная подпись, истёк токен и т.д.)
        raise HTTPException(status_code=401, detail="Invalid token")

# ═══════════════════════════════════════════════════════════════════════
# ШАГЕ 6: ЗАЩИЩЁННЫЙ ENDPOINT
# ═══════════════════════════════════════════════════════════════════════

@app.get("/protected")
def protected(current_user: str = Depends(verify_token)):
    """
    Этот endpoint ТРЕБУЕТ валидный JWT токен.
    
    Как работает:
    1. Клиент отправляет GET /protected с заголовком:
       Authorization: Bearer eyJhbGc...
    2. FastAPI вызовет verify_token()
    3. Если токен валидный → current_user = username
    4. Если токен неверный → ошибка 401, функция не вызовется
    
    Это dependency injection: verify_token автоматически вызывается!
    """
    return {"message": f"Hello, {current_user}"}

# ═══════════════════════════════════════════════════════════════════════
# ПОЛНЫЙ ПОТОК АУТЕНТИФИКАЦИИ
# ═══════════════════════════════════════════════════════════════════════

# ШАГ 1: Логин (получить токен)
# POST /login?username=admin&password=secret
# Ответ: {"access_token": "eyJhbGc...", "token_type": "bearer"}

# ШАГ 2: Получить защищённые данные
# GET /protected
# Заголовок: Authorization: Bearer eyJhbGc...
# Ответ: {"message": "Hello, admin"}

# ШАГ 3: Если токен истёк или неверный
# GET /protected (с неверным/истёкшим токеном)
# Ответ: 401 Unauthorized
```

**Установка:** `pip install python-jose passlib bcrypt`

---

### 📚 Ключевые отличия JWT от Basic Auth

| Параметр | Basic Auth | JWT |
|----------|-----------|-----|
| **Передача** | Base64(username:password) в заголовке | Подписанный токен |
| **Безопасность** | Пароль видна в base64 | Токен подписан, пароль не отправляется |
| **HTTPS** | ОБЯЗАТЕЛЕН | Рекомендуется |
| **Время жизни** | Каждый запрос проверяется заново | Токен живёт N часов |
| **Скорость** | Медленнее (проверка пароля каждый раз) | Быстрее (только проверка подписи) |
| **Стандарт** | HTTP базовый | Современный стандарт |

---

### 🔒 Важные моменты безопасности

1. **SECRET_KEY — абсолютный секрет!**
   - Генерируй: `openssl rand -hex 32`
   - Храни в `.env` файле, НЕ в коде
   - Если утечка → пересоздай все токены

2. **Время истечения (exp)**
   - Короче (15 минут) = безопаснее
   - Длиннее (7 дней) = удобнее
   - Обычно используют refresh-токены (они обновляют access-токены)

3. **HTTPS в production**
   - Без HTTPS даже JWT может быть украден
   - Используй SSL сертификат (Let's Encrypt бесплатный)

---

## 📌 Модуль 5: Работа с БД (SQLAlchemy)

### Теория

**SQLAlchemy** — ORM (Object-Relational Mapping) для работы с БД.

**Концепты:**
- **Model** — класс, который соответствует таблице в БД
- **Session** — соединение с БД, через которое мы выполняем запросы
- **Migration** — версионирование схемы БД

---

### Практика 5.1: Подключение и базовая модель

```python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Подключение к SQLite (для разработки)
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Модель БД
class UserDB(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

# Создаём таблицы
Base.metadata.create_all(bind=engine)

# Pydantic модель для API
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    
    class Config:
        from_attributes = True  # для конвертации из ORM объекта

# Dependecy для получения session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db = Depends(get_db)):
    db_user = UserDB(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/users", response_model=list[UserResponse])
def list_users(skip: int = 0, limit: int = 10, db = Depends(get_db)):
    users = db.query(UserDB).offset(skip).limit(limit).all()
    return users
```

**Установка:** `pip install sqlalchemy`

---

### Практика 5.2: Миграции с Alembic

```bash
# Инициализация
alembic init alembic

# Создание миграции
alembic revision --autogenerate -m "Add users table"

# Применение миграции
alembic upgrade head
```

---

## 📌 Модуль 6: Развёртывание и Production

### Теория

**Development vs Production:**
- **Development:** `uvicorn main:app --reload` (горячая перезагрузка)
- **Production:** Gunicorn/Uvicorn с несколькими workers, HTTPS, логирование

---

### Практика 6.1: Gunicorn + Uvicorn

```bash
# Установка
pip install gunicorn

# Запуск с 4 workers
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

---

### Практика 6.2: Docker

```dockerfile
FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
```

```bash
docker build -t my-api .
docker run -p 8000:8000 my-api
```

---

### Практика 6.3: Environment variables

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "FastAPI App"
    debug: bool = False
    database_url: str
    secret_key: str
    
    class Config:
        env_file = ".env"

settings = Settings()

@app.get("/")
def root():
    return {"name": settings.app_name}
```

**.env файл:**
```
DATABASE_URL=postgresql://user:password@localhost/dbname
SECRET_KEY=your-secret-key
DEBUG=true
```

**Установка:** `pip install pydantic-settings python-dotenv`

---

## 🎯 Ваш проект: Анализ и улучшения

Ваш код `/home/andrey/Projects/test_bot/backend/api.py` использует:
- ✅ Endpoints (`@app.get`, `@app.post`)
- ✅ Pydantic валидацию (`Item`, `TrainRequest`)
- ✅ BackgroundTasks (для обучения модели)
- ❌ Нету: Авторизации, БД, обработки ошибок
- ❌ Нету: Async/await (хотя BackgroundTasks это заменяет)

**Рекомендации улучшения:**
1. Добавить обработку ошибок (try/except)
2. Логирование обучения модели
3. Endpoint для загрузки обученной модели
4. БД для истории обучения
5. Авторизация для чувствительных операций

---

## 📚 Ресурсы

- [Официальная документация FastAPI](https://fastapi.tiangolo.com/)
- [Pydantic](https://docs.pydantic.dev/)
- [SQLAlchemy](https://docs.sqlalchemy.org/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)

---

## 🚦 Следующие шаги

1. **Уровень 1:** Прочитай понимай практику 1.1–1.3 (endpoints)
2. **Уровень 2:** Улучши Pydantic модели в своём проекте (модуль 2)
3. **Уровень 3:** Разберись с BackgroundTasks в своём коде (модуль 3)
4. **Уровень 4:** Добавь JWT авторизацию (модуль 4)
5. **Уровень 5:** Подключи SQLite БД (модуль 5)
6. **Уровень 6:** Задеплой на сервер (модуль 6)

Начни с модуля 1-2, потом спроси вопросы по конкретным темам!
