from app.core.models.secretaria import Secretaria
from pymysql.err import IntegrityError

class SecretariaRepository:
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def create(self, secretaria: Secretaria) -> int:
        cursor = self.db_conn.cursor()

        try:
            query = """
            INSERT INTO tb_cadastro_secretaria (nome_completo, email, senha_hash)
            VALUES (%s, %s, %s)
            """
            cursor.execute(query, (secretaria.nome_completo.lower(), secretaria.email, secretaria.senha_hash))
            self.db_conn.commit()
            return cursor.lastrowid

        except IntegrityError as err:
            error_msg = str(err).lower()
            if "duplicate entry" in error_msg and "email" in error_msg:
                raise ValueError("E-mail já cadastrado.")
            else:
                raise
