from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from database.models import User
from utils import encrypt_password, is_password_valid

'''
def check_login(username: str, password: str, db: Session) -> bool:
    hashed_password = encrypt_password(password)
    user = db.query(User).filter(User.username == username , User.password == hashed_password).first()
    return bool(user)

def register_user(username: str, password: str, email: str, db: Session) -> JSONResponse:
    try:
        existing_user = db.query(User).filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            return JSONResponse(
                status_code=400,
                content={"message": "Username or email already exists"}
            )
        if check_password(password=password):
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
        return JSONResponse(
            status_code=400,
            content={"message": "Weak password"}  # TODO add reason
        )
    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=400,
            content={"message": "Something went wrong"}
        )
'''
def check_password(password: str) -> bool:
    return True
    # TODO Read file password configuration and check that the password is correctly defined







#login with policy password
#login with policy password
#login with policy password
from utils import load_password_policy

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
        password_policy = load_password_policy()
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









# TODO forgot password -> DOR
# TODO make sure uniqueness on register -> OMRI
# TODO STMP server for forgot password -> DOR
# TODO think about unsafe code
# TODO configuration file that checks password is met with requirements -> OMRI
