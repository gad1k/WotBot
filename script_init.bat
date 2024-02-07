python -m venv venv
call .\venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo cd /d %CD% >> script_daily.bat
echo call .\venv\Scripts\activate.bat >> script_daily.bat
echo python main.py >> script_daily.bat

schtasks /create /tn "wot-daily" /tr %CD%\script_daily.bat /sc onstart