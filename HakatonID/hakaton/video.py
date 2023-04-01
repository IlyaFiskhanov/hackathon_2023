import os
import cv2
import hashlib
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
"""
    Функция compare_hashsum_image сравнивает хэш-сумму, введенную пользователем, с хэш-суммой файла, вычисленной с помощью функции 
"""
def compare_hashsum_video(filename, user_hashsum):
    # Запросить у пользователя ввод хэш-суммы файла
    print(user_hashsum)
    # Вычислить хэш-сумму файла
    file_hashsum = calculate_video_hash(filename)
    # Сравнить значения хэш-сумм
    if user_hashsum == file_hashsum:
        return"Хэш-суммы совпадают, файл не изменен"
    else:
        return"Хэш-суммы не совпадают, файл изменен"
"""
    Запрашивает у пользователя ввод названия файла signature_image.txt,
    если signature_filename равно None. Если файл не существует, создает его.
"""
def get_signature_video(signature_filename=None):
   
    if signature_filename is None:
        signature_filename = input("Введите название файла для цифровой подписи (например, signature_image.txt): ")
    if signature_filename is not None and not os.path.isfile(signature_filename):
        open(signature_filename, 'w').close()
    return signature_filename
"""
    Функция calculate_image_hash_print(filename) вычисляет хэш-сумму заданного файла filename
"""
def calculate_video_hash_print(filename):
    """
    Вычисление хэш-суммы видео-файла
    """
    hash = hashlib.sha256()
    with open(filename, 'rb') as f:
        while True:
            chunk = f.read(4096)
            if not chunk:
                break
            hash.update(chunk)
    print("Хэш-сумма изображения: ", hash.hexdigest())

    output_filename = 'hash_summa.txt'
    with open(output_filename, 'w') as f:
        f.write(hash.hexdigest())
    return hash.hexdigest()



"""
    Расчет хэш-сумму файла
"""
def calculate_video_hash(filename):
    """
    Вычисление хэш-суммы видео-файла
    """
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
def sign_video(filename, private_key,signature_filename=None):

    signature_filename = get_signature_video(signature_filename)
    signature = calculate_video_hash(filename)
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
    return signature
"""
    Проверка подлинности цифровой подписи и хэш-суммы файла
"""
def verify_video(filename, signature_filename, public_key, expected_hashsum=None):
    
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
    
    # Вычисляем хэш-сумму файла
    actual_hashsum = calculate_video_hash(filename)
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
            return"Файл оригинальный и подпись подлинна"
        else:
            return"Файл был изменен"
    except:
        return'Файл был изменен \nИли цифровая подпись недействительна'

"""
    Наложение водяного знака на видео и создание цифровой подписи
"""
def mark_video(video_filename, watermark_filename, private_key):
    output_filename = video_filename.split('.')[0] + "_new_with_mark.mp4"
    # Загрузка видео и водяного знака
    video = cv2.VideoCapture(video_filename)
    watermark = cv2.imread(watermark_filename)

    # Получение размеров видео и водяного знака
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    watermark_height, watermark_width, _ = watermark.shape

    # Наложение водяного знака на каждый кадр видео и сохранение результата в файл
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_filename, fourcc, 25, (width, height))
    i = 0
    while True:
        ret, frame = video.read()
        if not ret:
            break
        # Наложение водяного знака на кадр видео
        x = int(width - watermark_width - 10)
        y = int(height - watermark_height - 10)
        frame[y:y+watermark_height, x:x+watermark_width] = watermark
        # Запись кадра с водяным знаком в выходное видео
        out.write(frame)

        i += 1

    # Закрытие видеофайла и выходного видеофайла
    video.release()
    out.release()
    # Создание цифровой подписи для изображения с водяным знаком
    signature = sign_video(output_filename, private_key, 'signature_video.txt')

    return i, private_key