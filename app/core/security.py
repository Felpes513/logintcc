from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
import logging
from app.configs import settings

# Configuração mais robusta do contexto
pwd_context = CryptContext(
    schemes=["bcrypt"], 
    deprecated="auto",
    bcrypt__rounds=12,  # Especifica o número de rounds
)

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

SECRET_KEY = settings.SECRET_KEY

def gerar_hash_senha(senha: str) -> str:
    """Gera hash da senha com tratamento de erro"""
    try:
        return pwd_context.hash(senha)
    except Exception as e:
        logging.error(f"Erro ao gerar hash: {e}")
        raise

def verificar_senha(senha: str, senha_hash: str) -> bool:
    """Verifica senha com tratamento robusto de erros"""
    if not senha or not senha_hash:
        return False
    
    try:
        # Log para debug (remover em produção)
        logging.debug(f"Verificando senha. Hash: {senha_hash[:20]}...")
        
        result = pwd_context.verify(senha, senha_hash)
        logging.debug(f"Resultado da verificação: {result}")
        return result
        
    except Exception as e:
        logging.error(f"Erro ao verificar senha: {e}")
        
        # Fallback: tentar com bcrypt diretamente
        try:
            import bcrypt
            return bcrypt.checkpw(senha.encode('utf-8'), senha_hash.encode('utf-8'))
        except Exception as e2:
            logging.error(f"Erro no fallback bcrypt: {e2}")
            return False

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