import os
import cv2
import hashlib
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.exceptions import InvalidSignature
"""
    Функция compare_hashsum_image сравнивает хэш-сумму, введенную пользователем, с хэш-суммой файла, вычисленной с помощью функции 
"""
def compare_hashsum_image(filename, user_hashsum):
    # Вычислить хэш-сумму файла
    print(user_hashsum)
    file_hashsum = calculate_image_hash(filename)
    # Сравнить значения хэш-сумм
    if user_hashsum == file_hashsum:
        return "Хэш-суммы совпадают, файл не изменен"
    else:
        return "Хэш-суммы не совпадают, файл изменен"
"""
    Запрашивает у пользователя ввод названия файла signature_image.txt,
    если signature_filename равно None. Если файл не существует, создает его.
"""
def get_signature_image(signature_filename=None):
    if signature_filename is None:
        signature_filename = input("Введите название файла для цифровой подписи (например, signature_image.txt): ")
    file = None
    try:
        file = open(signature_filename, 'r')
        # чтение содержимого файла, если оно нужно
    except FileNotFoundError:
        open(signature_filename, 'w').close()
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        if file is not None:
            file.close()
    return signature_filename
"""
    Функция calculate_image_hash_print(filename) вычисляет хэш-сумму заданного файла filename
"""
def calculate_image_hash_print(filename):
    hash = hashlib.sha256()
    with open(filename, 'rb') as f:
        while True:
            chunk = f.read(4096)
            if not chunk:
                break
            hash.update(chunk)
    print("Хэш-сумма изображения: ", hash.hexdigest())
    # Спрашиваем у пользователя, нужно ли сохранить хэш-сумму в файл

    # Запрашиваем у пользователя имя файла для сохранения хэш-суммы
    output_filename = 'hash_summa.txt'
    with open(output_filename, 'w') as f:
        f.write(hash.hexdigest())
    return hash.hexdigest()

"""
    Расчет хэш-сумму файла
"""
def calculate_image_hash(filename):
    hash = hashlib.sha256()
    with open(filename, 'rb') as f:
        while True:
            chunk = f.read(4096)
            if not chunk:
                break
            hash.update(chunk)

    return hash.hexdigest()
"""
    Создание цифровой подписи файла
"""   
def sign_image(filename, private_key, signature_filename=None):
    
    signature_filename = get_signature_image(signature_filename)
    signature = calculate_image_hash(filename)
    with open(filename, 'rb') as f:
        data = f.read()
    signature = private_key.sign(
        data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    with open(signature_filename, 'wb') as f:
        f.write(signature)
    f.close()
    return signature
"""
    Проверка подлинности цифровой подписи и хэш-суммы файла
"""    
def verify_image(filename, signature_filename, public_key, expected_hashsum=None):
   
    with open(signature_filename, 'rb') as f:
        signature = f.read()
    # Запрашиваем у пользователя ввод хэш-суммы из файла или вручную
    hash_input = 'hash_summa.txt'
    # Проверяем, является ли введенное значение именем файла
    if os.path.isfile(hash_input):
        with open(hash_input, 'r') as f:
            hashsum = f.read().strip()

    else:
        hashsum = hash_input
    print(hashsum)
    actual_hashsum = calculate_image_hash(filename)
    with open(filename, 'rb') as f:
        data = f.read()


    try:
        public_key.verify(
            signature,
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        if hashsum == actual_hashsum:
            return "Файл оригинальный и подпись подлинна"
        else:
            return "Файл был изменен"
    except InvalidSignature:
       return'Файл был изменен \nИли цифровая подпись недействительна'

"""
    Наложение водяного знака на видео и создание цифровой подписи
"""
def mark_image(image_filename, watermark_filename, private_key):
    output_filename = image_filename.split('.')[0] + "_new_with_mark.jpg"
    image = cv2.imread(image_filename)
    watermark = cv2.imread(watermark_filename)
    # Получить размеры изображений
    image_height, image_width, _ = image.shape
    watermark_height, watermark_width, _ = watermark.shape
    # Вычислить координаты для размещения водяного знака
    x = image_width - watermark_width - 10
    y = image_height - watermark_height - 10
    # Наложить водяной знак на изображение
    image[y:y+watermark_height, x:x+watermark_width] = watermark
    # Сохранить изображение с водяным знаком
    cv2.imwrite(output_filename, image)
    # Создание цифровой подписи для изображения с водяным знаком
    signature = sign_image(output_filename, private_key, 'signature_image.txt')

   

