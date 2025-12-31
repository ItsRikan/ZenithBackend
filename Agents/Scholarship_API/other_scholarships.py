import json
import os

async def get_other_scholarships_info():
    try:
        file_path = os.path.join('data', 'scholarship_data.json')
        with open(file_path,'r') as f:
            obj = json.load(f)
            return obj
    except:
        return {'status':'Error occure while fetching other scholarships information'}






