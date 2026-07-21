import serial 
import time

arduino = serial.Serial("COM3", 115200)
time.sleep(2)

while True:
    message = input("Send: ")
    arduino.write((message + "\n").encode())