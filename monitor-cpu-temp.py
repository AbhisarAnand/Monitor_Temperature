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
import datetime

from constants import *


class MonitorTemperature:

    def __init__(self):
        self.temperature = self.get_temperature()
        self.maximum_temperature = MAX_TEMP
        self.minimum_temperature = MIN_TEMP
        self.temperatre_file = FILE_NAME
        self.sender_email = SENDING_EMAIL_ADDRESS
        self.receiver_email = EMAIL_LIST
        self.password = PASSWORD
        self.pi_name = NAME_OF_PI
        self.daily_update_low = TIME_DAILY_UPDATE_LOW_THRESHOLD
        self.daily_update_high = TIME_DAILY_UPDATE_HIGH_THRESHOLD

    def get_temperature(self) -> float:
        """This method gets and returns the temperature of the Raspberry Pi's CPU.

        Returns:
            float: The current temperature of the system.
        """
        self.temperature = float(os.popen("vcgencmd measure_temp").readline()[5:-3])
        return self.temperature           

    def write_temp_to_file(self, temp: float, current_time) -> None:
        """This method writes the current time and temperature to a file.

        Args:
            temp (float): The current temperature of the system.
            current_time (str): The current time of the system.
        """
        content = {current_time: str(temp)}
        Path(self.temperatre_file).touch(exist_ok=True)
        with open(self.temperatre_file, "a") as file:
            json.dump(content, file, indent=4)

    def email_send(self, temp, too_hot=False, too_cold=False, daily_update=False) -> None:
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
        sender_email = self.sender_email
        receiver_email = self.receiver_email
        password = self.password
        msg['From'] = sender_email
        msg['To'] = receiver_email
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
                    self.pi_name)
                body = "{} Raspberry Pi is getting hot.\nThe temperature was {}".format(
                    self.pi_name, temp)
            if too_cold:
                msg['Subject'] = 'COLD Temperature Warning Raspberry Pi - {}'.format(
                    self.pi_name)
                body = "{} Raspberry Pi is getting cold.\nThe temperature was {}".format(
                    self.pi_name, temp)
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
    def send_update_email(self) -> None:
        """
        This method sends an email to the developers with the temperature measured by the measure_temp function when the time is 10:00 PM EST.
        :return:
        """
        if self.daily_update_low < datetime.datetime.now() < self.daily_update_high:
            self.email_send(temp=None, too_hot=False,
                           too_cold=False, daily_update=True)
    
    def main(self) -> None:
        """
        This method measures the temperature of the Raspberry Pi's CPU and emails the developers if they are too hot or too cold.
        """
        current_time = str(time.strftime("%Y-%m-%d %H:%M:%S"))
        self.write_temp_to_file(self.temperature, current_time)
        self.send_update_email()
        if self.temperature >= self.maximum_temperature:
            self.email_send(temp=self.temperature, too_hot=True, too_cold=False)
        if self.temperature <= self.minimum_temperature:
            self.email_send(temp=self.temperature, too_hot=False, too_cold=True)


if __name__ == '__main__':
    monitor_temperature_inst = MonitorTemperature()
    monitor_temperature_inst.main()
