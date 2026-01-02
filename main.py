from Agents.agent_runner import agent_runner
from fastapi import FastAPI
from input_schema import InputSchema,InputMailSchema
from Agents.send_mail.mailing_tool import mailing_tool
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


origins = ["https://zenith-frontend-production1.vercel.app"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def health_check():
    return {'status':'healthy'}
@app.post('/query')
async def get_response(input_schema:InputSchema):
    return await agent_runner(user_query=input_schema.user_query,prev_action=input_schema.prev_action)

@app.post('/send_mail')
async def send_mail(mail_input:InputMailSchema):
    return await mailing_tool(dept_name=mail_input.department,draft=mail_input.draft)


