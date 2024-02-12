rem Set up a virtual environment
python -m venv .venv
call .\.venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

rem Create a bat file for the task
echo cd /d %cd% >> script_daily.bat
echo call .\.venv\Scripts\activate.bat >> script_daily.bat
echo python main.py >> script_daily.bat

rem Define variables for the settings
set task_name=WotDaily
set task_command="%cd%\script_daily.bat"
set task_trigger=Hourly
set task_interval=1
set task_owner=%username%

rem Create the task using schtasks command
schtasks /create /tn %task_name% /tr %task_command% /sc %task_trigger% /mo %task_interval% /ru %task_owner% /f