#include <SoftwareSerial.h>

SoftwareSerial mySerial(0, 1); // RX, TX

struct VR {
  int xval;
  int yval;
  int stop_signal;
};

VR vr;
int x, y;
int x_p;
int x_n;
int y_p;
int y_n;

void setup() {
  Serial.begin(9600);
  mySerial.begin(38400);
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
    pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);

}

void loop() {
  if (mySerial.available()) {
    mySerial.readBytes((char*)&vr, sizeof(vr));
    Serial.print("xval: ");
    Serial.print(vr.xval);
    Serial.print(" yval: ");
    Serial.println(vr.yval);
        Serial.print(" sw: ");
    Serial.println(vr.stop_signal);
// Convert xval, yval  and stop signals to analogWrite values
  x = vr.xval;
  y = vr.yval;

   if(x>95)
   {
     x_p = 1;
     x_n = 0;
   }

      if(x< 35)
   {
     x_n = 1;
     x_p = 0;
   }


      if(y>98)
   {
     y_p = 1;
     y_n = 0;
   }

      if(y <-70)
   {
     y_n = 1;
     y_p = 0;
   }

  if(x>35 && x < 95)
  {
    x_p = 0;
    x_n = 0;
  }

    if(y>-70 && y < 98)
  {
    y_p = 0;
    y_n = 0;
  }


// DIGITAL WRITE x_p, x_n, y_p, y_n, stop_signal
  digitalWrite(2, x_p);
  digitalWrite(3, x_n);
  digitalWrite(4, y_p);
  digitalWrite(5, y_n);
  digitalWrite(6, vr.stop_signal);

}

}

