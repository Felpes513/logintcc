from app.core.models.curso import Curso
from app.core.ports.output.porta_curso_repository import ICursoRepository  # ✅ importa a interface

class CursoRepository(ICursoRepository):  # ✅ herda da interface
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def create(self, curso: Curso) -> int:
        cursor = self.db_conn.cursor()
        query = "INSERT INTO tb_curso (nome) VALUES (%s)"
        cursor.execute(query, (curso.nome,))
        self.db_conn.commit()
        return cursor.lastrowid

    def get_all(self) -> list[dict]:
        cursor = self.db_conn.cursor()
        query = "SELECT id_curso, nome FROM tb_curso"
        cursor.execute(query)
        rows = cursor.fetchall()
        return [{"id_curso": row["id_curso"], "nome": row["nome"]} for row in rows]
