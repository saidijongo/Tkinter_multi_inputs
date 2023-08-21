const int CW_PIN = 5;
const int CCW_PIN = 7;
int motorPosition = 0;
boolean motorDirection = true; // true for CW, false for CCW

void setup() {
  pinMode(CW_PIN, OUTPUT);
  pinMode(CCW_PIN, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  // Check for incoming serial data
  if (Serial.available() > 0) {
    char command = Serial.read();

    if (command == 'S') {
      sendStatus();
    } else if (command == 'R') {
      resetMotor();
    } else if (command == 'CW') {
      rotateCW90();
    } else if (command == 'CCW') {
      rotateCCW90();
    }
  }

  // Simulate motor rotation (replace with actual motor control code)
  if (motorDirection) {
    digitalWrite(CW_PIN, HIGH);
    digitalWrite(CCW_PIN, LOW);
  } else {
    digitalWrite(CW_PIN, LOW);
    digitalWrite(CCW_PIN, HIGH);
  }

  delay(10); // Simulated motor rotation delay

  // Update motor position (replace with actual position tracking)
  motorPosition += motorDirection ? 1 : -1;
  if (motorPosition >= 360) {
    motorPosition = 0;
  }
}

void sendStatus() {
  Serial.print("Angle:");
  Serial.print(motorPosition);
  Serial.print(",Direction:");
  Serial.println(motorDirection ? "CW" : "CCW");
}

void resetMotor() {
  motorPosition = 0;
  motorDirection = true;
  digitalWrite(CW_PIN, HIGH);
  digitalWrite(CCW_PIN, LOW);
  Serial.println("Done");
}

void rotateCW90() {
  motorDirection = true;
  delay(9000); // Simulated motor rotation time for 90 degrees
  Serial.println("Done");
}

void rotateCCW90() {
  motorDirection = false;
  delay(9000); // Simulated motor rotation time for 90 degrees
  Serial.println("Done");
}
