# Arduino-for-the-Measurement-of-muon-lifetime
Arduino Code and Python Client for timestamping electronic pulses produced in an external Scintillator.
The code presented was created as part of the "Implementation of Arduino-based platform for measuring the muon’s mean lifetime" project  

## Instructions:
Before using the code, make sure the experimental Setup (Specifically the Sinctillator and additional circuits) is compatible with the Arduino UNO's digital input Vin.
For the Input Capture Interrupts to work, the pulses must feed into the Arduino UNO's Digital Pin8

[1]: Employ a copy of the Arduino IDE to upload the desired timestamping code
  (Keep into account that the 100kHz period measurer has a minimum pulse acquisition time of about 10 microseconds, while the High Frequency Period Measurer has a minimum data acquisition time of 2 microseconds)

[2]: Enter the required parameters into the Python LYMX code, set the experiment duration and COM port 

[3]: Wait for the data acquisition to finish. Experiment results will be saved to the specified file
