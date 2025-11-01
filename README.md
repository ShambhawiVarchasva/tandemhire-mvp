# TandemHire MVP - scaffolded

Run backend locally:
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r app/requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

Run frontend locally:
cd frontend
npm install
npm run dev
