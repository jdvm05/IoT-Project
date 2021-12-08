import datetime
from gspread.utils import ValueRenderOption
import psutil
import requests
import serial

import gspread
from oauth2client import client
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint

# Connect to Google Sheets document 'IoT Data'
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open("IoT Data").sheet1

# Read incoming Arduino data from Serial port
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.reset_input_buffer()
motion = 0
light = 0
temperature = 0
while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        #print(line.split())
        for l in line.split():
            if l[0] == 'l':
                light = l[1:]
            if l[0] == 'm':
                motion = l[1:]
            if l[0] == 't':
                temperature = l[1:]
        
                temperature = 960 - int(temperature)
                light = round(int(light) / 29)
                motion = int(motion)*10
                
                data = { 
                    "date": str(datetime.datetime.now()), 
                    "movement": motion, 
                    "temperature": temperature, 
                    "brightness": light 
                }
                print(data)

                # Method 1: Send data to Google Sheets with Integromat
                # r = requests.post("https://hook.integromat.com/g1q4jupqs219uekvkcgrdf30j652ss28", json=data)
                # print(r.status_code)

                # Method 2: Send data to Google Sheets with Google Sheets API
                new_row = [data.get("date"), data.get("movement"), data.get("temperature"), data.get("brightness")]
                sheet.insert_row(new_row, 2, value_input_option="USER_ENTERED")
                pprint("New row: " + sheet.row_values(2))

# data = {"date": str(datetime.datetime.now()), "movement": psutil.disk_usage("/").percent, "temperature": psutil.cpu_percent(1),
#         "brightness": psutil.cpu_percent(1)}
# 
# print("data", data)

# email = dochia21@student.oulu.fi
# Password = Unioulu2021.
# https://hook.integromat.com/g1q4jupqs219uekvkcgrdf30j652ss28
