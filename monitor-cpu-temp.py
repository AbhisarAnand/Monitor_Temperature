from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.utils import formatdate
from email import encoders
from pathlib import Path

import keyring
import os
import smtplib
import ssl
import json
import time

from constants import *


class MonitorTemperature:

    @classmethod
    def measure_temp(cls) -> None:
        """
        This method measures the temperature of the Raspberry Pi's CPU and emails the developers if they are too hot or too cold.
        """
        temp = os.popen("vcgencmd measure_temp").readline()
        temp = float(temp[5:-3])
        current_time = str(time.strftime("%Y-%m-%d %H:%M:%S"))
        cls.write_temp_to_file(temp, current_time)
        cls.send_update_email()
        if temp >= MAX_TEMP:
            cls.email_send(temp=temp, too_hot=True, too_cold=False)
        if temp <= MIN_TEMP:
            cls.email_send(temp=temp, too_hot=False, too_cold=True)

    @classmethod
    def write_temp_to_file(cls, temp: float, current_time) -> None:
        """This method writes the current time and temperature to a file.

        Args:
            temp (float): The current temperature of the system.
            current_time (str): The current time of the system.
        """
        content = {current_time: str(temp)}
        Path(FILE_NAME).touch(exist_ok=True)
        with open(FILE_NAME, "w") as file:
            json.dump(content, file, indent=4)


    @classmethod
    def email_send(cls, temp, too_hot=False, too_cold=False, daily_update=False) -> None:
        """
        This method sends an email to the developers with the temperature measured by the measure_temp function.
        :param temp:
        :type temp: float
        :param too_hot:
        :type too_hot: bool
        :param too_cold:
        :type too_cold: bool
        :return:
        """
        msg = MIMEMultipart()
        sender_email = "maskdetector101@gmail.com"
        receiver_email = "adityaanand.muz@gmail.com, srinivassriram06@gmail.com, raja.muz@gmail.com, abhisar.muz@gmail.com"
        password = keyring.get_password("gmail", "maskdetector101.gmail.com")
        msg['From'] = 'maskdetector101@gmail.com'
        msg['To'] = "adityaanand.muz@gmail.com, srinivassriram06@gmail.com, raja.muz@gmail.com, abhisar.muz@gmail.com"
        msg['Date'] = formatdate(localtime=True)
        if daily_update:
            msg['Subject'] = "Daily update: Here is the update for the temperature of the PI on {}".format(
                formatdate(localtime=True))
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(FILE_NAME).load())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                            'attachment', filename=FILE_NAME)
            msg.attach(part)
        else:
            if too_hot:
                msg['Subject'] = 'HOT Temperature Warning Raspberry Pi - {}'.format(
                    NAME_OF_PI)
                body = "{} Raspberry Pi is getting hot.\nThe temperature was {}".format(
                    NAME_OF_PI, temp)
            if too_cold:
                msg['Subject'] = 'COLD Temperature Warning Raspberry Pi - {}'.format(
                    NAME_OF_PI)
                body = "{} Raspberry Pi is getting cold.\nThe temperature was {}".format(
                    NAME_OF_PI, temp)
        msg.attach(MIMEText(body, "plain"))
        context = ssl.create_default_context()
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(
                    sender_email, receiver_email.split(","), msg.as_string())
        except Exception as e:
            print(type(e).__name__ + ': ' + str(e))

    @classmethod
    def send_update_email(cls) -> None:
        """
        This method sends an email to the developers with the temperature measured by the measure_temp function when the time is 10:00 PM EST.
        :return:
        """
        if time.strftime("%H:%M") == TIME_DAILY_UPDATE:
            cls.email_send(temp=None, too_hot=False,
                           too_cold=False, daily_update=True)


if __name__ == '__main__':
    MonitorTemperature.measure_temp()
