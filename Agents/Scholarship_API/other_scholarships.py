from .data import SCHOLARSHIP_DETAILS
async def get_other_scholarships_info():
    try:
        return SCHOLARSHIP_DETAILS
    except:
        return {'status':'Error occure while fetching other scholarships information'}






