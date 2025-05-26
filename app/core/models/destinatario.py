from datetime import datetime, date

class Destinatario:
    def __init__(self, name: str, email: str, cpf: str,
                 data_conclusao: date, ciclo: str
                 ):
        self.name = name
        self.email = email
        self.cpf = cpf
        self.data_conclusao = data_conclusao
        self.ciclo = ciclo
        self.data_atual = datetime.now().date()
