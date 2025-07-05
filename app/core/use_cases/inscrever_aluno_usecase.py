import os
import shutil
from fastapi import UploadFile

class InscreverAlunoUseCase:
    def __init__(self, repo):
        self.repo = repo

    def execute(self, id_projeto: int, id_aluno: int, pdf_file: UploadFile):
        pasta_destino = "app/static/pdfs"
        os.makedirs(pasta_destino, exist_ok=True)

        # Nome do arquivo salvo
        file_name = f"aluno_{id_aluno}_projeto_{id_projeto}.pdf"
        save_path = os.path.join(pasta_destino, file_name)

        # Salvar o arquivo PDF enviado
        try:
            with open(save_path, "wb") as buffer:
                shutil.copyfileobj(pdf_file.file, buffer)
        except Exception as e:
            raise Exception(f"Erro ao salvar o arquivo: {e}")

        # Salvar a inscrição no banco de dados
        self.repo.criar_inscricao(id_projeto, id_aluno, save_path)
