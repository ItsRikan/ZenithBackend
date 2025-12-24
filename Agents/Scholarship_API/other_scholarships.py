import json

async def get_other_scholarships_info():
    try:
        with open('data/scholarship_data.json','r') as f:
            obj = json.load(f)
            return obj
    except:
        return {'status':'Error occure while fetching other scholarships information'}






