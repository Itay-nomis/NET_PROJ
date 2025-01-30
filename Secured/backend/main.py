import uvicorn
from fastapi import FastAPI
from routes import router
from database.mysql_db import create_tables
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # כתובת ה-Frontend
    allow_credentials=True,
    allow_methods=["*"],  # מתיר כל שיטות ה-HTTP
    allow_headers=["*"],  # מתיר כל ה-Headers
)
app.include_router(router)

@app.on_event("startup")
def startup_event():
    create_tables()


if __name__ == '__main__':
    uvicorn.run(app=app, host='0.0.0.0', port=5000)


