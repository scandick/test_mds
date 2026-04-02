from datetime import datetime, timedelta, timezone

# для создания jwt токена пользователя
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials, HTTPBearer

import jwt
from passlib.context import CryptContext

from fastapi import FastAPI

import secrets # аналог openssl rand -hex 64 # TODO: заменить на получение из env

SECRET_KEY = secrets.token_hex(64) # ключ подписи 
ALGORITHM = "HS256" # алгоритм шифрования

app = FastAPI()

pwd_context = CryptContext(
    schemes=["bcrypt"], # bcrypt = криптография с солью, защита от радужных таблиц
    deprecated="auto") # автоматически помечать старые алгоритмы как устаревшие

# функции для работы с паролями
def hash_password(password: str):
    return pwd_context.hash(password)  # БЕЗОПАСНО: каждый раз разный результат (из-за соли)

def verify_password(plain_password: str, 
                    hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password) # Проверяет: совпадает ли password с тем, что был захеширован
    
# функция создания токена
def create_access_token(data: dict,
                        expires_delta: timedelta = None):

    """
    JWT = 3 части, разделённые точками:
    header.payload.signature
    
    Пример реального токена:
    eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.
    eyJzdWIiOiJhZG1pbiIsImV4cCI6MTcxMjAwMDAwMH0.
    SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
    """

    to_encode = data.copy() # работаем с копией исходного dict
    
    # время истечения токена (дефолт: 24ч)
    now_utc = datetime.now(timezone.utc)
    if expires_delta:
        expire = now_utc + expires_delta
    else:
        expire = now_utc + timedelta(hours=24)
    #
    
    # exp - стандартное поле JWT, для проверки сервером времени (истёк-не истёк)
    to_encode.update({"exp": expire})
    
    # кодировка токена + подпись (чтобы никто не мог подделать токен, не зная секретного ключа)
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

security = HTTPBasic()

# !!! эндпоинт, выдающий токен
@app.post("/login") # проверяет подходящий ли логин/пароль
def login(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username == "admin" or credentials.password == "secret":
        # создание токена с имененм пользователя, "sub" - стандартное имя для юзера в JWT
        access_token = create_access_token({"sub": credentials.username})
        
        return {
            "access_token": access_token,
            "token_type": "bearer" # этот тип будет вытаскиваться потом в HTTPBearer()         
        }
        
    raise HTTPException(status_code=401, 
                        detail='Неверные данные учётной записи')
    
# HTTPBearer() = FastAPI сам вытаскивает токен из заголовка Authorization: Bearer <token>
def verify_token(token: str = Depends(HTTPBearer())): 
    try:
        # Декодируем токен (проверяем подпись и формат)
        payload = jwt.decode(
            token.credentials, 
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
    except (jwt.InvalidTokenError, jwt.DecodeError): 
        raise HTTPException(status_code=401, detail='Неверный токен')
    
    # Вытаскиваем username из payload
    username = payload.get("sub")
    
    # Если username отсутствует — токен повреждён
    if username is None: 
        raise HTTPException(status_code=401, detail='Имя пустое, токен поврежден') # TODO ветка не отрабатывает
    return username
            
@app.get("/protected") # эндпоинт, проверяющий валидность токена
def protected(current_user: str = Depends(verify_token)):
    # Если токен валидный → current_user = username
    # Если токен неверный → ошибка 401, функция не вызовется
    return {"message": f"Hello, {current_user}"}

# TODO: добавить регистрацию, хранение юзеров в БД, возможность задавать права доступа в токене (например, admin/user) и проверять их в эндпоинтах