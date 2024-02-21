import re
import sqlite3
from tkinter import *
from tkcalendar import Calendar
from tkinter import messagebox
from registration import register



def validate_time(time):
    pattern = r'^([01]\d|2[0-3]):([0-5]\d)$'
    return re.match(pattern, time)


def add_task():
    task = entry.get()
    date = cal.selection_get().strftime("%d/%m/%Y")
    time = time_entry.get()
    
    if not task:
        messagebox.showerror("Ошибка", "Введите задачу.")
        return
    
    if not date:
        messagebox.showerror("Ошибка", "Выберите дату.")
        return
    
    if not time or not validate_time(time):
        messagebox.showerror("Ошибка", "Неверный формат времени. Введите время в формате ЧЧ:ММ (например, 09:30).")
        return
    
    task_with_datetime = f"{date} {time} - {task}"
    listbox.insert(END, task_with_datetime)
    entry.delete(0, END)
    time_entry.delete(0, END)
    messagebox.showinfo("Успех", "Задача успешно добавлена.")
    
    # Подключение к базе данных SQLite
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    
    # Создание таблицы, если она не существует
    c.execute('''CREATE TABLE IF NOT EXISTS tasks
                 (task text, date text, time text)''')
    
    # Вставка данных в таблицу
    c.execute("INSERT INTO tasks VALUES (?, ?, ?)", (task, date, time))
    
    # Сохранение изменений и закрытие соединения
    conn.commit()
    conn.close()

def delete_task():
    selected_index = listbox.curselection()
    if selected_index:
        # Удаление из списка
        listbox.delete(selected_index)
        messagebox.showinfo("Успех", "Задача успешно удалена.")

        # Удаление из базы данных SQLite
        conn = sqlite3.connect("tasks.db")
        c = conn.cursor()

        # Получение выбранной задачи
        selected_task = listbox.get(selected_index)

        # Разбор выбранной задачи для получения даты и времени
        date, time, task = selected_task.split(' ', 2)

        # Удаление соответствующей записи из таблицы
        c.execute("DELETE FROM tasks WHERE task=? AND date=? AND time=?", (task, date, time))

        # Сохранение изменений и закрытие соединения
        conn.commit()
        conn.close()

def show_schedule():
    selected_date = cal.selection_get().strftime("%d/%m/%Y")
    tasks = listbox.get(0, END)
    filtered_tasks = [task for task in tasks if task.startswith(selected_date)]
    sorted_tasks = sorted(filtered_tasks, key=lambda x: x.split()[1])
    
    schedule_window = Toplevel(root)
    schedule_window.title("Расписание дня")
    schedule_listbox = Listbox(schedule_window)
    
    for task in sorted_tasks:
        schedule_listbox.insert(END, task)
    
    schedule_listbox.pack()

root = Tk()
root.title("Приложение для организации дел")

# Изменение цветовой схемы
root.configure(bg="blue")

label = Label(root, text="Выберите дату:", bg="blue", fg="white")
label.pack()

cal = Calendar(root)
cal.pack()

time_label = Label(root, text="Выберите время:", bg="blue", fg="white")
time_label.pack()

time_entry = Entry(root)
time_entry.pack()

entry_label = Label(root, text="Введите задачу:", bg="blue", fg="white")
entry_label.pack()

entry = Entry(root)
entry.pack()

add_button = Button(root, text="Добавить", command=add_task, bg="blue", fg="white")
add_button.pack()

delete_button = Button(root, text="Удалить", command=delete_task, bg="blue", fg="white")
delete_button.pack()

show_schedule_button = Button(root, text="Показать расписание", command=show_schedule, bg="blue", fg="white")
show_schedule_button.pack()

listbox = Listbox(root)
listbox.pack()

root.mainloop()
