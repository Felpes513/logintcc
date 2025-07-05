from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.adapters.web.email_controller import router as email_router
from app.adapters.web.curso_controller import router as curso_controller
from app.adapters.web.aluno_controller import router as aluno_controller
from app.adapters.web.auth_controller import router as auth_controller
from app.adapters.web.orientador_controller import router as orientador_controller
from app.adapters.web.secretaria_controller import router as secretaria_controller
from app.adapters.web.register_controller import router as register_router
from app.adapters.web.projeto_controller import router as projeto_router
from app.adapters.web.inscricao_projeto_controller import router as inscricao_router
from app.adapters.web.campus_controller import router as campus_router



import uvicorn

__author__ = 'Rafael Ruiz da Silva 22/05/2025'


app = FastAPI()

# ✅ Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas
app.include_router(email_router)
app.include_router(curso_controller)
app.include_router(aluno_controller)
app.include_router(auth_controller)
app.include_router(orientador_controller)
app.include_router(secretaria_controller)
app.include_router(register_router)
app.include_router(projeto_router)
app.include_router(inscricao_router)
app.include_router(campus_router)




# uvicorn.run(app, host='localhost', port=8001)
