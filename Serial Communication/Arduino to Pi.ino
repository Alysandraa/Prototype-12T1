int a =0; 

void setup() {
Serial.begin(9600);              //Starting serial communication
}
  
void loop() {
  //a++;                          // convert a value to hexa 
  Serial.println("Hello");   // send the data
  delay(1000);                  // give the loop some break
}
