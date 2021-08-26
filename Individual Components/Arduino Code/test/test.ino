void setup() {
   Serial.begin(9600);

}

void loop() {
  if (Serial.available() > 0) {
    int command = Serial.read() - '0';
    Serial.print("[Arduino] Value received: ");
    Serial.println(command);

    switch (command) {
      case 1:
        sendMessage("[Arduino] Inside Case 1. Executing Case 1.");    
        sendMessage("4");
        break;
      case 2:
        sendMessage("[Arduino] Inside Case 2. Executing Case 2.");
        sendMessage("4");
        break;
      case 3:
        sendMessage("[Arduino] Inside Case 3. Executing Case 3.");
        sendMessage("4");
        break;
      case 5:
        sendMessage("[Arduino] Inside Case 5. Executing Case 5.");
        sendMessage("4");
        break;
      case 6:
        sendMessage("[Arduino] Inside Case 6. Executing Case 6.");
        sendMessage("4");
        break;
      case 7:
        sendMessage("[Arduino] Inside Case 7. Executing Case 7.");
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
