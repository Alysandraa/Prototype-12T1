void setup() {
Serial.begin(9600);              //Starting serial communication
}
  
void loop() {                      
  Serial.println("Hello");   // send data
  delay(1000);                  
}
