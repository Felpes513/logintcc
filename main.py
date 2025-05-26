from fastapi import FastAPI
from app.adapters.web.email_controller import router as email_router
import uvicorn

__author__ = 'Rafael Ruiz da Silva 22/05/2025'

app = FastAPI()
app.include_router(email_router)

uvicorn.run(app, host='localhost', port=8001)
