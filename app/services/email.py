from pathlib import Path
from typing import Annotated

from starlette.background import BackgroundTasks
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from ..config import settings
from ..models.email import EmailSchema

conf = ConnectionConfig(
    MAIL_USERNAME=settings.SMTP_USER,
    MAIL_PASSWORD=settings.SMTP_PASSWORD,
    MAIL_FROM=settings.SMTP_USER,
    MAIL_PORT=settings.SMTP_PORT,
    MAIL_SERVER=settings.SMTP_HOST,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    TEMPLATE_FOLDER=settings.TEMPLATE_FOLDER
)


class EmailService:
    def __init__(self):
        self.fm = FastMail(conf)
        self.background_tasks = BackgroundTasks()

    async def send_email(self, email: EmailSchema):
        message = MessageSchema(
            subject="Welcome",
            recipients=email.email,
            template_body=email.body,
            subtype=MessageType.html,
        )
        self.background_tasks.add_task(self.fm.send_message, message, template_name="signup.html")
