import json
import os
import sys

async def get_admission_info():
    try:
        root_dir = os.path.dirname(sys.path[0])
        file_path = os.path.join(root_dir, 'data', 'admission_data.json')
        with open(file_path,'r') as f:
            obj = json.load(f)
            return obj
    except:
        return {'status':'Error occure while fetching other scholarships information'}





