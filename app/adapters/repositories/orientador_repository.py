from app.core.models.orientador import Orientador
from pymysql.err import IntegrityError

class OrientadorRepository:
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def create(self, orientador: Orientador) -> int:
        cursor = self.db_conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO tb_cadastro_orientador (nome_completo, email, cpf, senha_hash)
                VALUES (%s, %s, %s, %s)
            """, (
                orientador.nome_completo.lower(),
                orientador.email,
                orientador.cpf,
                orientador.senha_hash
            ))
            self.db_conn.commit()
            orientador_id = cursor.lastrowid

            # Se cursos foram enviados, associe
            for id_curso in orientador.cursos:
                cursor.execute("""
                    INSERT INTO tb_orientador_curso (id_orientador, id_curso)
                    VALUES (%s, %s)
                """, (orientador_id, id_curso))

            self.db_conn.commit()
            return orientador_id

        except IntegrityError as err:
            msg = str(err).lower()
            if "duplicate entry" in msg and "cpf" in msg:
                raise ValueError("CPF já cadastrado.")
            elif "duplicate entry" in msg and "email" in msg:
                raise ValueError("E-mail já cadastrado.")
            else:
                raise
