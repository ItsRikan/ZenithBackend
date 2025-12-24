from .frontlayer_agent.output_schema import Action
def clean_json(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()

    return text


def action_taken_format(action:Action):
    return {
        "action":action.action,
        "department":action.department,
        "fetch_college_api_purpose":action.fetch_college_api_purpose,
        "search_scholarship_purpose":action.search_scholarship_purpose,
        "send_mail_purpose":action.send_mail_purpose,
        "user_details_for_mail":action.user_details_for_mail,
        "mail_objective":action.mail_objective,
        "message":action.message,
        "confidence_score":action.confidence_score,
    }



