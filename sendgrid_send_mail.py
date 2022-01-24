# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
import logging
from typing import List
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from decouple import config

from jinja2 import FileSystemLoader, Environment
TEMPLATE_DIR = config("TEMPLATE_DIR")

API_KEY = config("SENDGRID_API_KEY")
logger = logging.getLogger(__name__)


def create_and_send_mail(sender, recipients, subject, render_data):
    html_content = get_formatted_content('basic_template.html', render_data)
    message = create_message(sender, recipients, subject, html_content)
    send_message(message)


def get_formatted_content(html_template, render_data):
    j2_env = Environment(loader=FileSystemLoader(TEMPLATE_DIR), trim_blocks=True)
    j2_tpl = j2_env.get_template(html_template)
    email_text = j2_tpl.render(render_data)
    return email_text


def create_message(sender: str, recipients: List, subject: str, html_content: str):
    if len(recipients) == 1:
        recipients = recipients[0]
    return Mail(from_email=sender,
                to_emails=recipients,
                subject=subject,
                html_content=html_content)


def send_message(mail: Mail):
    try:
        mail_api_client = SendGridAPIClient(API_KEY)
        response = mail_api_client.send(mail)
        assert response.status_code == 202
    except Exception as e:
        logger.error(f"Exception occurred while sending email: {e}")


if __name__ == '__main__':
    create_and_send_mail(sender="daniel.hurghis98@gmail.com", recipients=['nemiyo1059@nahetech.com'],
                         subject="Twilio SendGrid test", render_data={})
