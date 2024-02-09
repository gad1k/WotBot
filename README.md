### Description
Bot helps to get a gift from the daily calendar of WoT.

### Prerequisites
Since the bot is developed in Python, it's crucial to install the Python interpreter and add its location to an environment variable named <b>Path</b>.

<u>Download Link</u>:
```
https://www.python.org/downloads/
```

### Initial Configuration
At the very beginning, you should run the script below:
```
script_init.bat
```
This script performs the following actions:
- creates a virtual environment
- downloads all the necessary dependencies
- generates the daily script (*script_daily.bat*)
- sets up a schedule task (*WotDaily*)

Then specify the relevant username and password to <b>config.json</b> file:
```
{
  "driver": "Chrome",
  "url": "https://tanki.su/ru/daily-check-in/",
  "username": "",
  "password": "",
  "token": ""
}
```
**Note** If you want to get notifications via Telegram, you will also need to provide the appropriate token.

### Daily Checkin
The schedule task runs this script every hour. At the same time, you can run the script manually:
```
script_daily.bat
```