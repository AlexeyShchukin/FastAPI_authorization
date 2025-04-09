from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException, status, Form
from fastapi.exceptions import RequestValidationError
from fastapi.security import OAuth2PasswordRequestForm
from starlette.middleware.cors import CORSMiddleware

from auth.rbac import has_role
from auth.tokens import create_access_token, create_refresh_token, get_user_from_token
from handlers import validation_exception_handler
from middlewares import LoggingMiddleware, origins
from models.users import UserIn, Role, UserOut
from database.fake_db import username_exists, get_user, save_user, authenticate_user, db

app = FastAPI()

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_middleware(LoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=['*'],
    allow_headers=['*'],
    allow_credentials=True
)


@app.post("/registration",
          status_code=status.HTTP_201_CREATED,
          tags=["Users"],
          response_model=UserOut)
def create_user(user: Annotated[UserIn, Form()]):
    if username_exists(user.username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="A user with this name already exists",
                            )
    saved_user = save_user(user)
    return saved_user


@app.post("/tokens",
          description="Creating access and refresh tokens",
          tags=["Users"])
def login(user_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, user_data.username, user_data.password)
    if user:
        access_token = create_access_token({"sub": user_data.username, "role": user["role"]})
        refresh_token = create_refresh_token({"sub": user_data.username, "role": user["role"]})
        return {"access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer"
                }
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid credentials",
                        headers={"WWW-Authenticate": "Bearer"},
                        )


@app.get("/refresh_token", description="Creates a new access token based on the refresh token")
def refresh_token(user: dict = Depends(get_user_from_token)):
    new_access_token = create_access_token({"sub": user["username"], "role": user["role"]})
    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }


@app.get("/protected_resource", description="Resource for authorized users")
def protected_resource(_=Depends(has_role([Role.ADMIN, Role.USER]))):
    return {"message": "You have access to this protected resource"}


@app.post("/create_resource", description="For admin")
def create_resource(_=Depends(has_role([Role.ADMIN]))):
    return {"message": "Resource created successfully"}


@app.put("/update_resource", description="Update resource for authorized users")
def update_resource(_=Depends(has_role([Role.ADMIN, Role.USER]))):
    return {"message": "Resource updated successfully"}


@app.delete("/delete_resource", description="For admin")
def delete_resource(_=Depends(has_role([Role.ADMIN]))):
    return {"message": "Resource deleted successfully"}
