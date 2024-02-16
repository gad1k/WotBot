import requests

from exception import InactiveChatException, InvalidTokenException


class TelegramExporter:
    def __init__(self, token):
        self.token = token
        self.chat_id = None


    def try_upload_cached_chat_id(self):
        try:
            with open(".settings") as settings:
                self.chat_id = settings.readline()
        except FileNotFoundError:
            pass


    def try_retrieve_chat_id_remotely(self):
        try:
            if not self.chat_id:
                url = f"https://api.telegram.org/bot{self.token}/getUpdates"
                response = requests.get(url).json()

                self.chat_id = response["result"][-1]["message"]["chat"]["id"]
                self.save_settings()
        except IndexError:
            raise InactiveChatException()
        except KeyError:
            raise InvalidTokenException()


    def save_settings(self):
        with open(".settings", "w", encoding="utf-8") as settings:
            settings.write(str(self.chat_id))


    def send_message(self, message):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage?chat_id={self.chat_id}&text={message}"
        requests.get(url)
