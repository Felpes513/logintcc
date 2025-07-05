import pymysql
from app.core.models.orientador import Orientador
from app.core.ports.output.porta_orientador_repository import IOrientadorRepository

class OrientadorRepository(IOrientadorRepository):
    def __init__(self, conn):
        self.conn = conn

    def create(self, orientador: Orientador) -> int:
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO tb_cadastro_orientador (nome_completo, email, senha_hash)
                    VALUES (%s, %s, %s)
                    """,
                    (orientador.nome_completo, orientador.email, orientador.senha_hash)
                )
                self.conn.commit()
                return cursor.lastrowid
        except pymysql.IntegrityError:
            raise ValueError("Orientador com esse e-mail já existe")

    def listar_orientadores(self):
        with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT id_orientador AS id, nome_completo, email FROM tb_cadastro_orientador")
            return cursor.fetchall()

    def buscar_por_nome(self, nome: str):
        with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(
                "SELECT id_orientador AS id, nome_completo, email FROM tb_cadastro_orientador WHERE nome_completo = %s",
                (nome,)
            )
            return cursor.fetchone()
