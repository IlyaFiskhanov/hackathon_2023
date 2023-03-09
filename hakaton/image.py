import os
import cv2
import hashlib
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding

def compare_hashsum_image(filename):
    # Запросить у пользователя ввод хэш-суммы файла
    user_hashsum = input("Введите хэш-сумму файла: ")

    # Вычислить хэш-сумму файла
    file_hashsum = calculate_image_hash(filename)

    # Сравнить значения хэш-сумм
    if user_hashsum == file_hashsum:
        print("Хэш-суммы совпадают, файл не изменен")
    else:
        print("Хэш-суммы не совпадают, файл изменен")

def get_signature_image(signature_filename=None):
    """
    Запрашивает у пользователя ввод названия файла signature_image.txt,
    если signature_filename равно None. Если файл не существует, создает его.
    """
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

def calculate_image_hash_print(filename):
    
    hash = hashlib.sha256()
    with open(filename, 'rb') as f:
        while True:
            chunk = f.read(4096)
            if not chunk:
                break
            hash.update(chunk)
    print("Хэш-сумма изображения: ", hash.hexdigest())
    return hash.hexdigest()


def calculate_image_hash(filename):
    
    hash = hashlib.sha256()
    with open(filename, 'rb') as f:
        while True:
            chunk = f.read(4096)
            if not chunk:
                break
            hash.update(chunk)

    return hash.hexdigest()
    
def sign_image(filename, private_key, signature_filename=None):
    """
    Создание цифровой подписи файла
    """
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
    
def verify_image(filename, signature_filename, public_key, expected_hashsum):
    """
    Проверка подлинности цифровой подписи и хэш-суммы файла
    """
    with open(signature_filename, 'rb') as f:
        signature = f.read()
    hashsum = calculate_image_hash(filename)
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
        if hashsum == expected_hashsum:
            print("Файл оригинальный и подпись подлинна")
        else:
            print("Файл был изменен")
    except:
        print('Цифровая подпись недействительна')



def mark_image(image_filename, watermark_filename, output_filename, private_key):
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
    signature = sign_image(output_filename, private_key)

    # Сохранение цифровой подписи в файл
    with open(output_filename[:-4]+'_signature.txt', 'wb') as f:
        f.write(signature)
        f.close()

