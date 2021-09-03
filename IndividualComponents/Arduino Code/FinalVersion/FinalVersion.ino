#include <Stepper.h>
#define Water_Sensor_Min 0
#define Water_Sensor_Max 521

const int Switch1 = 53;
const int LED_green = 51;
const int LED_orange = 49;
const int FAN = 47;
const int RGB_red = 45;
const int RGB_blue = 43;  // LED_ULTRASONIC
const int RGB_green = 41; // LED_VALVE
const int Water_Sensor_Power = 52;
const int Water_Sensor_Signal = A1;

int value;
boolean ButtonValue;
volatile byte CleaningMode = LOW;

//Stepper Motor Define
const int stepsPerRevolution = 2048; //number of steps per revolution
Stepper Stepper1 = Stepper(stepsPerRevolution, 24, 26, 25, 27);


void setup() {
  Serial.begin(9600);

  //IO Configurations
  pinMode(Switch1, INPUT);
  pinMode(LED_green, OUTPUT);
  pinMode(LED_orange, OUTPUT);
  pinMode(Water_Sensor_Power, OUTPUT);
  pinMode(FAN, OUTPUT);
  pinMode(RGB_red, OUTPUT);
  pinMode(RGB_blue, OUTPUT);
  pinMode(RGB_green, OUTPUT);
  pinMode(Water_Sensor_Signal, INPUT);

  //Stepper Motor setup()
  Stepper1.setSpeed(15);  //set the speed to 5 rpm
}

void loop() {
  int start = 0;
  digitalWrite(LED_green, HIGH); //turn on green LED (Idle Mode)
  digitalWrite(LED_orange, LOW); //turn off red LED
  digitalWrite(RGB_green, HIGH); //turn off water valves
  Serial.println("send 1 to start");
  while(Serial.available() <=0){
  }
  start = Serial.read();
  sendMessage("4");
  if(start == 1){
    CleaningMode = HIGH;
  }
  while(CleaningMode = HIGH){
    digitalWrite(LED_green, LOW); //turn off Green LED
    digitalWrite(LED_orange, HIGH); //turn on Orange LED (Cleaning Mode)
    while(Serial.available() <= 0) {
    }
      int command = Serial.read() - '0';
      Serial.print("[Arduino] Value received: ");
      Serial.println(command);

      switch (command) {
        case 1:
          sendMessage("[Arduino] Inside Case 1. Executing Cleaning Cycle.");
          CleaningProcess();
          sendMessage("4");
          break;
        
        case 2:
          sendMessage("[Arduino] Inside Case 2. Executing Drying Cycle.");
          DryingProcess();
          sendMessage("4");
          break;
          
        case 3:
          sendMessage("[Arduino] Inside Case 3. Executing Sterilization Cycle.");
          SterilizationProcess();
          sendMessage("4");
          break;
          
        case 5:
          sendMessage("[Arduino] Inside Case 5. Executing Check Syringe Cycle.");
          CheckSyringe();
          sendMessage("4");CheckSyringe();
          break;
          
        case 6:
          sendMessage("[Arduino] Inside Case 6. Executing Fill Tank Cycle.");
          FillTank();
          sendMessage("4");
          break;
          
        case 7:
          sendMessage("[Arduino] Inside Case 7. Executing Drain Tank Cycle.");
          DrainTank();
          sendMessage("4");
          break; 

        case 8:
          sendMessage("[Arduino] Inside Case 8. End Cleaning Mode");
          CleaningMode = LOW;
          sendMessage("4");
          break;
          
        default: 
          break;
      
    }
  }
}

void sendMessage(String m){
  Serial.println(m);
  delay(1000);
}

void FillTank(){
  digitalWrite(RGB_green, LOW);          //OPEN SOLENOID VALVE 1
  value = 0;
  while(value < 500){
    digitalWrite(Water_Sensor_Power, HIGH);
    delay(1000);
    value = analogRead(Water_Sensor_Signal);
    Serial.println(value);
    digitalWrite(Water_Sensor_Power, LOW);
 }
 digitalWrite(RGB_green, HIGH);    //CLOSE SOLENOID VALVE 1
}

void CleaningProcess(){
   Stepper1.step(2048);
   delay(1000);
   digitalWrite(RGB_blue, HIGH);    //Ultrasonic cleaner ON
   for (int i = 5; i >= 0; --i){
   delay(600);
   }
   digitalWrite(RGB_blue, LOW);
   delay(1000);
   DrainTank();
   delay(1000);
   FillTank();
   for(int i = 0; i <=5 ; i++){
    Stepper1.step(-200); //Clockwise
    delay(100);
    Stepper1.step(200);  //Anti-Clockwise
    delay(100);
   }
   delay(1000);
   Stepper1.step(-2048);
   delay(1000);
}

void DrainTank(){
  digitalWrite(RGB_green, LOW);          //OPEN SOLENOID VALVE 2
  value = 500;
  while(value >= 10){
    digitalWrite(Water_Sensor_Power, HIGH);
    delay(1000);
    value = analogRead(Water_Sensor_Signal);
    Serial.println(value);
    digitalWrite(Water_Sensor_Power, LOW);
     }
 digitalWrite(RGB_green, HIGH);    //CLOSE SOLENOID VALVE 2
}

void DryingProcess(){
  int count = 0;
  while(count < 5){
    Stepper1.step(100); //Clockwise
    delay(100);
    Stepper1.step(-100);  //Anti-Clockwise
    delay(100);
    count++;
  }
  delay(1000);
  digitalWrite(FAN, HIGH);
  for (int i = 5; i >= 0; --i){
    delay(600);
  }
  digitalWrite(FAN, LOW);
}

void SterilizationProcess(){
  //UV LIGHT ON
  digitalWrite(RGB_red, HIGH);
  digitalWrite(RGB_blue ,HIGH);
  //
  for (int i = 5; i >= 0; --i){
    delay(600);
  }
  //UV LIGHT OFF
  digitalWrite(RGB_red, LOW);
  digitalWrite(RGB_blue, LOW);
  //
}

void CheckSyringe(){
  delay(1000);
  Stepper1.step(341);
  delay(1000);
}
