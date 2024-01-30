python -m venv venv
call .\venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

rem создать планировщик задач при заупске компьютера 
schtasks /create /tn "wot-daily" /tr %CD%\script_daily.bat /sc onstart > wot_init.log