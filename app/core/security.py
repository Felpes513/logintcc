from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from app.configs import settings  # pegar SECRET_KEY do settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

SECRET_KEY = settings.SECRET_KEY  # ✅ uso correto da chave via config centralizada

def gerar_hash_senha(senha):
    return pwd_context.hash(senha)

def verificar_senha(senha, senha_hash):
    return pwd_context.verify(senha, senha_hash)

def criar_token_acesso(dados: dict):
    dados_exp = dados.copy()
    expira = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    dados_exp.update({"exp": expira})
    return jwt.encode(dados_exp, SECRET_KEY, algorithm=ALGORITHM)

def criar_token_refresh(dados: dict):
    dados_exp = dados.copy()
    expira = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    dados_exp.update({"exp": expira})
    return jwt.encode(dados_exp, SECRET_KEY, algorithm=ALGORITHM)

def verificar_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token expirado")
    except jwt.PyJWTError:
        raise ValueError("Token inválido")
