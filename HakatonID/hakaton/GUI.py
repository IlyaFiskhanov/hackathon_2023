from image import calculate_image_hash_print, compare_hashsum_image, sign_image, verify_image, mark_image
from video import calculate_video_hash_print, compare_hashsum_video, sign_video, verify_video, mark_video
from generate_key import load_keys
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

private_key, public_key = load_keys()

watermark = 'watermark.png'
filename = ""

root = Tk()
root.configure(bg='#ffc0cb')  # цвет фона
root.title("Маркировка контента")
root.geometry("635x500")  # рамер окна
style = ttk.Style()
style.configure("BW.TLabel", background="black")
root.clipboard_clear()

hash_box = Text(root, height=1, width=40)
hash_box.configure(bg='#fadadd')

name_file_box = Text(root, height=1, width=40)
name_file_box.configure(bg='#fadadd')

box1 = Text(root, height=1, width=70)
box1.configure(bg='#fadadd')

label_hash = Label(text="", justify=LEFT)
label_hash.configure(bg='#ffc0cb')

label_ID = Label(text="©КОМАНДА ID", justify=LEFT)
label_ID.configure(bg='#ffc0cb')
label_ID.place(relx=.05, rely=.91)

label2_hash = Label(text="", justify=LEFT)
label2_hash.configure(bg='#ffc0cb')

label = Label(text="", justify=LEFT)
label.configure(bg='#ffc0cb')

top_label = Label(text="Выбирете что хотите сделать с файлом:", justify=LEFT)  # надпись
top_label.place(relx=.05, rely=.05)  # расположение текста
top_label.configure(bg='#ffc0cb')  # цвет фона

type_list = ttk.Combobox(values=[
    "Посмотреть хэш-суммы файла",
    "Проверить хэш-суммы файла с оригиналом",
    "Подписать файл",
    "Проверка подлинности цифровой подписи и хэш-суммы файла",
    "Пометить файл водяным знаком"], width=60)  # окно выбора параметров
type_list.current(0)  # какой элемент будет автоматически выбран
type_list.place(relx=.05, rely=.15)

list_get_type = ttk.Combobox(values=["Изображение", "Видео"])
list_get_type.current(0)  # какой элемент будет автоматически выбран
list_get_type.place(relx=.05, rely=.25)

top_box = Text(root, height=1, width=40)
top_box.configure(bg='#fadadd')
top_box.place(relx=.05, rely=.35)





def select_file():
    top_box.delete("1.0", END)
    filetypes = (
        ('All files', '*.*'),
    )
    filename = fd.askopenfilename(
        initialdir='/',
        filetypes=filetypes)
    top_box.insert('1.0', filename)


def clean_pleace():
    top_box.delete("1.0", END)
    box1.place_forget()
    label_hash.place_forget()
    hash_box.place_forget()
    label.place_forget()
    name_file_box.place_forget()
    label2_hash.place_forget()


def selectCommandCallback(event):
    print(type_list.get())
    if type_list.get() == 'Посмотреть хэш-суммы файла':
        clean_pleace()
        box1.delete([1.0], END)
    if type_list.get() == 'Проверить хэш-суммы файла с оригиналом':
        clean_pleace()
        label.configure(text='Введите хэш-сумму файла оригинала:')
        label.place(relx=.05, rely=.45)
        hash_box.place(relx=.05, rely=.55)
        hash_box.delete([1.0], END)
    if type_list.get() == 'Подписать файл':
        clean_pleace()
    if type_list.get() == 'Проверка подлинности цифровой подписи и хэш-суммы файла':
        clean_pleace()
        label.configure(text='Данные о хэш-сумме вызываются из файла hash_summa.txt\nДанные о цифровой подписи берутся из файла signature_image.txt\nУбедитесь, что вы обновили данные ')
        label.place(relx=.05, rely=.45)
    if type_list.get() == 'Пометить файл водяным знаком':
        clean_pleace()
        label.configure(text='На файл добавляется водяной знак из файла wathermark.png')
        label.place(relx=.05, rely=.45)



