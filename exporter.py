import requests


class TelegramExporter:
    def __init__(self, token):
        self.token = token
        self.chat_id = None


    def retrieve_chat_id(self):
        url = f"https://api.telegram.org/bot{self.token}/getUpdates"
        response = requests.get(url).json()

        self.chat_id = response["result"][-1]["message"]["chat"]["id"]


    def send_message(self, message):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage?chat_id={self.chat_id}&text={message}"
        requests.get(url)