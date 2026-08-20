import logging

logger = logging.getLogger(__name__)


def send_lead_email(lead):
    """Returns None on success, or an error message string on failure."""
    # SMTP пока не настроен на боевую отправку — логируем вместо реальной
    # отправки, чтобы можно было тестировать капчу и форму целиком.
    logger.info(
        "Письмо отправлено (заглушка): заявка id=%s, имя=%s, телефон=%s, курс=%s",
        lead.id, lead.name, lead.phone, lead.course,
    )
    return None
