import hashlib
import base64

def generate_password_hash(password, salt, nonce, iterations):
    combined = password.encode('utf-8') + salt.encode('utf-8')
    hashed_password = hashlib.sha256(combined).digest()
    for _ in range(iterations - 1):
        combined = hashed_password + nonce.encode('utf-8')
        hashed_password = hashlib.sha256(combined).digest()
    return base64.b64encode(hashed_password).decode('utf-8')


# Параметры, предоставленные сервером
salt = "9v2tearEZ7T+3ljGywrtQQ=="
nonce = "YRlTDGjCmOnGqSlcB9ftfrhNjylZcA++5vQ5jyOAi19htfA0"
iterations = 4096

# Пароль пользователя
password = "admin"

# Генерация хеша пароля
password_hash = generate_password_hash(password, salt, nonce, iterations)

print("Хеш пароля:", password_hash)
