import os
import shutil
from pymysql.err import IntegrityError
from app.core.enums.status_inscricao import StatusInscricao



class InscricaoRepository:
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def criar_inscricao(self, id_projeto: int, id_aluno: int, pdf_path: str):
        cursor = self.db_conn.cursor()
        try:
            query = """
                INSERT INTO tb_inscricao_projeto (id_projeto, id_aluno, pdf_url)
                VALUES (%s, %s, %s)
            """
            cursor.execute(query, (id_projeto, id_aluno, pdf_path))
            self.db_conn.commit()
        except IntegrityError as err:
            if "Duplicate" in str(err):
                raise ValueError("Aluno já inscrito neste projeto.")
            raise err

    def listar_inscricoes_por_projeto(self, id_projeto: int):
        with self.db_conn.cursor() as cursor:
            query = """
                SELECT 
                    i.id_inscricao,
                    p.titulo_projeto AS nome_projeto,
                    o.nome_completo AS nome_orientador,
                    c.campus AS nome_campus,
                    a.nome_completo AS nome_aluno,
                    a.email,
                    i.status,
                    i.pdf_url
                FROM tb_inscricao_projeto i
                JOIN tb_novo_projeto p ON i.id_projeto = p.id_projeto
                JOIN tb_cadastro_orientador o ON p.id_orientador = o.id_orientador
                JOIN tb_campus c ON p.id_campus = c.id_campus
                JOIN tb_cadastro_aluno a ON i.id_aluno = a.id_aluno
                WHERE i.id_projeto = %s
            """
            cursor.execute(query, (id_projeto,))
            return cursor.fetchall()

    def aprovar_inscricao(self, id_inscricao: int):
        cursor = self.db_conn.cursor()

        # Atualiza o status para "SELECIONADO_ORIENTADOR"
        cursor.execute("""
            UPDATE tb_inscricao_projeto 
            SET status = %s 
            WHERE id_inscricao = %s
        """, (StatusInscricao.SELECIONADO_ORIENTADOR, id_inscricao))
        self.db_conn.commit()

        # Buscar o caminho do PDF
        cursor.execute("""
            SELECT pdf_url FROM tb_inscricao_projeto
            WHERE id_inscricao = %s
        """, (id_inscricao,))
        resultado = cursor.fetchone()

        if not resultado:
            raise ValueError("Inscrição não encontrada")

        pdf_path = resultado.get("pdf_url")
        if pdf_path and os.path.exists(pdf_path):
            try:
                os.remove(pdf_path)
            except Exception as e:
                print(f"⚠️ Falha ao remover o arquivo PDF: {e}")

    def excluir_inscricao(self, id_inscricao: int):
        cursor = self.db_conn.cursor()

        # Buscar o caminho do PDF
        cursor.execute("""
            SELECT pdf_url FROM tb_inscricao_projeto
            WHERE id_inscricao = %s
        """, (id_inscricao,))
        resultado = cursor.fetchone()

        if not resultado:
            raise ValueError("Inscrição não encontrada")

        # Extrair caminho do PDF
        pdf_path = resultado.get("pdf_url")
        if pdf_path and os.path.exists(pdf_path):
            try:
                os.remove(pdf_path)
                print(f"🗑️ PDF removido: {pdf_path}")
            except Exception as e:
                print(f"⚠️ Falha ao remover o arquivo PDF: {e}")

        # Excluir do banco
        cursor.execute("""
            DELETE FROM tb_inscricao_projeto
            WHERE id_inscricao = %s
        """, (id_inscricao,))
        self.db_conn.commit()
        print(f"✅ Inscrição com ID {id_inscricao} excluída do banco.")