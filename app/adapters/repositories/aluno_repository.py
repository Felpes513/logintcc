from app.core.models.aluno import Aluno, AlunoSchema
from app.core.ports.output.porta_aluno_repository import IAlunoRepository


class AlunoRepository:
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def create(self, aluno: Aluno) -> int:
        cursor = self.db_conn.cursor()

        query = """
        INSERT INTO tb_cadastro_aluno (nome_completo, email, cpf, senha_hash, id_curso)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (
            aluno.nome_completo,
            aluno.email,
            aluno.cpf,
            aluno.senha_hash,
            aluno.id_curso
        )

        cursor.execute(query, values)
        self.db_conn.commit()
        return cursor.lastrowid

    def get_all(self):
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT id_aluno, nome_completo, email, cpf, id_curso FROM tb_cadastro_aluno")
        rows = cursor.fetchall()
        return [AlunoSchema(**row) for row in rows]

    def get_by_id(self, id_aluno: int):
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT id_aluno, nome_completo, email, cpf, id_curso FROM tb_cadastro_aluno WHERE id_aluno = %s", (id_aluno,))
        row = cursor.fetchone()
        if row:
            return AlunoSchema(**row)
        return None
