import json

async def get_admission_info():
    try:
        with open('data/admission_data.json','r') as f:
            obj = json.load(f)
            return obj
    except:
        return {'status':'Error occure while fetching other scholarships information'}





