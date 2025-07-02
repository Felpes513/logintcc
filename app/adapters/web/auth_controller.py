from fastapi import APIRouter, Depends, HTTPException, status
from app.core.security import verificar_senha, criar_token_acesso, criar_token_refresh, verificar_token
from app.dependencies.db import get_db_conn
from app.core.security import ALGORITHM, SECRET_KEY
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db_conn)):
    email = form_data.username
    senha = form_data.password

    cursor = db.cursor()
    
    # Consulta SQL
    cursor.execute("SELECT id_aluno, senha_hash FROM tb_cadastro_aluno WHERE email = %s", (email,))
    result = cursor.fetchone()

    if not result:
        print(f"❌ Nenhum registro encontrado para: {email}")
        raise HTTPException(status_code=401, detail="Usuário não encontrado")

    aluno_id = result['id_aluno']
    senha_hash = result['senha_hash']

    # ===== LOGS DE DEBUG (REMOVER EM PRODUÇÃO) =====
    print(f"🔍 DEBUG LOGIN:")
    print(f"   Email: {email}")
    print(f"   Senha informada: '{senha}'")
    print(f"   Senha hash do banco: '{senha_hash}'")
    print(f"   Tamanho do hash: {len(senha_hash)} caracteres")
    print(f"   Hash começa com $2b$: {senha_hash.startswith('$2b$')}")
    print(f"   Hash completo válido: {len(senha_hash) == 60}")
    print(f"   Aluno ID: {aluno_id}")
    print(f"   Tipo do aluno_id: {type(aluno_id)}")
    print(f"   Tipo do senha_hash: {type(senha_hash)}")
    
    # Verificar se há espaços em branco ou caracteres estranhos
    senha_hash_limpo = senha_hash.strip()
    print(f"   Hash após strip: '{senha_hash_limpo}'")
    print(f"   Hash mudou após strip: {senha_hash != senha_hash_limpo}")
    
    # Tentar a verificação com logs
    try:
        print(f"   Tentando verificar senha...")
        resultado_verificacao = verificar_senha(senha, senha_hash_limpo)
        print(f"   Resultado da verificação: {resultado_verificacao}")
        
        if not resultado_verificacao:
            print("   ❌ Senha incorreta - gerando novo hash para comparação")
            from app.core.security import gerar_hash_senha
            novo_hash = gerar_hash_senha(senha)
            print(f"   Novo hash gerado: {novo_hash}")
            print(f"   Novo hash funciona: {verificar_senha(senha, novo_hash)}")
            
            raise HTTPException(status_code=401, detail="Senha incorreta")
        else:
            print("   ✅ Senha correta!")
            
    except Exception as e:
        print(f"   ❌ ERRO na verificação: {e}")
        print(f"   Tipo do erro: {type(e)}")
        raise HTTPException(status_code=401, detail="Erro na autenticação")
    # ===== FIM DOS LOGS DE DEBUG =====

    access_token = criar_token_acesso({"sub": str(aluno_id)})
    refresh_token = criar_token_refresh({"sub": str(aluno_id)})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/login-orientador")
def login_orientador(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db_conn)):
    email = form_data.username
    senha = form_data.password

    cursor = db.cursor()
    
    # Consulta SQL
    cursor.execute("SELECT id_orientador, senha_hash FROM tb_cadastro_orientador WHERE email = %s", (email,))
    result = cursor.fetchone()

    if not result:
        print(f"❌ Nenhum registro encontrado para orientador: {email}")
        raise HTTPException(status_code=401, detail="Usuário não encontrado")

    id_orientador = result['id_orientador']
    senha_hash = result['senha_hash']

    # ===== LOGS DE DEBUG (REMOVER EM PRODUÇÃO) =====
    print(f"🔍 DEBUG LOGIN ORIENTADOR:")
    print(f"   Email: {email}")
    print(f"   Senha informada: '{senha}'")
    print(f"   Senha hash do banco: '{senha_hash}'")
    print(f"   Tamanho do hash: {len(senha_hash)} caracteres")
    print(f"   Hash começa com $2b$: {senha_hash.startswith('$2b$')}")
    print(f"   Hash completo válido: {len(senha_hash) == 60}")
    print(f"   Orientador ID: {id_orientador}")
    print(f"   Tipo do id_orientador: {type(id_orientador)}")
    print(f"   Tipo do senha_hash: {type(senha_hash)}")
    
    # Verificar se há espaços em branco ou caracteres estranhos
    senha_hash_limpo = senha_hash.strip()
    print(f"   Hash após strip: '{senha_hash_limpo}'")
    print(f"   Hash mudou após strip: {senha_hash != senha_hash_limpo}")
    
    # Tentar a verificação com logs
    try:
        print(f"   Tentando verificar senha...")
        resultado_verificacao = verificar_senha(senha, senha_hash_limpo)
        print(f"   Resultado da verificação: {resultado_verificacao}")
        
        if not resultado_verificacao:
            print("   ❌ Senha incorreta - gerando novo hash para comparação")
            from app.core.security import gerar_hash_senha
            novo_hash = gerar_hash_senha(senha)
            print(f"   Novo hash gerado: {novo_hash}")
            print(f"   Novo hash funciona: {verificar_senha(senha, novo_hash)}")
            
            raise HTTPException(status_code=401, detail="Senha incorreta")
        else:
            print("   ✅ Senha correta!")
            
    except Exception as e:
        print(f"   ❌ ERRO na verificação: {e}")
        print(f"   Tipo do erro: {type(e)}")
        raise HTTPException(status_code=401, detail="Erro na autenticação")
    # ===== FIM DOS LOGS DE DEBUG =====

    access_token = criar_token_acesso({"sub": str(id_orientador)})
    refresh_token = criar_token_refresh({"sub": str(id_orientador)})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/login-secretaria")
