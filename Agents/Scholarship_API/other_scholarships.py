import json
import os

async def get_other_scholarships_info():
    try:
        # Get the directory of the current file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Go up three levels to reach the root: Agents/Scholarship_API -> Agents -> root
        root_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
        file_path = os.path.join(root_dir, 'data', 'scholarship_data.json')
        with open(file_path,'r') as f:
            obj = json.load(f)
            return obj
    except:
        return {'status':'Error occure while fetching other scholarships information'}






