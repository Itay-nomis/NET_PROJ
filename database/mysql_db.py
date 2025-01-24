import mysql.connector

# פונקציה לחיבור למסד הנתונים
def get_db_connection():
    return mysql.connector.connect(
        host="mysql",  # או 'mysql' עבור Docker
        user="root",
        password="password",
        database="project",

    )
    # פונקציה לחיבור מסד נתונים באמצעות context manager (yield)
def get_db():
    db = get_db_connection()
    try:
        yield db
    finally:
        db.close()

# פונקציה ליצירת טבלאות
def create_tables():
    connection = get_db_connection()
    cursor = connection.cursor()

    # יצירת טבלת המשתמשים
    create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) UNIQUE NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL
    );
    """
    cursor.execute(create_users_table)

    # יצירת טבלת הלקוחות
    create_clients_table = """
    CREATE TABLE IF NOT EXISTS clients (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """
    cursor.execute(create_clients_table)

    print("Tables created successfully.")
    connection.commit()
    cursor.close()
    connection.close()
