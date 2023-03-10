from get_file_type import type_get_file_hash,type_compare_hashsum,type_sign,type_verify_file_with_signature,type_mark_files_with_watermark

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
            type_get_file_hash()
            pass
# 2 - Проверить хэш-суммы файла с оригиналом
        elif choice == 2:
            type_compare_hashsum()
            pass
# 3 - подписать файл
        elif choice == 3:
            type_sign()
            pass
# 4 - Проверка подлинности цифровой подписи и хэш-суммы файла
        elif choice == 4:
            type_verify_file_with_signature()
            pass
#5 - Пометить файл водяным знаком
        elif choice == 5:
           type_mark_files_with_watermark()
           pass
        elif choice == 6:
            print('До свидания!')
            break
        else:
            print('Некорректный выбор')
    except Exception as e:
        print('Ошибка:', e)



