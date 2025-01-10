from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from schemas import LoginRequest, RegisterRequest
from services import check_login, register_user, get_login_attempts, login_attempts, password_policy
from database.mysql_db import get_db

router = APIRouter()

'''
@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)) -> JSONResponse:
    is_valid = check_login(username=request.username, password=request.password, db=db)
    if is_valid:
        return JSONResponse(content={"message": "Login successful"}, status_code=200)
    return JSONResponse(content={"message": "Invalid username or password"}, status_code=401)
'''

@router.post("/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)) -> JSONResponse:
    return register_user(
        username=request.username,
        password=request.password,
        email=request.email,
        db=db
    )


#login with policy password
#login with policy password
#login with policy password



@router.get("/login_attempts/{username}")
def get_attempts(username: str) -> JSONResponse:
    """
    API endpoint to get the number of failed login attempts for a user.
    """
    attempts = get_login_attempts(username)
    return JSONResponse(content={"username": username, "login_attempts": attempts}, status_code=200)


@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)) -> JSONResponse:
    """
    API endpoint for user login.
    """
    max_attempts = password_policy['LoginAttempts']

    if request.username in login_attempts and login_attempts[request.username] >= max_attempts:
        return JSONResponse(
            content={"message": "Account is locked. Too many login attempts."},
            status_code=403
        )

    is_valid = check_login(username=request.username, password=request.password, db=db)

    if is_valid:
        return JSONResponse(content={"message": "Login successful"}, status_code=200)

    remaining_attempts = max_attempts - login_attempts.get(request.username, 0)
    return JSONResponse(
        content={"message": f"Invalid username or password. {remaining_attempts} attempts remaining."},
        status_code=401
    )

