import logging
import os
import smtplib
from email.message import EmailMessage
from email.utils import formatdate, make_msgid

logger = logging.getLogger(__name__)


def send_lead_email(lead):
    """Returns None on success, or an error message string on failure."""
    try:
        msg = EmailMessage()
        msg["Subject"] = f"Новая заявка: {lead.name}"
        msg["From"] = os.environ["SMTP_FROM"]
        msg["To"] = os.environ["SMTP_TO"]
        msg["Date"] = formatdate(localtime=True)
        msg["Message-Id"] = make_msgid(domain=os.environ["SMTP_FROM"].split("@")[-1])
        msg.set_content(f"Имя: {lead.name}\nТелефон: {lead.phone}\nКурс: {lead.course}")

        host, port = os.environ["SMTP_HOST"], int(os.environ["SMTP_PORT"])
        client_cls = smtplib.SMTP_SSL if port == 465 else smtplib.SMTP
        with client_cls(host, port, timeout=10) as smtp:
            if port != 465:
                smtp.starttls()
            smtp.login(os.environ["SMTP_USER"], os.environ["SMTP_PASSWORD"])
            smtp.send_message(msg)
        return None
    except Exception as e:
        logger.exception("Failed to send lead notification email for lead id=%s", lead.id)
        return str(e)
