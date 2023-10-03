"""
Created on Fri Sept 01 2023

@author: Artemis 
"""

#Imports

import serial
import matplotlib as mlp
#mlp.rcParams['text.usetex'] = True
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
#import scienceplots

#Arduino Serial Init

arduino_port = 'COM4'  # Change this to the appropriate port
baud_rate = 115200

# Initialize serial communication with Arduino
ser = serial.Serial(arduino_port, baud_rate, timeout=1)

#Time Calculation
def lapse(T1, T2, TOV):
    Res = (65535*TOV - T1 ) + T2
    if Res > 0:
        return Res
    elif Res < 0:
        return (65535 - T1 ) + T2
    else:
        return 1


def time (D, preScale=1, Clock=16000000):
    return D*(preScale/Clock)

def frequency(T):
    return (1/T)

#Saving the Data to a TXT file
def save2TXT(arr, file_name):
    try:
        with open(file_name, 'w') as file:
            for item in arr:
                file.write(str(item) + '\n')
        print(f"Array saved to {file_name} successfully.")
    except Exception as e:
        print(f"Error: {e}")


EXPORT_T = []
EXPORT_F = []

try:
    for i in range(100):
        # Read the data sent by Arduino
        arduino_data = ser.readline().decode('ascii').strip()
        timeVect = arduino_data.split(":")
        print(timeVect)
        
except KeyboardInterrupt:
    ser.close()
    print("Serial connection closed.")


try:
    for i in range(1000):
        # Read the data sent by Arduino
        arduino_data = ser.readline().decode('ascii').strip()
        timeVect = arduino_data.split(":")
        if len(timeVect)==3: # Split the data into two integers
            T1_str, T2_str, TOV_str = arduino_data.split(':')
        
        # Convert the strings to integers
            T1 = int(T1_str)
            T2 = int(T2_str)
            TOV = int(TOV_str)
        
        # Perform the multiplication
            lap = lapse(T1, T2, TOV)
            t = time(lap)
            freq = frequency(t)
        
        # Print the result
            #print(f"Time Interval {t} Seconds ")
            #print(f" {freq} Hz ")
        #MakeExport
            EXPORT_F.append(freq)
            EXPORT_T.append(t)
            
        else:
            print("Time Measure fail")
            print(timeVect)
        
except KeyboardInterrupt:
    ser.close()
    print("Serial connection closed.")

print(EXPORT_T[-1])
print(EXPORT_F[-1])
file_F = "FreqTest.txt"
file_T = "PeriodTest.txt"
save2TXT(EXPORT_F, file_F)
save2TXT(EXPORT_T, file_T)