def apply_command():

    print(top_box.get("1.0", END)[:-1])

    if type_list.get() == 'Посмотреть хэш-суммы файла':
        if list_get_type.get() == 'Изображение':
            hash = calculate_image_hash_print(top_box.get("1.0", END)[:-1])
            label_hash.configure(text="Хэш сумма данного файла = ")
            label_hash.place(relx=.05, rely=.45)
            box1.insert('1.0', hash)
            box1.place(relx=.05, rely=.55)
            #root.clipboard_clear()
            #root.clipboard_append(hash)
            label.configure(text="Хэш сумма скопирована  в файл hash_summa.txt ")
            label.place(relx=.05, rely=.65)
        elif list_get_type.get() == 'Видео':
            hash = calculate_video_hash_print(top_box.get("1.0", END)[:-1])
            label_hash.configure(text="Хэш сумма данного файла = ")
            label_hash.place(relx=.05, rely=.45)
            box1.insert('1.0', hash)
            box1.place(relx=.05, rely=.55)
            #root.clipboard_clear()
            #root.clipboard_append(hash)
            label.configure(text="Хэш сумма скопирована в файл hash_summa.txt ")
            label.place(relx=.05, rely=.65)
        else:
            tk.messagebox.showerror(title="non", message="Хьюстон у нас проблемы")

    if type_list.get() == 'Проверить хэш-суммы файла с оригиналом':
        if list_get_type.get() == 'Изображение':
            hash_new = compare_hashsum_image(top_box.get("1.0", END)[:-1], hash_box.get("1.0", END)[:-1])
            label2_hash.configure(text=hash_new)
            label2_hash.place(relx=.05, rely=.65)
        elif list_get_type.get() == 'Видео':
            hash_new = compare_hashsum_video(top_box.get("1.0", END)[:-1], hash_box.get("1.0", END)[:-1])
            label2_hash.configure(text=hash_new)
            label2_hash.place(relx=.05, rely=.65)
        else:
            tk.messagebox.showerror(title="non", message="Хьюстон у нас проблемы")

    if type_list.get() == 'Подписать файл':
        if list_get_type.get() == 'Изображение':
            sign_image(top_box.get("1.0", END)[:-1], private_key, 'signature_image.txt')
            tk.messagebox.showinfo(title="good",
                                   message="Создана цифровая подпись для фото и сохранена в файл signature_image.txt")
        elif list_get_type.get() == 'Видео':
            sign_video(top_box.get("1.0", END)[:-1], private_key, 'signature_video.txt')
            tk.messagebox.showinfo(title="good",
                                   message="Создана цифровая подпись для видео и сохранена в файл signature_video.txt")
        else:
            tk.messagebox.showerror(title="non", message="Хьюстон у нас проблемы")

    if type_list.get() == 'Проверка подлинности цифровой подписи и хэш-суммы файла':
        if list_get_type.get() == 'Изображение':
            verify = verify_image(top_box.get("1.0", END)[:-1], 'signature_image.txt', public_key)
            label_hash.configure(text=verify)
            label_hash.place(relx=.05, rely=.55)
        elif list_get_type.get() == 'Видео':
            verify = verify_image(top_box.get("1.0", END)[:-1], 'signature_video.txt', public_key)
            label_hash.configure(text=verify)
            label_hash.place(relx=.05, rely=.55)
        else:
            tk.messagebox.showerror(title="non", message="Хьюстон у нас проблемы")

    if type_list.get() == 'Пометить файл водяным знаком':
        if list_get_type.get() == 'Изображение':
            mark = mark_image(top_box.get("1.0", END)[:-1], watermark,
                              private_key)
            tk.messagebox.showinfo(title="good", message="На фото добавлен водяной знак")
        elif list_get_type.get() == 'Видео':
            mark = mark_video(top_box.get("1.0", END)[:-1], watermark,
                              private_key)
            tk.messagebox.showinfo(title="good", message="На видео добавлен водяной знак")
        else:
            tk.messagebox.showerror(title="non", message="Хьюстон у нас проблемы")


open_button = Button(text='ОБЗОР',
                     bg='#ffffff',
                     command=select_file)  # кнопка обзора
open_button.place(relx=.6, rely=.34)

apply_button = Button(text='ПРИМЕНИТЬ',
                      bg='#ffffff',
                      command=apply_command)
apply_button.place(relx=.8, rely=.9)



type_list.bind("<<ComboboxSelected>>", selectCommandCallback)

root.mainloop()
