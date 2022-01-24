import requests
import logging

from jinja2 import FileSystemLoader, Environment

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.utils import COMMASPACE, formatdate

API_KEY = "87c22ef41b7ebb63026f535f40b37039-0be3b63b-4f363654"
MAIL_TITLE = "Test mail"
EMAIL_API_SERVER = "https://api.mailgun.net/v3/sandbox021e386f2710423b8371e9be714f8444.mailgun.org"
EMAIL_SENDER = "Scrappy Results <mailgun@sandbox>"
TEMPLATE_DIR = "/notification_system/email_templates"
logger = logging.getLogger(__name__)


def compose_and_send_email(template, recipients, render_data, files=None):
    """
    Composes and sends the validation email to the given user email address
    :param template: <str> template to use for email generation
    :param recipients: <str> user email address
    :param render_data: dict[str] data used to render the template
    :param files: list[path] file paths to be sent
    :return: None
    :raise Exception on send failed
    """
    j2_env = Environment(loader=FileSystemLoader(TEMPLATE_DIR), trim_blocks=True)
    j2_tpl = j2_env.get_template(template)
    email_text = j2_tpl.render(render_data)
    # email_subject = _get_email_subject(template, render_data, subject_key)
    email_message = _create_email(EMAIL_SENDER, recipients,
                                  MAIL_TITLE, email_text)
    try:
        _send_api_message(email_message, recipients)

    except Exception:
        logger.exception("Failed to send mail to recipient(s)")
        raise ValueError("Cannot send email to invalid email address.")


def _get_email_subject(template, render_data, subject_key):
    # subject = SUBJECTS.get(template) if not subject_key else SUBJECTS.get(subject_key)
    # subject = subject.format(migration_date=render_data.get("migration_date"))
    # return subject
    ...


def _create_email(from_account, send_to, subject, text):
    """
    Creates an email object
    :param from_account: <str> the sender's email address
    :param send_to: <list> the destination email addresses
    :param subject: <str> email subject
    :param text: <str> email text
    :return: <MIMEMultipart> the email object
    """
    assert isinstance(send_to, list)

    msg = MIMEMultipart()
    msg["to"] = COMMASPACE.join(send_to)
    msg['from'] = from_account
    msg["date"] = formatdate(localtime=True)
    msg["subject"] = subject
    msg.attach(MIMEText(text, "html"))

    # for f in (files or []):
    #     with open(f, "rb") as fat:
    #         part = MIMEApplication(fat.read(), Name=os.path.basename(f))
    #         # After the file is closed
    #         part["Content-Disposition"] = 'attachment; filename="{}"'.format(os.path.basename(f))
    #         msg.attach(part)

    return msg


def _send_api_message(email_message, user_email):
    """
    Sends a message using the Mailgun API
    :param email_message: <MIME> message
    :param user_email: <str> the destination email
    :return:
    """
    result = requests.post("{}/messages.mime".format(EMAIL_API_SERVER),
                           auth=("api", API_KEY),
                           data={"to": user_email},
                           files={"message": str(email_message)}).json()
    assert result.get("id")


if __name__ == '__main__':
    compose_and_send_email("basic_template.html", recipients=['daniel.hurghis98@gmail.com'], render_data={})
