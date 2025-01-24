from sqlalchemy.sql import text

from fastapi import Request


from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session

from starlette.responses import JSONResponse
from database.mysql_db import get_db, get_db_connection
from schemas import LoginRequest, RegisterRequest, ClientSchema
from services import check_login, register_user, get_login_attempts, login_attempts, password_policy, password_recovery, \
    verify_recovery_code, change_current_password, add_client, get_clients_by_user
import json
from fastapi.responses import Response
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.post("/register")
def register_user(
    username: str = Body(...),
    password: str = Body(...),
    email: str = Body(...)
):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = f"INSERT INTO users (username, password, email) VALUES ('{username}', '{password}', '{email}')"
    try:
        cursor.execute(query)
        connection.commit()
        return {"message": "User registered successfully"}
    except Exception as e:
        print(f"Error: {e}")
        return {"message": "Failed to register user"}
    finally:
        cursor.close()
        connection.close()



# login with policy password
@router.get("/login_attempts/{username}")
def get_attempts(username: str) -> JSONResponse:
    """
    API endpoint to get the number of failed login attempts for a user.
    """
    attempts = get_login_attempts(username)
    return JSONResponse(content={"username": username, "login_attempts": attempts}, status_code=200)


@router.post("/login")
def login(request: LoginRequest) -> JSONResponse:
    is_valid = check_login(username=request.username, password=request.password)

    if is_valid:
        return JSONResponse(content={"message": "Login successful"}, status_code=200)

    max_attempts = password_policy['LoginAttempts']
    remaining_attempts = max_attempts - login_attempts.get(request.username, 0)
    return JSONResponse(
        content={"message": f"Invalid username or password. {remaining_attempts} attempts remaining."},
        status_code=401
    )

@router.post("/forgot_password")
def forgot_password(email: str) -> JSONResponse:
    return password_recovery(email=email)

@router.post("/change_password_with_verify_code")
def change_password_with_verify_code(recovery_code: str, email: str, new_password: str) -> JSONResponse:
    if verify_recovery_code(recovery_code=recovery_code, email=email):
        return change_current_password(email=email, new_password=new_password)
    return JSONResponse(status_code=401, content={"message": "Invalid recovery code."})

@router.post("/change_password")
def change_password(email: str, new_password: str) -> JSONResponse:
    return change_current_password(email=email, new_password=new_password)

from pydantic import BaseModel

class ClientRequest(BaseModel):
    name: str
    email: str

@router.post("/add_client")
async def add_client(request: ClientSchema, db=Depends(get_db)):
    try:
        # יצירת שאילתה ללא הגנה לחלוטין
        query = f"INSERT INTO clients (name, email, user_id) VALUES ('{request.name}', '{request.email}', {1})"
        cursor = db.cursor()
        cursor.execute(query)  # ביצוע השאילתה
        db.commit()
        cursor.close()
        return JSONResponse(content={"message": "Client added successfully!"}, status_code=201)
    except Exception as e:
        return JSONResponse(content={"error": f"An error occurred: {str(e)}"}, status_code=500)




@router.get("/get_user_clients")
def get_user_clients(user_id: int) -> HTMLResponse:
    # קבלת הנתונים מהפונקציה
    clients = get_clients_by_user(user_id=user_id)

    # יצירת תוכן HTML
    response_content = "<br>".join([f"{client['name']} - {client['email']}" for client in clients])

    # החזרת התוכן כ-HTML
    return HTMLResponse(content=response_content, status_code=200)