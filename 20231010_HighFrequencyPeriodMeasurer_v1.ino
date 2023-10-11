/*
* Arduino HighSpeed-Speed Pulse Timestamper 
* Version release 1.0 2023/10/10  
* By Alex Artemis Castelblanco
* Developed for the proyect: 
  "Implementation of an Arduino-based platform for the measurement of the Muon's mean Lifetime"
*/


/*
*Initialization of measurement Variables
*/
bool activeMeas = 0; //Used to Tell wether this is the first or second consecutive rising wavefront
unsigned long T; //Stores the value of the first Measurement  
unsigned long T2 = 0; // Stores the value of the second measurement
int period = 0; //Stores the calculated value of the Signal's period


/*
*Timer 1 overflow Interrupt handler 
*Increases the Value of T1OVF_Counter each time there's a Timer Overflow Interrupt
*/
ISR(TIMER1_OVF_vect)
{
}


/*
*Timer 1 Input Interrupt handler 
*/
ISR(TIMER1_CAPT_vect)
{
  
  asm volatile (
    "cli \n\t" //Disables Interrupts 
  );
  
  //Checks activeMeas to know wether it's the first or second consecutive wavefront
  if(!activeMeas) 
  {
    //if activeMeas is False: then Stores the value of Timer1 in T, Resets T1OVF_Counter, and sets activeMeas True 
    asm volatile (
      "movw %0, %1    \n\t"  // Moves ICR1 into T 
      "ldi r16, 1     \n\t" // Set r16 to 1
      "sts %2, r16    \n\t" // Store r16 into activeMeasurement

      : "=r" (T) // Output operand (T) in a register
      : "r" (ICR1),   // Input operand (ICR1) in a register
        "m" (activeMeas) //Input operand (activeMeas)
      : "r16" // Clobbered register
    );
  }
  else //if activeMeas is True: Stores the value of Timer1 in T2, sets activeMeas False, and sends the Information via Serial Print
  {
    
    T2 = ICR1; //Stores ICR1 (Timer1) in T2
    activeMeas = 0; //Sets activeMeas to False
    period = calPeriod(T, T2, 0); //calculates the Period of the Signal (In Clock Cycles)
    //Serial.println(period);
    //Prints the Via Serial
    Serial.print(T);
    Serial.print(":");
    Serial.print(T2);
    Serial.print(":");
    Serial.println(0);
  }

  asm volatile (
    "sei \n\t" //re-enables interrupts
  );
}
 

/*
* Period Calculator
*/
int calPeriod(int T1, int T2, int TOVF){
  return T2 + (65536 * TOVF) - T1;
}

/*
* Setup Function
*/
void setup()
{
  TCCR1A = 0;           // Initializes Timer1A
  TCCR1B = 0;           // Initializes Timer1B
  TCCR1B = 0b01000001;  // Internal Clock, Prescaler = 1, ICU Filter OFF, ICU Pin RISING
  TIMSK1 |= B00100001;  // Enables Timer OVF & CAPT Interrupts
  Serial.begin(115200);   //Initializes the Serial port 
}
 
//Arduino's Loop Function left unused
void loop()
{

}