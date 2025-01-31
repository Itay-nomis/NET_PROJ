קישור ל-GIT של הפרויקט:
https://github.com/Itay-nomis/NET_PROJ

הפרויקט כולל ממשקי Frontend ו-Backend המאפשרים רישום משתמשים, התחברות, איפוס סיסמה והוספה וצפיה בלקוחות. הפרויקט משתמש ב-React עבור ה-Frontend וב-FastAPI עבור ה-Backend, יחד עם MySQL כמסד נתונים.
טכנולוגיות ושפות תכנות:
• Frontend: React, JavaScript, CSS
• Backend: FastAPI, Python, SQLAlchemy
• Database: MySQL
• Containerization: Docker, Docker Compose
סיסמא ל-מסד הנתונים: password
מבנה הפרויקט
תחת ה-ROOT של הפרויקט קיימות 2 תיקיות Secured ו-Not-Secured ההבדל הוא רמת האבטחה - בתוך כל אחת תמצא את המבנה הבא:
project/
├── backend/
│   ├── main.py                 # קובץ ההרצה הראשי של ה-Backend
│   ├── routes.py               # ניהול נתיבי ה-API
│   ├── models.py               # הגדרת המודלים למסד הנתונים
│   ├── utils.py                # פונקציות עזר
│   ├── services.py             # פונקציות הלוגיקה העסקית
│   ├── password_configuration  # קובץ הגדרות סיסמאות
│   ├── requirements.txt        # רשימת התלויות של ה-Backend
│   ├── Dockerfile              # קובץ Docker עבור ה-Backend
│     ├── docker-compose.yml      # קובץ ניהול השירותים ב-Docker Compose
│     ├── database/
│     │    ├── mysql_db.py             # קובץ ניהול מסד הנתונים ב-Backend
│     │    ├── models.py               # 
├── frontend/
│   ├── src/
│   │   ├── App.js              # קובץ ה-Root של ה-Frontend
│   │   ├── index.js            # נקודת הכניסה ל-Frontend
│   │   ├── config.js           # קובץ תצורה ל-Frontend
│   │   ├── pages/              # עמודים באפליקציה
│   │   │   ├── Login.js
│   │   │   ├── Register.js
│   │   │   ├── System.js
│   │   │   ├── ForgotPassword.js
│   │   │   ├── ResetPassword.js
│   │   ├── styles/             # קבצי עיצוב
│   │   │   ├── login.css
│   │   │   ├── register.css
│   │   │   ├── resetPassword.css
│   │   ├── components/         # רכיבי UI חוזרים
├── database/
│     ├── package-lock.json
│   ├── package.json            # תלויות ה-Frontend
│     ├── Dockerfile              # קובץ Docker עבור ה-Frontend
├── README.md                   # קובץ זה
התקנת והפעלת הפרויקט:
דרישות מערכת
• Docker & Docker Compose מותקנים
• Node.js & npm (במידה ולא משתמשים ב-Docker להרצת ה-Frontend)
• Python 3.9+ & pip (במידה ולא משתמשים ב-Docker להרצת ה-Backend)
הפעלת הפרויקט באמצעות Docker
1. ודא ש-Docker מותקן ומופעל במחשב שלך.
2. נווט לתיקייה backend תחת הפרויקט והפעל את הפקודה הבאה: 
3. docker-compose up --build
4. ה-Backend יהיה זמין בכתובת:
http://localhost:5000/docs
5. ה-Frontend יהיה זמין בכתובת:
http://localhost:3000

נתיבי API עיקריים
• POST /register – רישום משתמש חדש
• POST /login – התחברות
• POST /forgot-password – איפוס סיסמה
• GET /system – קבלת נתוני מערכת (דורש התחברות)
פרטי יוצרי הפרויקט:
יאנה סלדקוב, איתי סימון, דור מיטניק ועומרי גומל
קישור ל-GIT של הפרויקט:
https://github.com/Itay-nomis/NET_PROJ