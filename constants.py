import socket
import os
import datetime

NAME_OF_PI = socket.gethostname()

MAX_TEMP = 50.0

MIN_TEMP = 22.0

FILE_NAME = os.path.join(os.path.dirname(os.path.realpath(__file__)), "temperature.json")

TIME_DAILY_UPDATE_LOW_THRESHOLD = datetime.datetime.now().replace(hour=9, minute=59, second=0, microsecond=0)
TIME_DAILY_UPDATE_HIGH_THRESHOLD = datetime.datetime.now().replace(hour=10, minute=3, second=0, microsecond=0)
