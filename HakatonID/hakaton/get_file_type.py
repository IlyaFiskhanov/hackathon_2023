
from image import calculate_image_hash_print,compare_hashsum_image,sign_image,verify_image,mark_image
from video import calculate_video_hash_print,compare_hashsum_video,sign_video,verify_video,mark_video
from generate_key import load_keys
private_key, public_key = load_keys()

watermark = 'watermark.png'

def get_file_type():
    print('Выберите тип файла?\n1 - Изображение?\n2 - Видео')
    while True:
        file_type = input()
        if file_type in ['1', '2']:
            return file_type
        print('Некорректный ввод. Попробуйте еще раз.')

def type_get_file_hash():
    image_and_video = get_file_type()
    if image_and_video == '1':
        filename_image = input('Введите имя файла изображения: ')
        calculate_image_hash_print(filename_image)
    elif image_and_video == '2':
        filename_video = input('Введите имя файла видео: ')
        calculate_video_hash_print(filename_video)
    else:
        print('Я не понимаю вас')

def type_compare_hashsum():
    image_and_video = get_file_type()
    if image_and_video == '1':
        filename_image = input('Введите имя файла изображения: ')
        compare_hashsum_image(filename_image)
    elif image_and_video == '2':
        filename_video = input('Введите имя файла видео: ')
        compare_hashsum_video(filename_video)
    else:
        print('Я не понимаю вас')

def type_sign():
    image_and_video = get_file_type()
    if image_and_video == '1':
        filename_image = input('Введите имя файла изображения: ')
        sign_image(filename_image, private_key)
    elif image_and_video == '2':
        filename_video = input('Введите имя файла видео: ')
        sign_video(filename_video, private_key)
    else:
        print('Я не понимаю вас')

def type_verify_file_with_signature():
    expected_hashsum = None  # initialize expected_hashsum to None
    image_and_video = get_file_type()
    if image_and_video == '1':
        filename_image= input('Введите имя файла изображение: ')
        signature_filename = input('Введите имя файла с подписью изображения: ')
        if expected_hashsum:
            expected_hashsum = input("Оригинальная хэш-сумма не найдена. Введите ее вручную: ")
        verify_image(filename_image, signature_filename, public_key, expected_hashsum)
    elif image_and_video == '2':
        filename_video= input('Введите имя файла видео: ')
        signature_filename = input('Введите имя файла с подписью видео: ')
        if expected_hashsum:
            expected_hashsum = input("Оригинальная хэш-сумма не найдена. Введите ее вручную: ")
        verify_video(filename_video, signature_filename, public_key,expected_hashsum)
    else:
        print('Я не понимаю вас')

def type_mark_files_with_watermark():
    image_and_video = get_file_type()
    if image_and_video == '1':
        filename_image= input('Введите имя файла изображение: ')
        mark_image(filename_image, watermark, private_key)
    elif image_and_video == '2':
        filename_video= input('Введите имя файла видео: ')
        mark_video(filename_video, watermark, private_key)
    else:
        print('Я не понимаю вас')
              
"""
from image import calculate_image_hash_print,compare_hashsum_image,sign_image,verify_image,mark_image - импортирует функции для работы с изображениями
from video import calculate_video_hash_print,compare_hashsum_video,sign_video,verify_video,mark_video - импортирует функции для работы с видео
from generate_key import load_keys - импортирует функцию для загрузки ключей
private_key, public_key = load_keys() - загружает закрытый и открытый ключи
watermark = 'file.jpeg' - задает водяной знак
get_file_type() - функция, которая запрашивает тип файла (изображение или видео) у пользователя. Возвращает значение 1, если выбрано изображение, и 2, если выбрано видео.
type_get_file_hash() - функция, которая вызывает функцию для расчета хэш-суммы изображения или видео, в зависимости от выбранного типа файла.
type_compare_hashsum() - функция, которая вызывает функцию для сравнения хэш-суммы файла с оригиналом.
type_sign() - функция, которая вызывает функцию для подписания файла.
type_verify_file_with_signature() - функция, которая вызывает функцию для проверки подлинности цифровой подписи и хэш-суммы файла.
type_mark_files_with_watermark() - функция, которая вызывает функцию для пометки файла водяным знаком
"""