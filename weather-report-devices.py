# MICROSOFT STUDENT ACCELERATOR 2020 - AZURE & CLOUD FUNDAMENTALS
# IOT SOLUTION FOR CITY WEATHER REPORTS
# Written by Dat Huynh
# z5223470@ad.unsw.edu.au
# School of Computer Science and Engineering, University of New South Wales

import os
from azure.iot.device import Message, IoTHubDeviceClient
import random
import time
import json

# generate random values of temperature, humidity, wind direction,
# wind intensity and rain based on the given device ID
def generate_weather(id):
    # random values for device 1 (Melbourne)
    if id == 1:
        t = random.uniform(-1.0,25.01)
        temp = round(t,2)
        hum = random.randint(70,100)
        wind_dir = random.randint(0,360)
        wind_int = random.randint(75,100)
        rain = random.randint(30,50)
    # random values for device 2 (Sydney)
    else:
        t = random.uniform(5.0,40.01)
        temp = round(t,2)
        hum = random.randint(30,75)
        wind_dir = random.randint(0,360)
        wind_int = random.randint(30,75)
        rain = random.randint(0,35)

    return temp, hum, wind_dir, wind_int, rain


# return the CONNECTION STRING of the given device ID
def choose_device(id):
    # device 1 (Melbourne)
    if (id == 1):
        connection_string = "HostName=msa-cloud-iot-hub.azure-devices.net;DeviceId=MyPythonDevice;SharedAccessKey=RYN8O7rjNgLBhfY4eUTKhucalJyRYEThD0TmJtHqxfQ="
    # device 2 (Sydney)
    else:
        connection_string = "HostName=msa-cloud-iot-hub.azure-devices.net;DeviceId=MyPythonDevice2;SharedAccessKey=Oy3FWm58W+8jeATOEVsvYJaGcTmJiPec0ujGjkvrM60="
    
    return connection_string


# publish simulated messages to the Azure IoT hub every 3 seconds
def send_message():
    # set up months and years for simulated messages
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    year = 2020

    # create instances of the device clients using the authentication provider
    connection_string1 = choose_device(1)
    device_client1 = IoTHubDeviceClient.create_from_connection_string(connection_string1, websockets=True)
    connection_string2 = choose_device(2)
    device_client2 = IoTHubDeviceClient.create_from_connection_string(connection_string2, websockets=True)

    # Connect device clients to the Iot hub
    device_client1.connect()
    device_client2.connect()

    m = 0
    while(True):
        m = m % 12
        try:
            # generate the message of device 1
            temp, hum, wind_dir, wind_int, rain = generate_weather(1)
            msg = {'deviceID': 1, 'location': 'melbourne', 'month': months[m], 'monthNo': (m+1), 'year': year, 'temperature': temp, 'humidity': hum,'wind_direction': wind_dir,'wind_intensity':wind_int,'rain':rain}
            message = json.dumps(msg)

            # Send the message to IoT hub
            print("Sending message...")
            device_client1.send_message(message)
            print("Message from Device 1 successfully sent!")
            print(message)
            time.sleep(4)

            # generate the message of device 2
            temp,hum,wind_dir,wind_int,rain = generate_weather(2)
            msg = {'deviceID': 2, 'location': 'sydney', 'month': months[m], 'monthNo': (m+1), 'year': year, 'temperature': temp, 'humidity': hum,'wind_direction': wind_dir,'wind_intensity':wind_int,'rain':rain}
            message = json.dumps(msg)

            # Send the message to IoT hub
            print("Sending message...")
            device_client1.send_message(message)
            print("Message from Device 2 successfully sent!")
            print(message)
            time.sleep(4)

            # update the month and year
            m += 1
            if m == 12:
                year += 1
        
        except KeyboardInterrupt:
            print("IoTHubClient stopped")
            return
        
        except:
            print("Unexpected error")
            time.sleep(4)

    # disconnect from the hub after finishing messaging
    device_client1.disconnect()
    device_client2.disconnect()


if __name__ == "__main__":
    send_message()
