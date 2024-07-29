:: Set up a virtual environment
python -m venv ..\.venv
call ..\.venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r ..\requirements.txt

:: Define variables for the settings
set task_name=WotDaily
set task_daily="%cd%\script_daily.bat"
set task_schedule="wscript %cd%\script_schedule.vbs"
set task_trigger=Hourly
set task_interval=1
set task_owner=%username%

:: Create a bat file for the task
echo :: Daily Script > script_daily.bat
echo for %I in ("%cd%\..") do set "project_dir=%~fI" >> script_daily.bat
echo cd /d %project_dir% >> script_daily.bat
echo set pythonpath=%project_dir% >> script_daily.bat
echo call .venv\Scripts\activate.bat >> script_daily.bat
echo cd .\modules >> script_daily.bat
echo python main.py >> script_daily.bat

:: Create a vbs file for the schedule
echo set WshShell = CreateObject("WScript.Shell") > script_schedule.vbs
echo WshShell.run %task_daily%, 0, True >> script_schedule.vbs

:: Create the task using schtasks command
schtasks /create /tn %task_name% /tr %task_schedule% /sc %task_trigger% /mo %task_interval% /ru %task_owner% /f