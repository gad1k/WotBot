python -m venv venv
call .\venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

set PATH_WOT=%CD%
echo cd /d %PATH_WOT%>>script_daily.bat
echo call .\venv\Scripts\activate.bat>>script_daily.bat
echo python main.py>>script_daily.bat
schtasks /create /tn "wot-daily" /tr %PATH_WOT%\script_daily.bat /sc onstart > wot_init.log