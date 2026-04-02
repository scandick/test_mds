# Аутентификация и авторизация (Basic Auth)
from fastapi import HTTPException # выбрасывает ошибки при неудачной аутентификации
from fastapi import Depends # dependency injection: позволяет инжектировать проверку аутентификации в эндпоинты

from fastapi.security import HTTPBasic # класс для настройки Basic Authentification
from fastapi.security import HTTPBasicCredentials # модель данных для хранения username/password

from fastapi import FastAPI

app = FastAPI()

security = HTTPBasic() # объект для проверки Basic Auth в эндпоинтах
@app.get("/protected") # проверяет подходящий ли логин/пароль
def protected_route(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != "admin" or credentials.password != "secret":
        raise HTTPException(status_code=401, 
                        detail='Неверные данные учётной записи')
    return {"message": f"Добро пожаловать, {credentials.username}"}

# --------------------------------------------------------------------------------
