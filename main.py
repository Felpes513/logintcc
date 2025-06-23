from fastapi import FastAPI
from app.adapters.web.email_controller import router as email_router
from app.adapters.web.curso_controller import router as curso_controller
from app.adapters.web.aluno_controller import router as aluno_controller
from app.adapters.web.auth_controller import router as auth_controller


import uvicorn

__author__ = 'Rafael Ruiz da Silva 22/05/2025'

app = FastAPI()
app.include_router(email_router)
app.include_router(curso_controller)
app.include_router(aluno_controller)
app.include_router(auth_controller)

uvicorn.run(app, host='localhost', port=8001)
