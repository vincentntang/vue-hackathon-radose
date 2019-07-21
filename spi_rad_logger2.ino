 
#include <SPI.h>
#define LOG_PERIOD 10000  //Logging period in milliseconds, recommended value 15000-60000.
#define MAX_PERIOD 60000  //Maximum logging period 
#define conversion_factor 0.00812 // converting counts to uSV/h
#define max_readings 6

int counts = 0;     //variable for GM Tube events
int cpm = 0;        //variable for CPM
int multiplier = 0;  //variable for calculation CPM in this sketch
unsigned long previousMillis = 0;  //variable for time measurement
float radiation = 0.0;

int counts_array[max_readings];
int index = 0;
int total = 0;
int average = 0;
int tube = 2; // pin the tube is connected to the arduino

void tube_impulse(){       //subprocedure for capturing events from Geiger Kit
  counts++;

}

void setup(){             //setup subprocedure
  pinMode(tube,INPUT);
  //digitalWrite(tube,HIGH);
  multiplier = MAX_PERIOD / LOG_PERIOD;      //calculating multiplier, depend on your log period
  Serial.begin(9600);
  for (int current_reading = 0; current_reading < max_readings; current_reading++){
      counts_array[current_reading] = 0;
    }
    
  attachInterrupt(0, tube_impulse, FALLING); //define external interrupts 
  //Serial.println("Start counter");
}

void loop(){                                 //main cycle
  unsigned long currentMillis = millis();
  if(currentMillis - previousMillis > LOG_PERIOD){
    cpm = counts * multiplier ;
    
    total = total - counts_array[index];
    counts_array[index] = cpm;
    total = total + counts_array[index];
    index = index + 1;
    
    if (index >= max_readings){
        index = 0;
      }
      
    average = total / max_readings;
    radiation = average * conversion_factor;
    
    //Serial.println(average,DEC);
    //Serial.print("    CPM     ");
    Serial.println(radiation,4);
    //Serial.println("   uSv/hr");
    
    previousMillis = currentMillis;
    counts = 0;  
  }  
}
