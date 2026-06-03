from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from jsonPart import loadInfo
from email import encoders
import smtplib

    


async def sendTo(header, content, admins, file_buffer = None, filename = None):
    info=loadInfo()
    message = MIMEMultipart("mixed")
    message["Subject"] = header
    message["From"] = info['SENDER_EMAIL']

    # Создаем контейнер для текстовой и HTML частей
    body_parts = MIMEMultipart("alternative")

    text_version = content

    if file_buffer != None and filename != None:
        message.attach(file_attach(filename=filename, file_buffer=file_buffer))

    body_parts.attach(MIMEText(text_version, "plain", "utf-8"))
    message.attach(body_parts)

    for i in admins:
        print(i['email'])
        try:
            with smtplib.SMTP_SSL(info['SMTP_SERVER'], info['SMTP_PORT']) as server:
                server.login(info['SENDER_EMAIL'], info['SENDER_PASSWORD'])
                server.sendmail(info['SENDER_EMAIL'], i['email'], message.as_string())
                print("Письмо с вложением успешно отправлено!")
        except Exception as e:
            print(f"Ошибка при отправке: {e}")

def file_attach(filename,file_buffer):
    part = MIMEBase("application", "octet-stream")
    part.set_payload(file_buffer.read()) 
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename={f"{filename}"}")
    return part