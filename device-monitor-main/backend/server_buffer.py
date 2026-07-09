from datetime import datetime

MAX_READINGS = 30


class ServerBuffer:

    def __init__(self):

        self.readings = []

    def add_reading(self, reading):

        reading["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.readings.append(reading)

        if len(self.readings) > MAX_READINGS:

            self.readings.pop(0)

    def get_readings(self):

        return self.readings

    def clear(self):

        self.readings.clear()


buffer = ServerBuffer()