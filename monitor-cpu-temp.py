import os


def measure_temp():
    temp = os.popen("vcgencmd measure_temp").readline()
    temp = temp[5:-3]
    temp = float(temp)
    print(temp)
    if temp >= 50.0:
        print("Pi is too hot and the temp is {}".format(temp))
    if temp <= 22.0:
        print("Pi is getting too cold and the temp is {}".format(temp))


if __name__ == '__main__':
    measure_temp()
