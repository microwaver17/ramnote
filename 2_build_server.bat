rem nothing to do
cd server
python -m venv .\venv
.\venv\Scripts\pip install -r requirements.txt
.\venv\Scripts\python maintenance\create_table.py
cd ../