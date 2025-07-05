from app.core.models.projeto import Projeto
from pymysql.err import IntegrityError
import pymysql.cursors

class ProjetoRepository:
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def create(self, projeto: Projeto) -> int:
        cursor = self.db_conn.cursor()
        try:
            query = """INSERT INTO tb_novo_projeto(titulo_projeto,
                                                   resumo,
                                                   id_orientador,
                                                   id_campus) 
                       VALUES (%s, %s, %s, %s)"""
            cursor.execute(query, (projeto.titulo_projeto, projeto.resumo,
                                   projeto.id_orientador, projeto.id_campus))
            self.db_conn.commit()
            return cursor.lastrowid
        except IntegrityError as err:
            error_msg = str(err).lower()
            if "foreign key constraint fails" in error_msg:
                raise ValueError("ID do orientador e/ou ID do campus inválido(s).")

    def listar_todos(self):
        cursor = self.db_conn.cursor(pymysql.cursors.DictCursor)
        query = """
            SELECT 
                p.id_projeto,
                p.titulo_projeto AS nomeProjeto,
                p.resumo,
                c.campus,
                o.nome_completo AS nomeOrientador
            FROM tb_novo_projeto p
            LEFT JOIN tb_campus c ON p.id_campus = c.id_campus
            LEFT JOIN tb_cadastro_orientador o ON p.id_orientador = o.id_orientador
        """
        cursor.execute(query)
        return cursor.fetchall()

    def buscar_por_id(self, id_projeto: int):
        cursor = self.db_conn.cursor(pymysql.cursors.DictCursor)

        # 1. Buscar dados principais do projeto
        query = """
            SELECT 
                p.id_projeto,
                p.titulo_projeto AS nomeProjeto,
                p.resumo,
                p.id_orientador,
                o.email AS orientador_email,
                c.campus,
                c.id_campus,
                o.nome_completo AS nomeOrientador,
                p.quantidade_maxima_alunos AS quantidadeMaximaAlunos,
                p.data_criacao,
                p.data_atualizacao
            FROM tb_novo_projeto p
            LEFT JOIN tb_campus c ON p.id_campus = c.id_campus
            LEFT JOIN tb_cadastro_orientador o ON p.id_orientador = o.id_orientador
            WHERE p.id_projeto = %s
        """
        cursor.execute(query, (id_projeto,))
        projeto = cursor.fetchone()

        if not projeto:
            raise ValueError(f"Projeto com ID {id_projeto} não encontrado")

        # 2. Buscar alunos inscritos
        query_alunos = """
            SELECT 
                a.id_aluno AS id,
                a.nome_completo AS nome,
                a.email,
                i.pdf_url AS documentoNotasUrl
            FROM tb_inscricao_projeto i
            JOIN tb_cadastro_aluno a ON i.id_aluno = a.id_aluno
            WHERE i.id_projeto = %s
        """
        cursor.execute(query_alunos, (id_projeto,))
        alunos = cursor.fetchall()

        projeto["alunos"] = alunos
        projeto["nomesAlunos"] = [a["nome"] for a in alunos]

        return projeto



    def atualizar(self, id_projeto: int, projeto: Projeto):
        # Primeiro verifica se o projeto existe
        if not self._projeto_existe(id_projeto):
            raise ValueError(f"Projeto com ID {id_projeto} não encontrado")
        
        cursor = self.db_conn.cursor()
        try:
            query = """
                UPDATE tb_novo_projeto
                SET titulo_projeto = %s,
                    resumo = %s,
                    id_orientador = %s,
                    id_campus = %s
                WHERE id_projeto = %s
            """
            cursor.execute(query, (
                projeto.titulo_projeto,
                projeto.resumo,
                projeto.id_orientador,
                projeto.id_campus,
                id_projeto
            ))
            self.db_conn.commit()
        except IntegrityError as err:
            error_msg = str(err).lower()
            if "foreign key constraint fails" in error_msg:
                raise ValueError("ID do orientador e/ou ID do campus inválido(s).")

    def deletar(self, id_projeto: int):
        # Primeiro verifica se o projeto existe
        if not self._projeto_existe(id_projeto):
            raise ValueError(f"Projeto com ID {id_projeto} não encontrado")
        
        cursor = self.db_conn.cursor()
        query = "DELETE FROM tb_novo_projeto WHERE id_projeto = %s"
        cursor.execute(query, (id_projeto,))
        self.db_conn.commit()

    def _projeto_existe(self, id_projeto: int) -> bool:
        """Método auxiliar para verificar se um projeto existe"""
        cursor = self.db_conn.cursor()
        query = "SELECT 1 FROM tb_novo_projeto WHERE id_projeto = %s"
        cursor.execute(query, (id_projeto,))
        return cursor.fetchone() is not None