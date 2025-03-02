#include <Encoder.h>

// -------------------------------
// DRV8833 Input Pin Assignments
// -------------------------------
// Board #1: Motors 1 & 2
#define M1_IN1 4   // Motor 1, AIN1
#define M1_IN2 5   // Motor 1, AIN2
#define M2_IN1 6   // Motor 2, BIN1
#define M2_IN2 7   // Motor 2, BIN2

// Board #2: Motors 3 & 4
#define M3_IN1 8   // Motor 3, AIN1
#define M3_IN2 9   // Motor 3, AIN2
#define M4_IN1 10  // Motor 4, BIN1
#define M4_IN2 11  // Motor 4, BIN2

// Group them for easier indexing:
const int motorPins[4][2] = {
  {M1_IN1, M1_IN2}, // Motor 1
  {M2_IN1, M2_IN2}, // Motor 2
  {M3_IN1, M3_IN2}, // Motor 3
  {M4_IN1, M4_IN2}  // Motor 4
};

// -------------------------------
// Encoder Pin Assignments
// -------------------------------
Encoder encoder1(21, 23);  // Motor 1
Encoder encoder2(20, 22);  // Motor 2
Encoder encoder3(18, 19);  // Motor 3
Encoder encoder4(2, 3);    // Motor 4

// We'll store each motor's speed in an array: -255..255
int motorSpeeds[4] = {0, 0, 0, 0};

// For reading serial commands
String inputString = "";
bool stringComplete = false;

// -------------------------------
// Setup
// -------------------------------
void setup() {
  Serial.begin(115200);

  // Initialize motor driver pins
  for (int i = 0; i < 4; i++) {
    pinMode(motorPins[i][0], OUTPUT);
    pinMode(motorPins[i][1], OUTPUT);
    // Start each motor at 0 speed
    setMotorSpeed(i, 0);
  }

  // Reserve space for incoming serial data
  inputString.reserve(100);
}

// -------------------------------
// Main Loop
// -------------------------------
void loop() {
  // Check if we've received a full command via serial
  if (stringComplete) {
    parseMotorCommands(inputString);
    inputString = "";
    stringComplete = false;
  }

  // Update each motor speed
  for (int i = 0; i < 4; i++) {
    setMotorSpeed(i, motorSpeeds[i]);
  }

  // Print encoder values periodically for debugging
  static unsigned long lastPrint = 0;
  if (millis() - lastPrint > 1000) {
    long enc1 = encoder1.read();
    long enc2 = encoder2.read();
    long enc3 = encoder3.read();
    long enc4 = encoder4.read();

//    Serial.print("Encoders: ");
    Serial.print("<");
    Serial.print(enc1); Serial.print(", ");
    Serial.print(enc2); Serial.print(", ");
    Serial.print(enc3); Serial.print(", ");
    Serial.print(enc4); Serial.print(">\n");

    lastPrint = millis();
  }
}

// -------------------------------
// Serial Event
// -------------------------------
void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    if (inChar == '\n') {
      stringComplete = true;
    } else {
      inputString += inChar;
    }
  }
}

// -------------------------------
// Parse Motor Commands
// -------------------------------
// Expects a string like: "<speed1,speed2,speed3,speed4>"
// e.g. "(100,100,100,100)"
void parseMotorCommands(String command) {
  command.trim();
  if (command.startsWith("(") && command.endsWith(")")) {
    String data = command.substring(1, command.length() - 1); // remove ( and )
    int lastIndex = 0;

    for (int i = 0; i < 4; i++) {
      int index = data.indexOf(',', lastIndex);
      String value;

      if (index == -1 && i == 3) {
        // Last value
        value = data.substring(lastIndex);
      } else if (index != -1) {
        value = data.substring(lastIndex, index);
        lastIndex = index + 1;
      } else {
        // Malformed command
        return;
      }      

      motorSpeeds[i] = value.toInt();
      motorSpeeds[i] = constrain(motorSpeeds[i], -255, 255);
    }
  }
}

// -------------------------------
// Set Motor Speed for DRV8833
// -------------------------------
// motorIndex: 0..3
// speed: -255..255  (negative -> reverse)
void setMotorSpeed(int motorIndex, int speed) {
  int in1 = motorPins[motorIndex][0];
  int in2 = motorPins[motorIndex][1];

  // Sign-magnitude control:
  // Forward:  IN1 = PWM,   IN2 = LOW
  // Reverse:  IN1 = LOW,   IN2 = PWM
  // Speed magnitude = PWM duty cycle (0..255)
  int pwmVal = abs(speed);
  if (pwmVal > 255) pwmVal = 255;

  if (speed >= 0) {
    // Forward
    analogWrite(in1, pwmVal);
    digitalWrite(in2, LOW);
  } else {
    // Reverse
    digitalWrite(in1, LOW);
    analogWrite(in2, pwmVal);
  }
}
