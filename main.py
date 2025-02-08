# Аутентификация - проверка наличия логина в базе и соответствующего ему пароля
# Авторизация - проверка наличия у пользователя прав для обращения к этой ручке
# JWT токен кодируется с помощью SECRET_KEY и декодируется(https://jwt.io/),
# занимает очень много памяти по сравнению с сессиями

from fastapi import FastAPI, HTTPException, Response, Depends
from authx import AuthX, AuthXConfig
from pydantic import BaseModel


app = FastAPI()

config = AuthXConfig()
config.JWT_SECRET_KEY = 'SECRET_KEY'
config.JWT_ACCESS_COOKIE_NAME = 'my_access_token'
config.JWT_TOKEN_LOCATION = ['cookies']

security = AuthX(config=config)


class UserLogicSchema(BaseModel):
    username: str
    password: str


@app.post('/login')
def login(credentials: UserLogicSchema, response: Response):
    if credentials.username == 'test' and credentials.password == 'test':
        token = security.create_access_token(uid='1')
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
        return {'access_token': token}
    raise HTTPException(status_code=401, detail='Incorrect username or password')


@app.get('/protected', dependencies=[Depends(security.access_token_required)])
def protected():
    return {'data': 'TOP SECRET'}