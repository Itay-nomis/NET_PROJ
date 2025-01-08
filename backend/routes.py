from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from schemas import LoginRequest, RegisterRequest
from services import check_login, register_user
from database.mysql_db import get_db

router = APIRouter()


@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)) -> JSONResponse:
    is_valid = check_login(username=request.username, password=request.password, db=db)
    if is_valid:
        return JSONResponse(content={"message": "Login successful"}, status_code=200)
    return JSONResponse(content={"message": "Invalid username or password"}, status_code=401)


@router.post("/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)) -> JSONResponse:
    return register_user(
        username=request.username,
        password=request.password,
        email=request.email,
        db=db
    )
