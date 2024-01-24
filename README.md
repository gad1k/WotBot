### Description
Bot helps to get a gift from the daily calendar of WoT.

### Prerequisites
Since the bot is developed in Python, it's crucial to install the Python interpreter and add its location to an environment variable named <b>Path</b>.

<u>Download Link</u>:
```
https://www.python.org/downloads/
```

### Initial Configuration
Before using the bot on a daily basis, you need to create a virtual environment and download all the necessary dependencies by running the following script:
```
script_init.bat
```
Then specify the relevant username and password to <b>config.json</b> file:
```
{
  "driver": "Chrome",
  "url": "https://tanki.su/ru/daily-check-in/",
  "username": "",
  "password": ""
}
```

### Daily Checkin
To receive a gift, it's just needed to run the next script:
```
script_daily.bat
```