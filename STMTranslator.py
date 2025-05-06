import requests

class STMTranslator:
    def __init__(self, api_url="http://127.0.0.1:5000/translate"):
        self.api_url = api_url

    def translate(self, text):
        try:
            response = requests.post(
                self.api_url,
                json={"text": text},
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            response.raise_for_status()
            return response.json()["translated"]
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return ""
