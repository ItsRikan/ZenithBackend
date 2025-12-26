from Agents.agent_runner import agent_runner
from fastapi import FastAPI
from input_schema import InputSchema,InputMailSchema
from Agents.send_mail import mailing_tool
app = FastAPI()

@app.get('/')
async def get_health():
    return {'status':'healthy'}

@app.post('/query')
async def get_response(input_schema:InputSchema):
    return await agent_runner(user_query=input_schema.user_query,prev_action=input_schema.prev_action)

@app.post('/send_mail')
async def send_mail(mail_input:InputMailSchema):
    return await mailing_tool(dept_name=mail_input.department,draft=mail_input.draft)


