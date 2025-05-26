# 📧 TccEmailApi

Sistema em Python para envio automatizado de e-mails personalizados a partir de uma planilha Excel.

---

## ✅ Requisitos

- Python **3.13.3**
- Git (opcional)
- Conexão com servidor SMTP (ex: Gmail)

---

## 📦 Instalação

### 1. Instale o `virtualenv`

Garanta que o `virtualenv` esteja instalado para o Python 3.13.3:

```bash
python3.13 -m pip install virtualenv
```

### 2. Crie o ambiente virtual

Substitua `<CAMINHO_PYTHON>` pelo caminho completo do Python 3.13.3:

```bash
virtualenv -p <CAMINHO_PYTHON> venv
```

> Exemplo:
> `virtualenv -p /usr/bin/python3.13 venv`

### 3. Ative o ambiente virtual

- No **Windows**:
  ```bash
  .\venv\Scripts\activate
  ```

- No **Linux/Mac**:
  ```bash
  source venv/bin/activate
  ```

### 4. Instale as dependências

```bash
pip install -r requirements.txt
```

---

## 📁 Estrutura do Projeto

```
UscsTCC/ 
├── app/
│   ├── adapters/
│   │   ├── web/                    
│   │   └── email/                 
│   ├── configs/                     
│   └── core/
│       ├── models/                 
│       ├── ports/
│       │   ├── input/              
│       │   └── output/             
│       └── use_cases/             
├── main.py
├── tests/
```

---

## ⚙️ Configuração

Antes de executar, crie um arquivo chamado `settings.py` na pasta `configs` do projeto com as configurações do servidor SMTP:

```python
SMTP_CONFIG = {
    "host": "smtp.gmail.com",
    "port": 587,
    "from": "seu_email@gmail.com",  # Substitua pelo seu e-mail
    "password": "sua_chave_de_aplicativo"  # Nunca use sua senha normal
}
```

> ⚠️ **Atenção**:
> - Não compartilhe esse arquivo publicamente.
> - **Não use sua senha de e-mail diretamente**.
> - Gere uma **senha de app** no [Google App Passwords](https://support.google.com/accounts/answer/185833?hl=pt-BR) caso use Gmail com autenticação em dois fatores.

---
## 🚀 Executando o app

Para executar o app, basta digitar no terminal com a venv ativada:
```bash
fastapi run main.py
```

## ▶️ Executando os testes

O projeto utiliza `pytest` para testes automatizados.

### 1. Instale o pytest e plugins:
**OBS:** (caso não tenha instalado o `requirements.txt`)
```bash
pip install pytest pytest-mock coverage
```

### 2. Execute os testes:

```bash
coverage run -m pytest tests
```

---

## 📫 Contato

Em caso de dúvidas, sugestões ou colaborações, entre em contato por e-mail:

- rafael.silva49@uscsonline.com.br
- felipe.moreira@uscsonline.com.br
---


## 📝 Licença

Este projeto está sob a licença MIT. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.
