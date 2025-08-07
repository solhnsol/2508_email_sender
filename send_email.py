import smtplib, ssl
from email.message import EmailMessage
from functools import wraps
import os
from dotenv import load_dotenv
load_dotenv()


def send_notification_email(to_email, subject, content):
    """지정된 내용으로 이메일을 보내는 함수"""
    SENDER_EMAIL = 'jayhanss@yonsei.ac.kr'
    from_name = 'KFAI 연구실 알림이'
    APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")
    msg = EmailMessage()
    msg.set_content(content)
    msg["Subject"] = subject
    msg["From"] = f"{from_name} <{SENDER_EMAIL}>"
    msg["To"] = to_email
    
    smtp_server = "smtp.gmail.com"
    port = 465

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.send_message(msg)
        print(f"[{subject}] 이메일 전송 성공")
    except Exception as e:
        print(f"이메일 전송 오류: {e}")


def notify_on_finish(to_email):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                subject = f"[성공] 학습 완료: {func.__name__}"
                content = f"'{func.__name__}' 학습이 성공적으로 완료되었습니다."
                send_notification_email(to_email, subject, content)
                return result
            except Exception as e:
                subject = f"[오류] 학습 실패: {func.__name__}"
                content = f"'{func.__name__}' 학습 중 오류가 발생했습니다.\n\n오류 내용:\n{e}"
                send_notification_email(to_email, subject, content)
                raise
        return wrapper
    return decorator