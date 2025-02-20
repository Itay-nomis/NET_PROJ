import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from schemas import ClientSchema
from database.models import User, Client
from utils import encrypt_password, is_password_valid

# login with policy password
from utils import load_password_policy
from configuration import *

# Load the password policy from the ini file
password_policy = load_password_policy()


def check_login(username: str, password: str, db: Session) -> bool:
    max_attempts = password_policy['LoginAttempts']  # Load the max login attempts from policy

    # Check if the user has exceeded the max attempts
    if username in login_attempts and login_attempts[username] >= max_attempts:
        print(f"User {username} is locked due to too many login attempts.")
        return False  # Account is locked

    hashed_password = encrypt_password(password)  # Encrypt the provided password
    user = db.query(User).filter(User.username == username, User.password == hashed_password).first()

    if user:
        reset_login_attempts(username)  # Reset attempts on successful login
        return True

    # Increment failed attempts
    increment_login_attempts(username)
    remaining_attempts = max_attempts - login_attempts[username]
    print(f"Invalid login. {remaining_attempts} attempts remaining for {username}.")
    return False


login_attempts = {}  # Dictionary to track login attempts for each user
email_to_recovery_password = {}


def get_login_attempts(username: str) -> int:
    """
    Get the current number of failed login attempts for a specific user.
    """
    return login_attempts.get(username, 0)


def reset_login_attempts(username: str):
    """
    Reset the login attempts counter for a user.
    """
    if username in login_attempts:
        login_attempts.pop(username)


def increment_login_attempts(username: str):
    """
    Increment the login attempts counter for a user.
    """
    login_attempts[username] = login_attempts.get(username, 0) + 1


def register_user(username: str, password: str, email: str, db: Session) -> JSONResponse:
    try:
        existing_user = db.query(User).filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            return JSONResponse(
                status_code=400,
                content={"message": "Username or email already exists"}
            )

        # Validate password
        if not is_password_valid(password, password_policy):
            return JSONResponse(
                status_code=400,
                content={"message": "Password does not meet the policy requirements"}
            )

        # Create new user
        user = User(
            username=username,
            email=email,
            password=encrypt_password(password)
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return JSONResponse(
            status_code=201,
            content={"message": "User registered successfully"}
        )

    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=400,
            content={"message": "Something went wrong"}
        )


# Function to generate a 6-digit recovery code
def generate_recovery_code():
    return encrypt_password(str(random.randint(100000, 999999)))


def password_recovery(email: str, db : Session):
    if not db.query(User).filter((User.email == email)).first():
        return False
    recovery_code = generate_recovery_code()
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = email
    message["Subject"] = "Your Recovery Password"
    message.attach(MIMEText(f"Your recovery password is: {recovery_code}", "plain"))
    try:
        # Establish connection to the SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, sender_password)
            server.send_message(message)
            print(f"Recovery email sent to {email}")
            email_to_recovery_password[email.lower()] = recovery_code
            return JSONResponse(status_code=200, content={"message": "Recovery password sent successfully"})
    except Exception as e:
        print(f"Failed to send email: {e}")
        return JSONResponse(status_code=400, content={"message": "Something went wrong"})


def verify_recovery_code(recovery_code: str, email: str):
    if email_to_recovery_password.get(email.lower()) == recovery_code:
        return True
    return False


def change_current_password(email: str, new_password: str, db: Session):
    if is_password_valid(new_password, password_policy):
        try:
            user = db.query(User).filter(User.email == email).first()
            user.password = encrypt_password(new_password)
            db.commit()
            email_to_recovery_password.pop(email, None)
            return JSONResponse(status_code=200, content={"message": "Password changed successfully"})
        except Exception as e:
            print(e)
            return JSONResponse(status_code=400, content={"message": "Something went wrong"})
    return JSONResponse(status_code=400, content={"message": "Weak password"})


def add_client(client: ClientSchema, user_id: int, db: Session):
    if not db.query(Client).filter(Client.email == client.email).first():
        new_client = Client(user_id=user_id, name=client.name, email=client.email)
        db.add(new_client)
        db.commit()
        db.refresh(new_client)
        return JSONResponse(status_code=200, content={"message": "Client added successfully"})
    return JSONResponse(status_code=400, content={"message": "Client already exists"})

def get_clients_by_user(user_id: int, db: Session):
    return db.query(Client).filter(Client.user_id == user_id).all()
