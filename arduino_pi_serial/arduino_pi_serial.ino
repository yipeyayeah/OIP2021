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
        break;
      case 2:
        sendMessage("[Arduino] Inside Case 2. Executing Case 2.");
        break;
      case 3:
        sendMessage("[Arduino] Inside Case 3. Executing Case 3.");
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
