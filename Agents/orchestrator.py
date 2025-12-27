from .frontlayer_agent.output_schema import Action
from .College_API.about import get_college_data
from .College_API.admission_process import get_admission_info
from .College_API.placement_details import get_top_placement_records
from .College_API.college_contact_details import get_college_contact_details
from .College_API.latest_events_and_news import get_news_and_events
from .Scholarship_API.about import get_svmcm_about
from .Scholarship_API.other_scholarships import get_other_scholarships_info
from .Scholarship_API.schedule import get_svmcm_schedule
from .send_mail.mailing_orchestrator import mailing_orchestrator


async def run_action(action: Action):
    if action.action == "answer":
        return action.message
    if action.action == "send_email":
        response = await mailing_orchestrator(action=action)
        return response
    
    # College API/Details
    if action.action == "fetch_college_api":
        if action.fetch_college_api_purpose.lower()=="admission":
            return await get_admission_info()
        elif action.fetch_college_api_purpose.lower()=="placement_record":
            return await get_top_placement_records()
        elif action.fetch_college_api_purpose.lower()=="details":
            return await get_college_data()
        elif action.fetch_college_api_purpose.lower()=="college_contact_details":
            return await get_college_contact_details()
        elif action.fetch_college_api_purpose.lower()=="news_and_events":
            return await get_news_and_events()
        elif action.fetch_college_api_purpose.lower()=="everything":
            admission = await get_admission_info()
            details = await get_college_data()
            placements = await get_top_placement_records()
            news_and_events = await get_news_and_events()
            return {"college_details":details,"admission":admission,"placement_record":placements,"news_and_events":news_and_events}
        
    # Scholarship Details
    if action.action == "search_scholarship":
        if action.search_scholarship_purpose.lower()=="all_available_scholarship":
            return await get_other_scholarships_info()
        if action.search_scholarship_purpose.lower()=="about_svmcm":
            return await get_svmcm_about()
        if action.search_scholarship_purpose.lower()=="schedule_of_svmcm":
            return await get_svmcm_schedule()
        if action.search_scholarship_purpose.lower()=="everything":
            all_scholarship_info = await get_other_scholarships_info()
            about = await  get_svmcm_about()
            schedule = await get_svmcm_schedule()
            return {"all_available_scholarships":all_scholarship_info,"about_svmcm":about,"schedule":schedule}
