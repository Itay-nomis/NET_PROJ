from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from services import check_login, register_user
from database.mysql_db import get_db

router = APIRouter()


@router.get("/{username}/{password}")
def login(username: str, password: str, db: Session = Depends(get_db)) -> bool:
    return check_login(username=username, password=password, db=db)


@router.post("/register")
def register(username: str, password: str, email: str, db: Session = Depends(get_db)) -> JSONResponse:
    return register_user(username=username, password=password, email=email, db=db)
