import json

async def get_college_contact_details():
    try:
        with open('data/college_contact_details.json','r') as f:
            obj = json.load(f)
            return obj
    except:
        return {'status':'Error occure while fetching other scholarships information'}


