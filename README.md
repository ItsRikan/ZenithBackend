# HackZenith Backend

## Local Development Setup

### 1) Clone the repository
```bash
git clone https://github.com/ItsRikan/ZenithBackend.git
cd ZenithBackend
```

### 2) Create a virtual environment and activate it (For Windows)
```bash
python -m venv venv
venv\Scripts\activate
```

### 3) Create a `.env` file with required environment variables
```env
GOOGLE_API_KEY=your_google_api_key_here
GMAIL_PASSWORD=your_gmail_app_password_here
```

### 4) Update email configuration
Navigate to `Agents/details.py` and update:
- `SENDER_EMAIL` with your Gmail address
- `DEPT_TO_MAILS` dictionary with appropriate department emails

### 5) Install dependencies and run
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`
