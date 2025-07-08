import pandas as pd
from datetime import datetime
import os

def gerar_relatorio_alunos_aprovados(db):
    sql = """
        SELECT 
            a.nome_completo AS nome_aluno,
            a.matricula AS ra,
            p.titulo_projeto AS nome_projeto,
            p.numero_projeto,
            c.campus AS nome_campus
        FROM tb_inscricao_projeto ip
        JOIN tb_cadastro_aluno a ON a.id_aluno = ip.id_aluno
        JOIN tb_novo_projeto p ON p.id_projeto = ip.id_projeto
        JOIN tb_campus c ON c.id_campus = p.id_campus
        WHERE ip.status = 'CADASTRADO_FINAL'
    """

    with db.cursor() as cursor:
        cursor.execute(sql)
        colunas = [desc[0] for desc in cursor.description]
        dados = cursor.fetchall()

    df = pd.DataFrame(dados, columns=colunas)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    nome_arquivo = f"relatorio_alunos_aprovados_{timestamp}.xlsx"
    pasta_destino = "static/relatorios"
    os.makedirs(pasta_destino, exist_ok=True)
    caminho_arquivo = os.path.join(pasta_destino, nome_arquivo)

    df.to_excel(caminho_arquivo, index=False)
    return caminho_arquivo



def gerar_relatorio_projeto_especifico(db, titulo=None, orientador=None, numero_projeto=None):
    sql = """
        SELECT 
            p.titulo_projeto AS nome_projeto,
            p.numero_projeto,
            p.resumo AS descricao_projeto,
            p.data_criacao,
            o.nome_completo AS orientador,
            a.nome_completo AS aluno,
            c.campus AS campus
        FROM tb_novo_projeto p
        LEFT JOIN tb_cadastro_orientador o ON o.id_orientador = p.id_orientador
        LEFT JOIN tb_campus c ON c.id_campus = p.id_campus
        LEFT JOIN tb_inscricao_projeto ip ON ip.id_projeto = p.id_projeto AND ip.status = 'CADASTRADO_FINAL'
        LEFT JOIN tb_cadastro_aluno a ON a.id_aluno = ip.id_aluno
        WHERE 1=1
    """

    params = []

    if titulo:
        sql += " AND p.titulo_projeto LIKE %s"
        params.append(f"%{titulo}%")
    if orientador:
        sql += " AND o.nome_completo LIKE %s"
        params.append(f"%{orientador}%")
    if numero_projeto:
        sql += " AND p.numero_projeto = %s"
        params.append(numero_projeto)

    with db.cursor() as cursor:
        cursor.execute(sql, params)
        colunas = [desc[0] for desc in cursor.description]
        dados = cursor.fetchall()

    df = pd.DataFrame(dados, columns=colunas)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    nome_arquivo = f"relatorio_projeto_{timestamp}.xlsx"
    pasta_destino = "static/relatorios"
    os.makedirs(pasta_destino, exist_ok=True)
    caminho_arquivo = os.path.join(pasta_destino, nome_arquivo)

    df.to_excel(caminho_arquivo, index=False)
    return caminho_arquivo

def gerar_relatorio_todos_projetos(db):
    sql = """
        SELECT 
            p.titulo_projeto AS nome_projeto,
            p.numero_projeto,
            p.resumo AS descricao_projeto,
            o.nome_completo AS orientador,
            a.nome_completo AS aluno,
            c.campus AS campus
        FROM tb_novo_projeto p
        LEFT JOIN tb_cadastro_orientador o ON o.id_orientador = p.id_orientador
        LEFT JOIN tb_campus c ON c.id_campus = p.id_campus
        LEFT JOIN tb_inscricao_projeto ip ON ip.id_projeto = p.id_projeto AND ip.status = 'CADASTRADO_FINAL'
        LEFT JOIN tb_cadastro_aluno a ON a.id_aluno = ip.id_aluno
        ORDER BY p.numero_projeto
    """

    with db.cursor() as cursor:
        cursor.execute(sql)
        colunas = [desc[0] for desc in cursor.description]
        dados = cursor.fetchall()

    df = pd.DataFrame(dados, columns=colunas)

    from datetime import datetime
    import os
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    nome_arquivo = f"relatorio_todos_projetos_{timestamp}.xlsx"
    pasta_destino = "static/relatorios"
    os.makedirs(pasta_destino, exist_ok=True)
    caminho_arquivo = os.path.join(pasta_destino, nome_arquivo)

    df.to_excel(caminho_arquivo, index=False)
    return caminho_arquivo