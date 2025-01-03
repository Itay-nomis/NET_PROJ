from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from database.models import User
from utils import encrypt_password


def check_login(username: str, password: str, db: Session) -> bool:
    hashed_password = encrypt_password(password)
    user = db.query(User).filter(User.username == username and User.password == hashed_password).first()
    return bool(user)

def register_user(username: str, password: str, email: str, db: Session) -> JSONResponse:
    try:
        if check_password(password=password):
            user = User(username=username, email=email, password=encrypt_password(password))
            db.add(user)
            db.commit()
            db.refresh(user)
            return JSONResponse(status_code=201, content={"message": "User registered successfully"})
        return JSONResponse(status_code=400, content={"message": "Weak password"}) # TODO add reason
    except Exception as e:
        print(e)
        return JSONResponse(status_code=400, content={"message": "Something went wrong"})


def check_password(password: str) -> bool:
    pass
    # TODO Read file password configuration and check that the password is correctly defined


# TODO forgot password -> DOR
# TODO make sure uniqueness on register -> OMRI
# TODO STMP server for forgot password -> DOR
# TODO think about unsafe code
# TODO configuration file that checks password is met with requirements -> OMRI
