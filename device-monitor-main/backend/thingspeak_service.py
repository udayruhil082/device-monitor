import requests

CHANNEL_ID = "3426883"
READ_API_KEY = "8XZ1WL6NHYO31JCT"


class ThingSpeakService:

    def get_latest_data(self):

        url = (
            f"https://api.thingspeak.com/channels/"
            f"{CHANNEL_ID}/feeds/last.json"
            f"?api_key={READ_API_KEY}"
        )

        try:

            response = requests.get(url, timeout=5)

            return response.json()

        except Exception as e:

            return {
                "error": str(e)
            }


thingspeak = ThingSpeakService()