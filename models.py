from typing import List, Dict,Optional
from pydantic import BaseModel


class SendMailBody(BaseModel):
    template_name: str
    sender: str
    recipients: List[str]
    render_data: Optional[Dict]
    subject: str
