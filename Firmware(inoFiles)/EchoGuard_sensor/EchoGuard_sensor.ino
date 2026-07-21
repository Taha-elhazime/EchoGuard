#include <Servo.h>

//customize the variables to match the sensor's position
int sens_X = 120;
int sens_Y = 70;

Servo Xservo;
Servo Yservo;
float k = 0.015;
float a = 3;
float Xangle = 90;
float Yangle = 90;
bool tracking = false;
int direction = 1;
unsigned long lostTime = 0;
int state = 2;
int idleCounter = 0;
int dirX = 1;
int dirY = 1;

void setup() {
Serial.begin(115200);
Xservo.attach(8);
Xservo.write(Xangle);
Yservo.attach(9);
Yservo.write(Yangle);
delay(1000);
} 

void loop() {

if (Serial.available()){ 
String msg = Serial.readStringUntil('\n');

int firstComma = msg.indexOf(',');
int secondComma = msg.indexOf(',', firstComma + 1);
int thirdComma = msg.indexOf(',', secondComma +1);
int fourthComma = msg.indexOf(',', thirdComma + 1);

int dx = msg.substring(0, firstComma).toInt();
int dy = msg.substring(firstComma + 1, secondComma).toInt();

tracking = msg.substring(secondComma + 1).toInt();

int bearing = msg.substring(thirdComma + 1).toInt();
bool sensor = msg.sunstring(fourthComma + 1).toInt();

if(sensor){

Xangle = sens_X;
Yangle = sens_Y;
Xservo.write(Xangle);
Xservo.write(Yangle);
delay(5000);

}else if(tracking){
state = 0;
Xangle += dx * k;
Yangle += dy *k;

Xangle = constrain(Xangle, 0, 180);
Yangle = constrain(Yangle, 35, 180);

Xservo.write(Xangle);
Yservo.write(Yangle);
}else if(state == 0){
state = 1;
lostTime = millis();

Xangle = Xangle;
Yangle = Yangle;

Xangle += dx * a;
Yangle += dy * a;

Xangle = constrain(Xangle, 0, 180);
Yangle = constrain(Yangle, 35, 180);

Xservo.write(Xangle);
Yservo.write(Yangle);

}else if(state == 1){
 if(millis() - lostTime < 500){

float angleRad = radians(bearing-90);
float stepSize = 5;

Yangle -= sin(angleRad)*a;
Xangle += cos(angleRad)*a;

Xangle = constrain(Xangle, 0, 180);
Yangle = constrain(Yangle, 30, 180);

Xservo.write(Xangle);
Yservo.write(Yangle);
}else {
  state = 2;
}
} else if(state == 2){
  idleCounter++ ;
  if(idleCounter >= 8){
    idleCounter = 0;
    Xangle += dirX * 3;

    if(Xangle > 180){
      dirX = -1;
    }
    if(Xangle < 0) {
      dirX = 1;
  }

  Yangle += dirY * 3;
  if (Yangle >= 150){
    dirY = -1;
  }
  if(Yangle <= 35){
    dirY = 1;
  }


  
}

Xangle = constrain(Xangle, 0, 180);
Yangle = constrain(Yangle, 35, 180);

Xservo.write(Xangle);
Yservo.write(Yangle);

}

}
}