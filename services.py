import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from configuration import sender_email, sender_password
from database.mysql_db import get_db_connection
from utils import generate_random_string
from utils import load_password_policy

login_attempts = {}
email_to_recovery_password = {}
# Load the password policy from the ini file
password_policy = load_password_policy()

def check_login(username: str, password: str) -> bool:
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)
    user = cursor.fetchone()
    connection.close()

    if user:
        reset_login_attempts(username)
        return True

    increment_login_attempts(username)
    return False



def register_user(username: str, password: str, email: str):
    connection = get_db_connection()
    cursor = connection.cursor()

    # שאילתה פגיעה לשם הדגמת SQLi
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



def generate_recovery_code():
    return generate_random_string(6)


def password_recovery(email: str):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = f"SELECT * FROM users WHERE email = '{email}'"
    cursor.execute(query)
    user = cursor.fetchone()

    if not user:
        return {"message": "Email not found"}

    recovery_code = generate_recovery_code()
    email_to_recovery_password[email] = recovery_code

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = email
    message["Subject"] = "Your Recovery Password"
    message.attach(MIMEText(f"Your recovery password is: {recovery_code}", "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)
            return {"message": "Recovery password sent successfully"}
    except Exception as e:
        print(f"Failed to send email: {e}")
        return {"message": "Failed to send recovery password"}
    finally:
        cursor.close()
        connection.close()



def verify_recovery_code(recovery_code: str, email: str) -> bool:
    return email_to_recovery_password.get(email) == recovery_code


def change_current_password(email: str, new_password: str):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = f"UPDATE users SET password = '{new_password}' WHERE email = '{email}'"
    try:
        cursor.execute(query)
        connection.commit()
        return {"message": "Password changed successfully"}
    except Exception as e:
        print(f"Error: {e}")
        return {"message": "Failed to change password"}
    finally:
        cursor.close()
        connection.close()

def add_client(user_id: int, name: str, email: str):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Escape single quotes to prevent SQL syntax errors
    name = name.replace("'", "''")  # הכפלת גרשיים בודדים
    email = email.replace("'", "''")

    query = f"INSERT INTO clients (user_id, name, email) VALUES ('{user_id}', '{name}', '{email}')"
    try:
        cursor.execute(query)
        connection.commit()
        return {"message": "Client added successfully"}
    except Exception as e:
        print(f"Error: {e}")
        return {"message": "Failed to add client"}
    finally:
        cursor.close()
        connection.close()



def get_clients_by_user(user_id: int):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = f"SELECT * FROM clients WHERE user_id = {user_id}"
    try:
        cursor.execute(query)
        clients = cursor.fetchall()
        return clients
    except Exception as e:
        print(f"Error: {e}")
        return {"message": "Failed to fetch clients"}
    finally:
        cursor.close()
        connection.close()


def increment_login_attempts(username: str):
    login_attempts[username] = login_attempts.get(username, 0) + 1


def reset_login_attempts(username: str):
    if username in login_attempts:
        del login_attempts[username]


def get_login_attempts(username: str) -> int:
    return login_attempts.get(username, 0)
