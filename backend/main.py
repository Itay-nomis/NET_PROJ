import uvicorn
from fastapi import FastAPI
from routes import router
from database.mysql_db import create_tables

app = FastAPI()
app.include_router(router)

@app.on_event("startup")
def startup_event():
    create_tables()


if __name__ == '__main__':
    uvicorn.run(app=app, host='0.0.0.0', port=5000)
