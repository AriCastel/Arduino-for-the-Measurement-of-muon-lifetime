/*
* Arduino Pulse Timestamper 
*/

bool activeMeas = 0;
//uint8_t T1OVF_Counter = 0;
volatile unsigned int T; 
unsigned long T2 = 0;



ISR(TIMER1_OVF_vect)
{
  //T1OVF_Counter++;
}


ISR(TIMER1_CAPT_vect)
{
  asm volatile (
    "cli \n\t");
  if(!activeMeas)
  {


///////
    asm volatile (
    "movw %0, %1"  // Move the 16-bit integer into the unsigned long
    : "=r" (T) // Output operand (myLong) in a register
    : "r" (ICR1)   // Input operand (myInt) in a register
  );

/////

    //T = ICR1;

    asm volatile (  
    "ldi r16, 1                      \n\t" // Set r16 to 1
    "sts %0, r16   \n\t" // Store r16 into activeMeasurement

    "clr r16                         \n\t" // Reset r16 to 0
    //"sts %1, r16       \n\t" // Store r16 into T1OVF_Counter

    : // No output operands
    :  "m" (activeMeas) // Input operands
    //, "m" (T1OVF_Counter)
    : "r16" // Clobbered register
    
  );


  }
  else
  {

    delayMicroseconds(2);
    T2 = ICR1;
    activeMeas = 0;
    Serial.print(T);
    Serial.print("_");
    Serial.print(T2);
    Serial.print("_");
    Serial.println("0");
    
    //Serial.println(T1OVF_Counter);
    


  }

  asm volatile (
    "sei \n\t");
}
 
void setup()
{
  TCCR1A = 0;           // Init Timer1A
  TCCR1B = 0;           // Init Timer1B
  TCCR1B = 0b01000001;  // Internal Clock, Prescaler = 1, ICU Filter OFF, ICU Pin RISING
  TIMSK1 |= B00100001;  // Enable Timer OVF & CAPT Interrupts
  Serial.begin(9600);

}
 
void loop()
{

}