//H-bridge pins
const int EnA = 10;
const int In1 = 9;
const int In2 = 8;
const int In3 = 7;
const int In4 = 6;
const int EnB = 5;

//variables
float positionData;
float position;

void setup() {
  Serial.begin(9600);

  //set all pins relating to motors as outputs
  pinMode(EnA, OUTPUT);
  pinMode(In1, OUTPUT);
  pinMode(In2, OUTPUT);
  pinMode(In3, OUTPUT);
  pinMode(In4, OUTPUT);
  pinMode(EnB, OUTPUT);
  
}

void loop() {
  //Write both motors high as a baseline
   analogWrite(EnA,255);
   analogWrite(EnB,255);
  //forwards();
   if(Serial.available()){
     positionData = (Serial.parseInt());
     //converts the number from a scale of 100-200 to a scale of -1 to 1
     position = (((float(positionData))-(float(100))) / (float(100)));
   }
   //Serial.println(position);
   direction();
}

void forwards(){   //go forwards
    digitalWrite(In1, LOW);
    digitalWrite(In2, HIGH);
    digitalWrite(In3, LOW);
    digitalWrite(In4, HIGH);
}

void backwards(){  //go backwards
    digitalWrite(In1, HIGH);
    digitalWrite(In2, LOW);
    digitalWrite(In3, HIGH);
    digitalWrite(In4, LOW);
}

void direction(){
  if (position < 0){
    //Serial.println(position);
    //converts the number to a motor speed
    float speedR = (((float(1))+position)*(float(255)));
    analogWrite(EnA, 255);
    //writes that speed to the right motor to turn left to the appropriate degree
    analogWrite(EnB, (speedR));
    Serial.println(speedR);
    forwards(); //runs motors
  }else{
    //converts the number to a motor speed
    float speedL = (((float(1))-position)*(float(255)));
    //writes that speed to the right motor to turn left to the appropriate degree
    analogWrite(EnA, (speedL));
    analogWrite(EnB, 255);
    Serial.println(speedL);
    forwards();  //runs motors
  }
  //Serial.println(position);
}
