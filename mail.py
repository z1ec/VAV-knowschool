import logging
import os
import smtplib
from email.message import EmailMessage

logger = logging.getLogger(__name__)


def send_lead_email(lead):
    try:
        msg = EmailMessage()
        msg["Subject"] = f"Новая заявка: {lead.name}"
        msg["From"] = os.environ["SMTP_FROM"]
        msg["To"] = os.environ["SMTP_TO"]
        msg.set_content(f"Имя: {lead.name}\nТелефон: {lead.phone}\nКурс: {lead.course}")

        host, port = os.environ["SMTP_HOST"], int(os.environ["SMTP_PORT"])
        client_cls = smtplib.SMTP_SSL if port == 465 else smtplib.SMTP
        with client_cls(host, port, timeout=10) as smtp:
            if port != 465:
                smtp.starttls()
            smtp.login(os.environ["SMTP_USER"], os.environ["SMTP_PASSWORD"])
            smtp.send_message(msg)
    except Exception:
        logger.exception("Failed to send lead notification email for lead id=%s", lead.id)
