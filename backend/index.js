const express = require('express');
const mysql = require('mysql2');
const cors = require('cors');

const app = express();
app.use(express.json());
app.use(cors()); // מאפשר תקשורת בין ה-frontend ל-backend

// הגדרות חיבור למסד הנתונים
const db = mysql.createConnection({
    host: 'mysql', // שם השירות בדוקר
    user: 'root',
    password: 'password', // הסיסמה כפי שמוגדרת בקובץ docker-compose.yml
    database: 'project', // שם מסד הנתונים
});

// בדיקת חיבור למסד הנתונים
db.connect((err) => {
    if (err) {
        console.error('Error connecting to MySQL:', err);
        process.exit(1);
    }
    console.log('Connected to MySQL database.');

    // יצירת טבלת users אם היא לא קיימת
    const createTableQuery = `
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    `;
    
    db.query(createTableQuery, (err, results) => {
        if (err) {
            console.error('Error creating users table:', err);
            return;
        }
        console.log('Users table created or already exists.');
    });
});

// נקודת קצה לאימות משתמש
app.post('/api/login', (req, res) => {
    const { username, password } = req.body;

    // בדיקת שם משתמש וסיסמה
    const query = 'SELECT * FROM users WHERE username = ? AND password = ?';
    db.query(query, [username, password], (err, results) => {
        if (err) {
            console.error('Error querying the database:', err);
            return res.status(500).json({ success: false, message: 'Server error' });
        }

        if (results.length > 0) {
            res.json({ success: true, message: 'Login successful' });
        } else {
            res.status(401).json({ success: false, message: 'Invalid credentials' });
        }
    });
});

// נקודת קצה לרישום משתמש
app.post('/api/register', (req, res) => {
    const { username, password, email } = req.body;

    // בדיקות נתונים
    if (!username || !password || !email) {
        return res.status(400).json({ success: false, message: 'All fields are required.' });
    }

    if (password.length < 10) {
        return res.status(400).json({ success: false, message: 'Password must be at least 10 characters long.' });
    }

    if (!email.includes('@')) {
        return res.status(400).json({ success: false, message: 'Invalid email address.' });
    }

    // בדוק אם שם המשתמש או האימייל כבר קיימים
    const checkUserQuery = 'SELECT * FROM users WHERE username = ? OR email = ?';
    db.query(checkUserQuery, [username, email], (err, results) => {
        if (err) {
            console.error('Error querying the database:', err);
            return res.status(500).json({ success: false, message: 'Database error.' });
        }

        if (results.length > 0) {
            // שם המשתמש או האימייל כבר קיימים
            return res.status(400).json({ success: false, message: 'Username or email already exists.' });
        }

        // הוספת משתמש למסד הנתונים
        const insertUserQuery = 'INSERT INTO users (username, password, email) VALUES (?, ?, ?)';
        db.query(insertUserQuery, [username, password, email], (err, results) => {
            if (err) {
                console.error('Error inserting user:', err);
                return res.status(500).json({ success: false, message: 'Database error.' });
            }
            res.status(201).json({ success: true, message: 'User registered successfully.' });
        });
    });
});

// נקודת קצה לשינוי סיסמה
app.post('/api/reset-password', (req, res) => {
    const { username, currentPassword, newPassword } = req.body;

    // בדוק אם שם המשתמש והסיסמה הנוכחית קיימים
    const query = 'SELECT * FROM users WHERE username = ? AND password = ?';
    db.query(query, [username, currentPassword], (err, results) => {
        if (err) {
            console.error('Error querying the database:', err);
            return res.status(500).json({ success: false, message: 'Database error.' });
        }

        if (results.length === 0) {
            // שם המשתמש או הסיסמה אינם נכונים
            return res.status(401).json({ success: false, message: 'Username or password is incorrect.' });
        }

        // בדוק אם הסיסמה החדשה עומדת בדרישות
        if (newPassword.length < 10) {
            return res.status(400).json({ success: false, message: 'Password must be at least 10 characters long.' });
        }

        // עדכן את הסיסמה במסד הנתונים
        const updateQuery = 'UPDATE users SET password = ? WHERE username = ?';
        db.query(updateQuery, [newPassword, username], (err, results) => {
            if (err) {
                console.error('Error updating password:', err);
                return res.status(500).json({ success: false, message: 'Database error.' });
            }
            res.status(200).json({ success: true, message: 'Password updated successfully.' });
        });
    });
});

// הפעלת השרת
const PORT = 5000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
