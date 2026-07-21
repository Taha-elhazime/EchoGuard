#include <BluetoothSerial.h>
BluetoothSerial SerialBT;
#include <Ultrasonic.h>
int Dist = 0;
int Reset = 0;
bool sent = false;
bool Trig = false;
Ultrasonic ultrasonic(8, 9);

void setup() {
Serial.begin(9600);
pinMode(3, INPUT_PULLUP);

SerialBT.begin("EchoGuard");

while(!SerialBT.hasClient()){
  delay(100);
}

Serial.println("Connected");

}

void loop() {
if (sent == false){
long distance = ultrasonic.read();

if (digitalRead(3) == LOW){
  Reset = 1;
  delay(5000);
}

if(Reset == 1){
  distance = ultrasonic.read();
  delay(100);
  Dist = distance;
  Reset = 0;
}


if(Dist-distance > 10){
  Trig = true;
}

if(Trig){
  SerialBT.println("1");
  Trig = false;
  sent = true;

}

}
}