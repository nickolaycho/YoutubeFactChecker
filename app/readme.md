How to run locally

1. Activate virtual environment
source venv/Scripts/activate

2. Install dependencies
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
Swagger su http://127.0.0.1:8000/docs