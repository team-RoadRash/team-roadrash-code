#include <SoftwareSerial.h>
SoftwareSerial Bluetooth(A3,A2);
struct vals{
  int xval;
  int yval;
  int stop_signal;

};

vals VR;


int VRx = A0;
int VRy = A1;
int stop_signal = SDA;

int xPosition = 0;
int yPosition = 0;
int SW_state = 0;
int mapX = 0;
int mapY = 0;
int mapX1 = 0;
int mapY1 = 0;
int mapX2 = 0;
int mapY2 = 0;


// BLUETOOTH RATE IS 38400

// VRx and VRy are the analog pins connected to the joystick
// xPosition and yPosition are the values read from the joystick

void setup() {
  Serial.begin(9600);
  Bluetooth.begin(38400);
  pinMode(VRx, INPUT);
  pinMode(VRy, INPUT);
  pinMode(stop_signal, INPUT);
  // pinMode(13, OUTPUT);
}

void loop() {
  xPosition = analogRead(VRx);
  yPosition = analogRead(VRy);
  // read the stop signal from the pin D4
    SW_state = digitalRead(stop_signal);
mapX = map(xPosition, 0, 1023, -100,100);
mapY = map(yPosition, 0, 1023, -100, 100);

// x,y = 756, 771
// mapX1 = map(xPosition, 0, 756, -100,0);
// mapY1 = map(yPosition, 0, 770, -100, 0);

// mapX2 = map(xPosition, 756, 1023, 0,100);
// mapY2 = map(yPosition, 770, 1023, 0,100);

// // mapX must be mapped to mapX1 and mapX2
// // mapY must be mapped to mapY1 and mapY2
// if (xPosition < 756) {
//     mapX = mapX1;
//     }
//     else {
//       mapX = mapX2;
//     }
//     if (yPosition < 770) {
//       mapY = mapY1;
//     }
//     else {
//       mapY = mapY2;
//     }
  
  VR.xval = mapX;
  VR.yval = mapY;
    VR.stop_signal = SW_state;

 
      // STORE mapX and mapY in a struct and send it to the bluetooth module
    Bluetooth.write((byte*)&VR, sizeof(VR));
    // print the values to the serial monitor
    Serial.print("\n X: ");
    Serial.print(mapX);
    Serial.print(" Y: ");
    Serial.println(mapY);
    Serial.print("SW: ");
    Serial.println(SW_state);
    
  // Bluetooth.write(VR.xval);
  // Serial.println(VR.xval);
  delay(100);
}