def login_secretaria(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db_conn)):
    email = form_data.username
    senha = form_data.password

    cursor = db.cursor()
    cursor.execute("SELECT id_secretaria, senha_hash FROM tb_cadastro_secretaria WHERE email = %s", (email,))
    result = cursor.fetchone()

    if not result:
        print(f"❌ Nenhum registro encontrado para secretaria: {email}")
        raise HTTPException(status_code=401, detail="Usuário não encontrado")

    id_secretaria = result['id_secretaria']
    senha_hash = result['senha_hash']

    # ===== LOGS DE DEBUG (REMOVER EM PRODUÇÃO) =====
    print(f"🔍 DEBUG LOGIN SECRETARIA:")
    print(f"   Email: {email}")
    print(f"   Senha informada: '{senha}'")
    print(f"   Senha hash do banco: '{senha_hash}'")
    print(f"   Tamanho do hash: {len(senha_hash)} caracteres")
    print(f"   Hash começa com $2b$: {senha_hash.startswith('$2b$')}")
    print(f"   Hash completo válido: {len(senha_hash) == 60}")
    print(f"   Secretaria ID: {id_secretaria}")
    print(f"   Tipo do id_secretaria: {type(id_secretaria)}")
    print(f"   Tipo do senha_hash: {type(senha_hash)}")

    senha_hash_limpo = senha_hash.strip()
    print(f"   Hash após strip: '{senha_hash_limpo}'")
    print(f"   Hash mudou após strip: {senha_hash != senha_hash_limpo}")

    try:
        print(f"   Tentando verificar senha...")
        resultado_verificacao = verificar_senha(senha, senha_hash_limpo)
        print(f"   Resultado da verificação: {resultado_verificacao}")

        if not resultado_verificacao:
            print("   ❌ Senha incorreta - gerando novo hash para comparação")
            from app.core.security import gerar_hash_senha
            novo_hash = gerar_hash_senha(senha)
            print(f"   Novo hash gerado: {novo_hash}")
            print(f"   Novo hash funciona: {verificar_senha(senha, novo_hash)}")

            raise HTTPException(status_code=401, detail="Senha incorreta")
        else:
            print("   ✅ Senha correta!")

    except Exception as e:
        print(f"   ❌ ERRO na verificação: {e}")
        print(f"   Tipo do erro: {type(e)}")
        raise HTTPException(status_code=401, detail="Erro na autenticação")

    # ===== FIM DOS LOGS DE DEBUG =====

    access_token = criar_token_acesso({"sub": str(id_secretaria)})
    refresh_token = criar_token_refresh({"sub": str(id_secretaria)})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = verificar_token(token)
        return payload["sub"]
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

@router.post("/refresh-token")
def refresh_token(refresh_token: str):
    try:
        payload = verificar_token(refresh_token)
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Refresh token inválido")
        novo_access_token = criar_token_acesso({"sub": user_id})
        return {"access_token": novo_access_token, "token_type": "bearer"}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

# --- Exemplo de rota protegida ---
@router.get("/me")
def get_user_logado(user_id: int = Depends(get_current_user)):
    return {"mensagem": f"Você está autenticado como aluno ID {user_id}"}