from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate

import keyring
import os
import smtplib
import ssl

from constants import NAME_OF_PI, MAX_TEMP, MIN_TEMP


class MonitorTemperature:

    @classmethod
    def measure_temp(cls):
        temp = os.popen("vcgencmd measure_temp").readline()
        temp = float(temp[5:-3])
        if temp >= MAX_TEMP:
            cls.email_send(temp=temp, too_hot=True, too_cold=False)
        if temp <= MIN_TEMP:
            cls.email_send(temp=temp, too_hot=False, too_cold=True)

    @classmethod
    def email_send(cls, temp, too_hot=False, too_cold=False):
        msg = MIMEMultipart()
        sender_email = "maskdetector101@gmail.com"
        receiver_email = "adityaanand.muz@gmail.com, srinivassriram06@gmail.com, raja.muz@gmail.com, abhisar.muz@gmail.com"
        password = keyring.get_password("gmail", "maskdetector101.gmail.com")
        msg['From'] = 'maskdetector101@gmail.com'
        msg['To'] = "adityaanand.muz@gmail.com, srinivassriram06@gmail.com, raja.muz@gmail.com, abhisar.muz@gmail.com"
        msg['Date'] = formatdate(localtime=True)
        if too_hot:
            msg['Subject'] = 'HOT Temperature Warning Raspberry Pi - {}'.format(NAME_OF_PI)
            body = "{} Raspberry Pi is getting hot.\nThe temperature was {}".format(NAME_OF_PI, temp)
        if too_cold:
            msg['Subject'] = 'COLD Temperature Warning Raspberry Pi - {}'.format(NAME_OF_PI)
            body = "{} Raspberry Pi is getting cold.\nThe temperature was {}".format(NAME_OF_PI, temp)
        msg.attach(MIMEText(body, "plain"))
        context = ssl.create_default_context()
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email.split(","), msg.as_string())
        except Exception as e:
            print(type(e).__name__ + ': ' + str(e))


if __name__ == '__main__':
    MonitorTemperature.measure_temp()
