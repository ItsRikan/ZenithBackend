import smtplib
import os
from typing import Literal
from dotenv import load_dotenv
from .output_schema import MailSchema
from ..details import SENDER_EMAIL,DEPT_TO_MAILS
from Agents.details import CREATOR_EMAIL
import socket
from ..cofig import DEPARTMENTS
load_dotenv()
a= ['INFO','PAYMENT','MANAGEMENT']
password = os.environ.get('GMAIL_PASSWORD')
async def mailing_tool(dept_name:Literal['INFO','PAYMENT','MANAGEMENT'],draft:str):
    try:
        if dept_name not in DEPARTMENTS:
            return {'status':'failed','message':f'department {dept_name} not found! available departments are {', '.join(DEPARTMENTS)}'}
        reciever_email = DEPT_TO_MAILS[dept_name]
        if not reciever_email:
            {'status':'failed','message':f'department {dept_name} not found!'}
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(SENDER_EMAIL,password)
        server.sendmail(SENDER_EMAIL,reciever_email,draft)
        server.close()
        return {'status':'succeed','message':f"Mail has been sent successfully to {dept_name} department."}
    except (socket.gaierror,socket.timeout,smtplib.SMTPServerDisconnected,smtplib.SMTPConnectError) as e:
        return {'status':'failed','message':f"Can't send mail. Check Internet Connection"}
    except Exception as e:
        return {'status':'failed','message':f"I encountered an internal error. Please report to {SENDER_EMAIL} email about this issue"}