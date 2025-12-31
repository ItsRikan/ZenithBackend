import json

async def get_college_data():
    try:
        with open('data/college_data.json','r') as f:
            obj = json.load(f)
            return obj
    except:
        return {'status':'Error occure while fetching other scholarships information'}







