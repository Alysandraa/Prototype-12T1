//H-bridge pins
const int EnA = 10;
const int In1 = 9;
const int In2 = 8;
const int In3 = 7;
const int In4 = 6;
const int EnB = 5;


float positionData;
float position;

void setup() {
  Serial.begin(9600);
  
  pinMode(EnA, OUTPUT);
  pinMode(In1, OUTPUT);
  pinMode(In2, OUTPUT);
  pinMode(In3, OUTPUT);
  pinMode(In4, OUTPUT);
  pinMode(EnB, OUTPUT);
  
}

void loop() {
   analogWrite(EnA,255);
   analogWrite(EnB,255);
  //forwards();
   if(Serial.available()){
     positionData = (Serial.parseInt());
     position = (((float(positionData))-(float(100))) / (float(100)));
   }
   //Serial.println(position);
   direction();
}

void forwards(){
    digitalWrite(In1, LOW);
    digitalWrite(In2, HIGH);
    digitalWrite(In3, LOW);
    digitalWrite(In4, HIGH);
}

void backwards(){
    digitalWrite(In1, HIGH);
    digitalWrite(In2, LOW);
    digitalWrite(In3, HIGH);
    digitalWrite(In4, LOW);
}

void direction(){
  if (position < 0){
    //Serial.println(position);
    float speedL = (((float(1))+position)*(float(255)));
    analogWrite(EnA, 255);
    analogWrite(EnB, (speedL));
    Serial.println(speedL);
    forwards();
  }else{
    float speedR = (((float(1))-position)*(float(255)));
    analogWrite(EnA, (speedR));
    analogWrite(EnB, 255);
    Serial.println(speedR);
    forwards();
  }
  //Serial.println(position);
}
