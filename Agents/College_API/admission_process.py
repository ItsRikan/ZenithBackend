import json
import os

async def get_admission_info():
    try:
        # Get the directory of the current file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Go up three levels to reach the root: Agents/College_API -> Agents -> root
        root_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
        file_path = os.path.join(root_dir, 'data', 'admission_data.json')
        with open(file_path,'r') as f:
            obj = json.load(f)
            return obj
    except:
        return {'status':'Error occure while fetching other scholarships information'}





