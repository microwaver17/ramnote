rem nothing to do
cd server
python -m venv .\venv
call .\venv\Scripts\activate.bat
pip install -r requirements.txt
python maintenance\create_table.py
cd ../