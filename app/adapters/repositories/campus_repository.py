import pymysql
from app.dependencies.db import DB_CONFIG

def listar_campus():
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id_campus AS id, campus FROM tb_campus")
            return cursor.fetchall()  # retorna lista de dicionários
    finally:
        conn.close()

def buscar_campus_por_id(id_campus: int):
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id_campus AS id, campus FROM tb_campus WHERE id_campus = %s", (id_campus,))
            return cursor.fetchone()
    finally:
        conn.close()

def inserir_campus(nome: str):
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO tb_campus (campus) VALUES (%s)", (nome,))
            conn.commit()
            return cursor.lastrowid
    finally:
        conn.close()

def atualizar_campus(id_campus: int, novo_nome: str):
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            cursor.execute("UPDATE tb_campus SET campus = %s WHERE id_campus = %s", (novo_nome, id_campus))
            conn.commit()
            return cursor.rowcount
    finally:
        conn.close()

def deletar_campus(id_campus: int):
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM tb_campus WHERE id_campus = %s", (id_campus,))
            conn.commit()
            return cursor.rowcount
    finally:
        conn.close()
