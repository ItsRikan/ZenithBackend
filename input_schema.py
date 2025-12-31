from pydantic import BaseModel,Field
from typing import Literal,Optional

class InputSchema(BaseModel):
    user_query:str=Field(...,description="User's prompt",examples=["Hi","Tell me about this college"])
    prev_action:dict=Field(...,description="Previous action")


class InputMailSchema(BaseModel):
    draft:str=Field(...,)
    department:str=Literal['INFO','PAYMENT','MANAGEMENT']