from .data import ADMISSION_DETAILS

async def get_admission_info():
    try:
        return ADMISSION_DETAILS
    except:
        return {'status':'Error occure while fetching other scholarships information'}





