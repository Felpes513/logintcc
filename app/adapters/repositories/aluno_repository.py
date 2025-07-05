from app.core.models.aluno import AlunoSchema

class AlunoRepository:
    def __init__(self, db_conn):
        self.db_conn = db_conn

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
