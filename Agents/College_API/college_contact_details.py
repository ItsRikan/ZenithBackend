import json
import os
import sys

async def get_college_contact_details():
    try:
        root_dir = sys.path[0]
        file_path = os.path.join(root_dir, 'data', 'college_contact_details.json')
        with open(file_path,'r') as f:
            obj = json.load(f)
            return obj
    except:
        return {'status':'Error occure while fetching other scholarships information'}


