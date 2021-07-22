import socket
import os

NAME_OF_PI = socket.gethostname()

MAX_TEMP = 50.0

MIN_TEMP = 22.0

FILE_NAME = os.path.join(os.path.dirname(os.path.realpath(__file__)), "temperature.json")

TIME_DAILY_UPDATE = "22:00"