import socket
import os
import datetime

NAME_OF_PI = socket.gethostname()

MAX_TEMP = 50.0

MIN_TEMP = 22.0

FILE_NAME = os.path.join(os.path.dirname(os.path.realpath(__file__)), "temperature.json")

TIME_DAILY_UPDATE_LOW_THRESHOLD = datetime.datetime.now().replace(hour=23, minute=8, second=0, microsecond=0)
TIME_DAILY_UPDATE_HIGH_THRESHOLD = datetime.datetime.now().replace(hour=0, minute=2, second=0, microsecond=0)

EMAIL_LIST = "adityaanand.muz@gmail.com, srinivassriram06@gmail.com, raja.muz@gmail.com, abhisar.muz@gmail.com, ssriram.78@gmail.com"
SENDING_EMAIL_ADDRESS = "maskdetector101@gmail.com"
PASSWORD = ""
