from ..frontlayer_agent.output_schema import Action
from .model import mail_formatter_model
from .output_schema import MailSchema
from .mailing_tool import mailing_tool
from ..details import CREATOR_EMAIL,DEPT_TO_MAILS
from ..logger import logging


async def mailing_orchestrator(action:Action)->str:
    try:
        # Action -> Mail Details
        mail_details:dict = {
            'department':action.department,
            'send_mail_purpose':action.send_mail_purpose,
            'user_details_for_mail':action.user_details_for_mail,
            'mail_objective':action.mail_objective,
            'message':action.message
        }

        logging.debug(mail_details)
        # Check all attributes
        if (mail_details.get('message',None) is not None) or (mail_details.get('message',None) =="null"):
            if (mail_details.get('department',None) is None) or (mail_details.get('department') == 'null'):
                departments = ", ".join(str(dept) for dept in DEPT_TO_MAILS.keys())
                return f"{action.message}. Can you please mention the department where you want to mail. Available departments are : {departments}"
            if (mail_details.get('send_mail_purpose',None) is None) or (mail_details.get('send_mail_purpose') == 'null'):
                return f"{action.message}. Can you please mention your purpose of mailing"
            if (mail_details.get('user_details_for_mail',None) is None) or (mail_details.get('user_details_for_mail') == 'null'):
                return f"{action.message}. Please provide your name, contact number, email address and college roll number if available."
            if (mail_details.get('mail_objective',None) is None) or (mail_details.get('mail_objective') == 'null'):
                return f"{action.message}. Can you please mention your objetive of mailing"
        else:
            if (mail_details.get('department',None) is None) or (mail_details.get('department') == 'null'):
                departments = ", ".join(str(dept) for dept in DEPT_TO_MAILS.keys())
                return f"Can you please mention the department where you want to mail. Available departments are : {departments}"
            if (mail_details.get('send_mail_purpose',None) is None) or (mail_details.get('send_mail_purpose') == 'null'):
                return f"Can you please mention your purpose of mailing"
            if (mail_details.get('user_details_for_mail',None) is None) or (mail_details.get('user_details_for_mail') == 'null'):
                return f"Please provide your name, contact number,and email address"
            if (mail_details.get('mail_objective',None) is None) or (mail_details.get('mail_objective') == 'null'):
                return f"Can you please mention your objetive of mailing"
            
        for key,value in mail_details['user_details_for_mail'].items():
            if key=="roll_no":
                continue
            if value is None or value=="null":
                return f"Please provide your {key}"    
            
            
        # Mail model calling
        logging.debug("mail formatter model called")
        mail_model_response:MailSchema=mail_formatter_model(input_object=mail_details)
        logging.debug(f"Mail Formatter Respose => {mail_model_response}")
        # Check for error or unnecessary
        if (mail_model_response.error is not None) or (mail_model_response.necessity_score_of_mail<0.1):
            return str(mail_model_response.reason_if_mail_rejected)
        
        # Confidance Check
        if mail_model_response.confidence_score<0.6:
            return "I’m not fully sure I understand your message. Could you please clarify what you mean?"
        
        # Calling Mailing Tool
        mail_response:bool = await mailing_tool(
            dept_name=action.department,
            mail=mail_model_response.mail,
            subject=mail_model_response.subject
        )
        logging.debug("Mail Sent Successfully")
        # Check mail failure
        if mail_response.get('status','failed')=='failed':
            return f"""
            Failed to send mail to {action.department} department. 
            Issue : {mail_response.get('issue','Internal Error')}
            Our maling tool is busy or has some error can you please try again later.
            report on Email : {CREATOR_EMAIL} manually regarding this issue"""
        
        return f"""Mail hasbeen sent successfully to {action.department} department. 
        Mail Details : 
            {mail_details}
        """
    except Exception as e:
        logging.exception(f"Error in mailing orchestrator. Type = {type(e)} | error = {e}")
        return f"""Failed to send mail to {action.department} department due to an internal error. Can you please report on Email : {CREATOR_EMAIL} manually regarding this issue"""







