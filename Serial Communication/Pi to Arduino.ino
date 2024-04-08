void setup(){
  // Starting serial communication
  Serial.begin(9600);
}
 
void loop(){
  if(Serial.available() > 0) {
     //sets a parameter for when to stop reading the string
    int data = Serial.readStringUntil('\n');
    Serial.print("Hi Raspberry Pi! You sent me: ");
    Serial.println(data);
  }
}
