from pydantic import BaseModel,Field
from typing import Literal,Optional,Dict

class MailSchema(BaseModel):
    subject:Optional[str]=None
    mail:Optional[str]=None
    error:Optional[Literal['retry','invalid_name','model_not_found','model_failed','unknown']]=None
    reason_if_mail_rejected:Optional[str]=None
    necessity_score_of_mail:float=Field(...,ge=0,le=1)
    confidence_score:float=Field(...,ge=0,le=1)
    




