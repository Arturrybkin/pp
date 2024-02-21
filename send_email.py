import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime

def send_email():
    # Подключение к базе данных
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    # Получение адреса электронной почты и даты из базы данных
    cursor.execute("SELECT email, date FROM tasks")
    results = cursor.fetchall()
    
    # Проверка каждой записи в базе данных
    for result in results:
        email = result[0]
        date = result[1]
        
        # Проверка, является ли дата текущей датой
        current_date = datetime.date.today()
        if date == current_date:
            # Создание объекта MIMEMultipart для создания письма
            message = MIMEMultipart()
            
            # Заполнение полей письма
            message["From"] = "practice.project.2202@mail.ru"  # Замените на ваш адрес электронной почты
            message["To"] = email
            message["Subject"] = "Напоминание о задаче"
            
            # Текст письма
            body = "Ваша задача: ..."
            message.attach(MIMEText(body, "plain"))
            
            # Отправка письма
            try:
                smtp_obj = smtplib.SMTP("smtp.mail.ru", 993)  # Замените на данные вашего почтового сервера
                smtp_obj.starttls()
                smtp_obj.login("practice.project.2202@mail.ru", "pKf-G4d-yHW-2k8")  # Замените на данные вашего почтового аккаунта
                smtp_obj.sendmail("practice.project.2202@mail.ru", email, message.as_string())
                smtp_obj.quit()
                
                print("Письмо отправлено успешно.")
            except Exception as e:
                print(f"Ошибка при отправке письма: {str(e)}")
    
    # Закрытие соединения с базой данных
    cursor.close()
    conn.close()

send_email()
