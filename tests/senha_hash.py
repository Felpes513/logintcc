import bcrypt

senha = "123456"  # senha que o usuário vai usar
hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt())
print(hash.decode())
