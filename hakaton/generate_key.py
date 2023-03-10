
"""
Генерация пары ключей
"""
import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend 

PRIVATE_KEY_FILE = 'private_key.pem'
PUBLIC_KEY_FILE = 'public_key.pem'

def generate_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

def save_keys(private_key, public_key, private_key_file='private_key.pem', public_key_file='public_key.pem'):
    # Сохраняем закрытый ключ в файл
    with open(private_key_file, 'wb') as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))

    # Сохраняем открытый ключ в файл
    with open(public_key_file, 'wb') as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

def load_keys():
    if os.path.exists(PRIVATE_KEY_FILE) and os.path.exists(PUBLIC_KEY_FILE):
        # Загружаем закрытый ключ из файла
        with open(PRIVATE_KEY_FILE, 'rb') as f:
            private_key = load_pem_private_key(f.read(), password=None, backend=default_backend())
        # Загружаем открытый ключ из файла
        with open(PUBLIC_KEY_FILE, 'rb') as f:
            public_key = serialization.load_pem_public_key(f.read(), backend=default_backend())
    else:
        # Генерируем новую пару ключей
        private_key, public_key = generate_keys()
        # Сохраняем ключи в файлы
        save_keys(private_key, public_key, PRIVATE_KEY_FILE, PUBLIC_KEY_FILE)

    return private_key, public_key
