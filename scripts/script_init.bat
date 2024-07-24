rem Set up a virtual environment
python -m venv .venv
call .\.venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

rem Define variables for the settings
set task_name=WotDaily
set task_daily="%cd%\script_daily.bat"
set task_schedule="wscript %cd%\script_schedule.vbs"
set task_trigger=Hourly
set task_interval=1
set task_owner=%username%

rem Create a bat file for the task
echo cd /d %cd% > script_daily.bat
echo call .\.venv\Scripts\activate.bat >> script_daily.bat
echo python main.py >> script_daily.bat

rem Create a vbs file for the schedule
echo set WshShell = CreateObject("WScript.Shell") > script_schedule.vbs
echo WshShell.run %task_daily%, 0, True >> script_schedule.vbs

rem Create the task using schtasks command
schtasks /create /tn %task_name% /tr %task_schedule% /sc %task_trigger% /mo %task_interval% /ru %task_owner% /f