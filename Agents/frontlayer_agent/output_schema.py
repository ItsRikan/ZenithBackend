from pydantic import BaseModel,Field
from typing import Literal,Optional,TypedDict

class UserDetailsSchema(TypedDict):
    name:Optional[str]=None
    roll_no:Optional[str]=None
    contact_number:Optional[str]=None
    email:Optional[str]=None


class Action(BaseModel):
    action : Literal[
        "answer",
        "send_email",
        "fetch_college_api",
        "search_scholarship"
    ]
    department:Optional[Literal['INFO','PAYMENT','MANAGEMENT','null']] = None
    fetch_college_api_purpose:Optional[Literal['admission','placement_record','details','college_contact_details','news_and_events','everything','null']] = None
    search_scholarship_purpose:Optional[Literal['all_available_scholarship','about_svmcm','schedule_of_svmcm','everything','null']] = None
    send_mail_purpose:Optional[Literal['report_issue','query','inform','uncertain','null']] = None
    user_details_for_mail:Optional[UserDetailsSchema]=None
    mail_objective:Optional[str]=None
    message:Optional[str] = None
    error:Optional[Literal['retry','invalid_name','model_not_found','model_failed','unknown']]=None
    confidence_score:float=Field(...,ge=0,le=1)




