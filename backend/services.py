import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from sqlalchemy import and_
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from database.models import User
from utils import encrypt_password

# HARDCODED VARIABLES (MAY MOVE TO CONF FILE)
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 465
EMAIL_ADDRESS = '<EMAIL>'
EMAIL_PASSWORD = '<PASSWORD>'


def check_login(username: str, password: str, db: Session) -> bool:
    hashed_password = encrypt_password(password)
    user = db.query(User).filter(and_(User.username == username, User.password == hashed_password)).first()
    return bool(user)


def register_user(username: str, password: str, email: str, db: Session) -> JSONResponse:
    try:
        if check_password(password=password):
            user = User(username=username, email=email, password=encrypt_password(password))
            db.add(user)
            db.commit()
            db.refresh(user)
            return JSONResponse(status_code=201, content={"message": "User registered successfully"})
        return JSONResponse(status_code=400, content={"message": "Weak password"})  # TODO add reason
    except Exception as e:
        print(e)
        return JSONResponse(status_code=400, content={"message": "Something went wrong"})


def check_password(password: str) -> bool:
    return True
    # TODO Read file password configuration and check that the password is correctly defined


def send_recovery_code(email: str):
    recovery_code = f"{random.randint(100000, 99999)}"

    subject = "Password recovery code"
    body = "Your password recovery code is {recovery_code}"

    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = email
    msg['Subject'] = subject
    msg.attach(MIMEText(body))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        return recovery_code
    except Exception as e:
        print(f"Failed to send mail: {e}")
        return JSONResponse(status_code=400, content={"message": "Something went wrong"})

# TODO forgot password -> DOR
# TODO make sure uniqueness on register -> OMRI
# TODO STMP server for forgot password -> DOR
# TODO think about unsafe code
# TODO configuration file that checks password is met with requirements -> OMRI
