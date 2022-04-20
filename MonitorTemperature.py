import os


class MonitorTemperature:

    def __init__(self):
        self.temperature = 0.0

    def get_current_temperature(self) -> float:
        """This method gets and returns the temperature of the Raspberry Pi's CPU.

        Returns:
            float: The current temperature of the system.
        """
        self.temperature = float(os.popen("vcgencmd measure_temp").readline()[5:-3])
        return self.temperature


if __name__ == "__main__":
    import time

    monitor = MonitorTemperature()
    while True:
        print("Temperature of the PI: " + str(monitor.get_current_temperature()))
        time.sleep(1)
