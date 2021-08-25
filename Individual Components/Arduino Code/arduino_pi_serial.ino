#include <Stepper.h>
#define DHT11_PIN 9
#define Water_Sensor_Min 0
#define Water_Sensor_Max 521

const int Switch1 = 53;
const int LED_green = 51;
const int LED_red = 49;
const int FAN = 47;
const int LED_uv = 45;
const int Water_Sensor_Power = 52;
const int Water_Sensor_Signal = A0;


int value;
boolean ButtonValue;
volatile byte CleaningMode = LOW;

//Stepper Motor Define
const int stepsPerRevolution = 2048; //number of steps per revolution
Stepper Stepper1 = Stepper(stepsPerRevolution, 24, 26, 25, 27);

void setup() {
  Serial.begin(9600);
  pinMode(Switch1, INPUT);
  pinMode(LED_green, OUTPUT);
  pinMode(LED_red, OUTPUT);
  pinMode(Water_Sensor_Power, OUTPUT);
  pinMode(FAN, OUTPUT);
  pinMode(LED_uv, OUTPUT);
  digitalWrite(Water_Sensor_Power, LOW); //turn the sensor off
  Stepper1.setSpeed(15);  //set the speed to 15 rpm
}

void loop() {
  if (Serial.available() > 0) {
    int command = Serial.read() - '0';
    Serial.print("[Arduino] Value received: ");
    Serial.println(command);

    switch (command) {
      case 1:
        sendMessage("[Arduino] Inside Case 1. Executing Case 1.");    
        CleaningProcess();
        sendMessage("4");
        break;
      case 2:
        sendMessage("[Arduino] Inside Case 2. Executing Case 2.");
        DryingProcess();
        sendMessage("4");
        break;
      case 3:
        sendMessage("[Arduino] Inside Case 3. Executing Case 3.");
        SterilizationProcess();
        sendMessage("4");
        break;
      case 5:
        sendMessage("[Arduino] Inside Case 5. Executing Case 5.");
        sendMessage("4");
        break;
      case 6:
        sendMessage("[Arduino] Inside Case 6. Executing Case 6.");
        FillTank();
        sendMessage("4");
        break;
      case 7:
        sendMessage("[Arduino] Inside Case 7. Executing Case 7.");
        DrainTank();
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

void CleaningProcess(){
    Stepper1.step(2048); //move syringe into tank
    delay(1000);
    digitalWrite(LED_uv, HIGH); //ultrasonic cleaner
    delay(1000);
    digitalWrite(LED_uv, LOW);
    delay(1000);
    Stepper1.step(-2048);
    delay(1000);
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
  digitalWrite(FAN, HIGH);
  for (int i = 5; i >= 0; --i){
    delay(500);
  }
  digitalWrite(FAN, LOW);
}

void SterilizationProcess(){
  digitalWrite(LED_uv, HIGH);
  delay(1000);
  digitalWrite(LED_uv, LOW);
}

void DrainTank(){
  digitalWrite(LED_uv, HIGH); //ultrasonic cleaner
  delay(1000);
  digitalWrite(LED_uv, LOW);
  delay(1000);
}

void FillTank(){
  digitalWrite(LED_uv, HIGH); //ultrasonic cleaner
  delay(1000);
  digitalWrite(LED_uv, LOW);
  delay(1000);
}
