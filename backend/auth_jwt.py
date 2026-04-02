from datetime import datetime, timedelta, timezone

# для создания jwt токена пользователя
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import jwt
from passlib.context import CryptContext

from fastapi import FastAPI

SECRET_KEY = "key"
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

@app.post("/login") # проверяет подходящий ли логин/пароль
def protected_route(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username == "admin" or credentials.password == "secret":
        # создание токена с имененм пользователя, "sub" - стандартное имя для юзера в JWT
        access_token = create_access_token({"sub": credentials.username})
        
        return {
            "access_token": access_token,
            "token_type": "bearer"            
        }
        
    raise HTTPException(status_code=401, 
                        detail='Неверные данные учётной записи')



