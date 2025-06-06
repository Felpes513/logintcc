from app.core.models.aluno import Aluno
from pymysql.err import IntegrityError

class AlunoRepository:
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def create(self, aluno: Aluno) -> int:
        cursor = self.db_conn.cursor()

        try:
            query = """
            INSERT INTO tb_cadastro_aluno (nome_completo, email, cpf, id_curso)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (aluno.nome_completo.lower(), aluno.email, aluno.cpf, aluno.id_curso))
            self.db_conn.commit()
            return cursor.lastrowid

        except IntegrityError as err:
            error_msg = str(err).lower()
            if "duplicate entry" in error_msg and "cpf" in error_msg:
                raise ValueError("CPF já cadastrado.")

            elif "duplicate entry" in error_msg and "email" in error_msg:
                raise ValueError("E-mail já cadastrado.")

            elif "foreign key constraint fails" in error_msg:
                raise ValueError("ID do curso inválido.")

            else:
                raise
