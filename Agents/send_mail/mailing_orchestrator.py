from ..frontlayer_agent.output_schema import Action
from .model import mail_formatter_model
from .output_schema import MailSchema
from .mailing_tool import mailing_tool
from ..details import CREATOR_EMAIL,DEPT_TO_MAILS


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

        # Check all attributes
        if (mail_details.get('message',None) is not None) or (mail_details.get('message',None) =="null"):
            if (mail_details.get('department',None) is None) or (mail_details.get('department') == 'null'):
                departments = ", ".join(str(dept) for dept in DEPT_TO_MAILS.keys())
                message= f"{action.message}. Can you please mention the department where you want to mail. Available departments are : {departments}"
                return {'ready_to_send':False,'message':message}
            if (mail_details.get('send_mail_purpose',None) is None) or (mail_details.get('send_mail_purpose') == 'null'):
                message= f"{action.message}. Can you please mention your purpose of mailing"
                return {'ready_to_send':False,'message':message}
            if (mail_details.get('user_details_for_mail',None) is None) or (mail_details.get('user_details_for_mail') == 'null'):
                message= f"{action.message}. Please provide your name, contact number, email address and college roll number if available."
                return {'ready_to_send':False,'message':message}
            if (mail_details.get('mail_objective',None) is None) or (mail_details.get('mail_objective') == 'null'):
                message= f"{action.message}. Can you please mention your objetive of mailing"
                return {'ready_to_send':False,'message':message}
            
        else:
            if (mail_details.get('department',None) is None) or (mail_details.get('department') == 'null'):
                departments = ", ".join(str(dept) for dept in DEPT_TO_MAILS.keys())
                message= f"Can you please mention the department where you want to mail. Available departments are : {departments}"
                return {'ready_to_send':False,'message':message}
            if (mail_details.get('send_mail_purpose',None) is None) or (mail_details.get('send_mail_purpose') == 'null'):
                message= f"Can you please mention your purpose of mailing"
                return {'ready_to_send':False,'message':message}
            if (mail_details.get('user_details_for_mail',None) is None) or (mail_details.get('user_details_for_mail') == 'null'):
                message= f"Please provide your name, contact number,and email address"
                return {'ready_to_send':False,'message':message}
            if (mail_details.get('mail_objective',None) is None) or (mail_details.get('mail_objective') == 'null'):
                message= f"Can you please mention your objetive of mailing"
                return {'ready_to_send':False,'message':message}
                       
        for key,value in mail_details['user_details_for_mail'].items():
            if key=="roll_no":
                continue
            if value is None or value=="null":
                return {'ready_to_send':False,'message':f"Please provide your {key}"}            
            
        # Mail model calling
        mail_model_response:MailSchema=mail_formatter_model(input_object=mail_details)
        # Check for error or unnecessary
        if (mail_model_response.error is not None) or (mail_model_response.necessity_score_of_mail<0.1):
            return {'ready_to_send':False,'message':str(mail_model_response.reason_if_mail_rejected)} 
        
        # Confidance Check
        if mail_model_response.confidence_score<0.6:
            message = "I’m not fully sure I understand your message. Could you please clarify what you mean?"
            return {'ready_to_send':False,'message':message}
        
        
        mail_draft = f"Subject : {mail_model_response.mail} \n\n {mail_model_response.subject}"
        return {'ready_to_send':True,'draft':mail_draft,'department':action.department}
    except Exception as e:
        message = f"""Failed to send mail to {action.department} department due to an internal error. Can you please report on Email : {CREATOR_EMAIL} manually regarding this issue"""
        return {'ready_to_send':False,'message':message}







