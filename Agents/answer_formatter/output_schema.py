from pydantic import BaseModel,Field
from typing import Literal,Optional

class AnswerSchma(BaseModel):
    message:str=Field(...)
    error:Optional[Literal['retry','invalid_name','model_not_found','model_failed','unknown']]=None




