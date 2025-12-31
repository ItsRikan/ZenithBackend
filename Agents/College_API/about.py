from .data import ABOUT_COLLEGE
async def get_college_data():
    try:
        return ABOUT_COLLEGE
    except:
        return {'status':'Error occure while fetching other scholarships information'}







