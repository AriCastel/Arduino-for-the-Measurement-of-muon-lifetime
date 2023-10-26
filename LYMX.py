"""
* Windows Host Code for LYMX interface
* By Alex Artemis Castelblanco
* version 0.01 pre release
* Developed for the proyect: 
  "Implementation of an Arduino-based platform for the measurement of the Muon's mean Lifetime"
"""

import time 
import logging
import serial
from datetime import datetime


#Initializes the Arduino Board
def sketch_Load():
    logging.debug("sketch_Load was called but the function is not yet usable: Make sure to use the IDE to load the Sketch Manually")


#Period Calculation        
def period(T1, T2, TOVF=0, preScale = 1, ClockM=16):
    if T2 > T1:
        count = T2 - T1
    elif TOVF>0:
        count = T2 - T1 + 65536*TOVF
    else:
        count = 1
    micras = count*(preScale/(ClockM*(10**6)))
    logging.debug(f"Period Calculated as {micras}")
    return micras 

    
    
#Saves Data to file 
def save(data, file_name): 
    try:
        with open(file_name, 'w') as file:
            for item in data:
                file.write(str(item) + '\n')
        logging.info(f"Data saved to {file_name} successfully.")
    except Exception as e:
        logging.error(f"Error: {e}")    

#Code Initialization
def serInit(arduino_port = 'COM6', baud_rate = 115200):
    
    #Sets up the Terminal Print Logging and Debugging  
    level = logging.DEBUG
    fmt = '[%(levelname)s] %(asctime)s - %(message)s'
    logging.basicConfig(level=level, format=fmt)

    logging.info("Initializing...")
    
    try: 
        seri = serial.Serial(arduino_port, baud_rate, timeout=1)    #Serial Initialization
        sketch_Load()   #arduino Initialization
        logging.info("Ready!")
        return seri
        
    except: 
        logging.error(f"Loading {(arduino_port)} failed, please enter a valid port as COM#")


#Main Loop
def main(seri, file_Name, experiment_Duration = 3, save_Interval = 1):
    Data = []
    end_time = time.time() + (experiment_Duration * 60)
    last_save = time.time()

    
    try:
        while time.time() < end_time:
            # Read the data sent by Arduino
            arduino_data = seri.readline().decode('ascii').strip()
            timeVect = arduino_data.split(":")
            logging.debug(f"Serial Data read as {timeVect}")
            
            if len(timeVect)==3: # Split the data into two integers
                T1_str, T2_str, TOVF_str = arduino_data.split(':')
                T1 = int(T1_str)
                T2 = int(T2_str)
                TOVF = int(TOVF_str)
                timestamp = time.ctime()
                lapse = period(T1, T2, TOVF)
                event = (lapse, timestamp)
                Data.append(event)
                logging.debug(f"Event {event} logged successfully") 
            else:
                logging.error("Timer Fail")
            
            if time.time() - last_save >= save_Interval*60:
                save(Data, file_Name)
                logging.info(f"Data autosaved as {file_Name} at {time.ctime()}")
                last_save = time.time()
        seri.close()    
    except KeyboardInterrupt:
        seri.close()
                
        
     
     

serial = serInit()
logging.info(f"Experiment Started at {time.ctime()}")
main(serial, "TestRun")
logging.info(f"Experiment Ended at {time.ctime()}")