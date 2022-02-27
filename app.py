import logging
import uvicorn
from fastapi import FastAPI
from fastapi.responses import Response, RedirectResponse
from sendgrid_send_mail import create_and_send_mail

from models import SendMailBody

app = FastAPI()
logger = logging.getLogger(__name__)


@app.get("/")
def main_page():
    return RedirectResponse(url="/docs")


@app.post("/send_mail")
def k_send_mail(body: SendMailBody):
    try:
        return create_and_send_mail(body.sender, body.recipients, body.subject, body.template_name, body.render_data)
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        return Response(status_code=500)


uvicorn.run(app, port=8100)
