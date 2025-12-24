# ZenithProject
### 1) Run these two commands
```bash
 - git clone https://github.com/ItsRikan/ZenithProject.git
 - cd ZenithProject
```
### 2) Inside ZenithProject create a .env file and store : 
```
GOOGLE_API_KEY=...
GMAIL_PASSWORD=...
```
### 3) Move to Agents and find details.py file : 
- Enter your different email in 
SENDER_EMAIL and DEPT_TO_MAILS's INFO, PAYMENT and MANAGEMENT

### 4) Run The following command from ZenithProject
```bash
pip install -r requirments.txt
uvicorn main:app --reload
```




