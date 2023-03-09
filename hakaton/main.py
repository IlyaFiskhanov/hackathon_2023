import cv2
import hashlib
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
from generate_key import generate_keys
from image import sign_image,verify_image,calculate_image_hash_print,mark_image,get_signature_image,compare_hashsum_image
from video import sign_video,verify_video,calculate_video_hash_print,mark_video,compare_hashsum_video



private_key, public_key = generate_keys()
assert private_key.public_key().public_numbers() == public_key.public_numbers()

watermark = 'аа.jpeg'

while True:
    try:
        print('Выберите действие:\n'
              '1 - Посмотреть хэш-суммы файла\n'
              '2 - Проверить хэш-суммы файла с оригиналом\n'
              '3 - Подписать файл\n'
              '4 - Проверка подлинности цифровой подписи и хэш-суммы файла\n'
              '5 - Пометить файл водяным знаком\n'
              '6 - Выйти')
        choice = int(input())
# 1 - посмотреть хэш-суммы файла
        if choice == 1:
            print('Выберите тип файла?\n'
            '1 - Изображение?\n'
            '2 - Видео')
            image_and_video = input()
            if image_and_video == '1':
                filename_image = input('Введите имя файла изображения: ')
                calculate_image_hash_print(filename_image)
            elif image_and_video == '2':
                filename_video = input('Введите имя файла видео: ')
                calculate_video_hash_print(filename_video)
            else:
                print('Я не понимаю вас')
            pass
# 2 - Проверить хэш-суммы файла с оригиналом
        elif choice == 2:
            print('Выберите тип файла?\n'
            '1 - Изображение?\n'
            '2 - Видео')
            image_and_video = input()
            if image_and_video == '1':
                filename_image = input('Введите имя файла изображения: ')
                compare_hashsum_image(filename_image)
            elif image_and_video == '2':
                filename_video = input('Введите имя файла видео: ')
                compare_hashsum_video(filename_video)
            else:
                print('Я не понимаю вас')
            pass
# 3 - подписать файл\n
        elif choice == 3:
            print('Выберите тип файла?\n'
            '1 - Изображение?\n'
            '2 - Видео')
            image_and_video = input()
            if image_and_video == '1':
                filename_image = input('Введите имя файла изображения: ')
                sign_image(filename_image, private_key)
            elif image_and_video == '2':
                filename_video = input('Введите имя файла видео: ')
                sign_video(filename_video, private_key)
            else:
                print('Я не понимаю вас')
            pass
# 4 - Проверка подлинности цифровой подписи и хэш-суммы файла
        elif choice == 4:
            print('Выберите тип файла?\n'
            '1 - Изображение?\n'
            '2 - Видео')
            image_and_video = input()
            if image_and_video == '1':
                filename_image= input('Введите имя файла изображение: ')
                signature_filename = input('Введите имя файла с подписью изображения: ')
                expected_hashsum = input('Введите оригинальный хэш-суммы файла: ')
                verify_image(filename_image, signature_filename, public_key,expected_hashsum)
            elif image_and_video == '2':
                filename_video= input('Введите имя файла видео: ')
                signature_filename = input('Введите имя файла с подписью видео: ')
                expected_hashsum = input('Введите оригинальный хэш-суммы файла: ')
                verify_video(filename_video, signature_filename, public_key,expected_hashsum)
            else:
                print('Я не понимаю вас')

            pass
#5 - Пометить файл водяным знаком\n
        elif choice == 5:
            print('Выберите тип файла?\n'
            '1 - Изображение?\n'
            '2 - Видео')
            image_and_video = input()
            if image_and_video == '1':
                filename_image= input('Введите имя файла изображение: ')
                mark_image(filename_image, watermark, 'marked_image.jpg', private_key)
            elif image_and_video == '2':
                filename_video= input('Введите имя файла видео: ')
                mark_video(filename_video, watermark, 'marked_video.mp4', private_key)
            else:
                print('Я не понимаю вас')
            pass

        elif choice == 6:
            print('До свидания!')
            break
        else:
            print('Некорректный выбор')
    except Exception as e:
        print('Ошибка:', e)

"""

"""




