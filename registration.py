import sqlite3
from tkinter import *
from tkinter import messagebox
import main
import os
import subprocess

def register():
    email = email_entry.get()
    
    if not email:
        messagebox.showerror("Ошибка", "Введите адрес электронной почты.")
        return
    
    # Подключение к базе данных
    conn = sqlite3.connect("database.db")
    
    # Создание курсора для выполнения SQL-запросов
    cursor = conn.cursor()
    
    # Создание таблицы, если она не существует
    cursor.execute("CREATE TABLE IF NOT EXISTS users (email TEXT)")
    
    # Выполнение SQL-запроса для добавления адреса электронной почты в базу данных
    cursor.execute("INSERT INTO users (email) VALUES (?)", (email,))
    
    # Подтверждение изменений в базе данных
    conn.commit()
    
    # Выполнение SQL-запроса для проверки наличия адреса электронной почты в базе данных
    cursor.execute("SELECT * FROM users WHERE email=?", (email,))
    result = cursor.fetchone()
    
    # Проверка результата запроса
    if result:
        messagebox.showinfo("Успех", "Вход выполнен успешно.")
    else:
        messagebox.showerror("Ошибка", "Пользователь с таким адресом электронной почты не найден.")

    # Закрытие соединения с базой данных
    cursor.close()
    conn.close()

def login():
    email = email_entry.get()
    
    if not email:
        messagebox.showerror("Ошибка", "Введите адрес электронной почты.")
        return
    
    # Подключение к базе данных
    conn = sqlite3.connect("database.db")
    
    # Создание курсора для выполнения SQL-запросов
    cursor = conn.cursor()
    
    # Выполнение SQL-запроса для проверки наличия адреса электронной почты в базе данных
    cursor.execute("SELECT * FROM users WHERE email=?", (email,))
    result = cursor.fetchone()
    
    # Проверка результата запроса
    if result:
        messagebox.showinfo("Успех", "Вы вошли в систему.")
        #exec(open("venv\main.py").read())  # Открыть окно с основным кодом
        root.destroy()  # Закрыть окно регистрации
        subprocess.Popen(["python", "main.py"])  # Запустить файл main.py
        
    else:
        messagebox.showerror("Ошибка", "Пользователь с таким адресом электронной почты не найден.")

    # Закрытие соединения с базой данных
    cursor.close()
    conn.close()

root = Tk()
root.title("Экран регистрации")

# Изменение цветовой схемы
root.configure(bg="blue")

# Получение размеров окна
window_width = 500
window_height = 300

# Создание фрейма для размещения элементов
frame = Frame(root, bg="blue")
frame.place(relx=0.5, rely=0.5, anchor=CENTER)

email_label = Label(frame, text="Введите адрес электронной почты:", bg="blue", fg="white")
email_label.pack()

email_entry = Entry(frame)
email_entry.pack()

register_button = Button(frame, text="Зарегистрироваться", command=register, bg="blue", fg="white")
register_button.pack()

login_button = Button(frame, text="Войти", command=login, bg="blue", fg="white")
login_button.pack()

# Вычисление координат фрейма
frame_width = frame.winfo_reqwidth()
frame_height = frame.winfo_reqheight()

x = (window_width - frame_width) // 2
y = (window_height - frame_height) // 2

# Позиционирование окна по центру экрана
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

root.geometry(f"{window_width}x{window_height}+{screen_width//2 - window_width//2}+{screen_height//2 - window_height//2}")

root.mainloop()
