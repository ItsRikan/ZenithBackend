from .orchestrator import run_action
from .frontlayer_agent.output_schema import Action
from .frontlayer_agent.model import decide_action_model
from .answer_formatter.model import answer_formatter_model
from .utils import action_taken_format
from .cofig import MODEL_LIST
from .answer_formatter.output_schema import AnswerSchma
from .details import CREATOR_EMAIL


async def agent_runner(user_query,prev_action)->dict:
    try:
        final_result = None

        # Decide Action - 1
        action = decide_action_model(user_query=user_query,prev_action=prev_action)

        # Action -> Dict
        action_taken:dict = action_taken_format(action)
        

        # Error Checking
        if action.error is not None:
            final_result=f"Sorry! I can't respond now! The reason of this error could be your Internet problem or API token Exceeded"
            return {'final_result':final_result,'summary':action_taken,'ready_to_send':False}
        
        # Confidence Checking
        if action.confidence_score<0.6:
            final_result = "I’m not fully sure I understand your message. Could you please clarify what you mean?"
            return {'final_result':final_result,'summary':action_taken,'ready_to_send':False}
        

        # Performing Action - 2
        action_result = await run_action(action)

        # Format Answer If Required - 3
        if action.action=="answer":
            final_result=AnswerSchma(message=action_result)
        elif action.action=="send_email":
            if action_result.get('ready_to_send',False)==False:
                final_result = action_result['message']
                return {'final_result':final_result,'summary':action_taken,'ready_to_send':False}
            else:
                final_result = "I am ready to send the mail. Just waiting for your approval"
                return {'final_result':final_result,'summary':action_taken,**action_result}
        elif action.action=="fetch_college_api" or action.action=="search_scholarship":
            final_result = answer_formatter_model(user_query=user_query,answer=action_result)
        
        return {'final_result':final_result.message,'summary':action_taken,'ready_to_send':False}
    except Exception as e:
        final_result=f"I encountered an Intrenal error. Can you please report on {CREATOR_EMAIL} email manually about this error with your prompt"
        return {'final_result':final_result,'summary':action_taken,'ready_to_send':False}




