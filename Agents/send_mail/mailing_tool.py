import smtplib
import os
from typing import Literal
from dotenv import load_dotenv
from .output_schema import MailSchema
from ..details import SENDER_EMAIL,DEPT_TO_MAILS
from ..logger import logging
from Agents.details import CREATOR_EMAIL
load_dotenv()

password = os.environ.get('GMAIL_PASSWORD')
async def mailing_tool(dept_name:Literal['INFO','PAYMENT','MANAGEMENT'],draft:str):
    try:
        reciever_email = DEPT_TO_MAILS[dept_name]
        if not reciever_email:
            {'status':'failed','issue':f'department {dept_name} not found!'}
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(SENDER_EMAIL,password)
        logging.debug("Login to server")
        server.sendmail(SENDER_EMAIL,reciever_email,draft)
        logging.debug("mail sent")
        server.close()
        return {'status':'succeed'}
    except:
        return {'status':'failed','issue':f'I encountered an Internal Error.Report to {SENDER_EMAIL} about this issue'}