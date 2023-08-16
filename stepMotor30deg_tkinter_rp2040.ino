#define CW 5  // CW+ connected
#define CCW 6 // CCW+ connected

int steps_per_rotation = 360; // Number of steps for one full rotation (360 degrees)
int steps_per_30_deg = steps_per_rotation / 12; // Number of steps for 30 degrees
int current_angle = 0; // Current angle of the motor
int current_direction = 0; // 0 for stopped, 1 for CW, -1 for CCW

void CW_n(int n) {
  for (int i = 0; i < n; i++) {
    digitalWrite(CW, HIGH);
    delayMicroseconds(1000); 
    digitalWrite(CW, LOW);
    delayMicroseconds(1000);
    current_angle = (current_angle + 30) % 360;
    current_direction = 1;
  }
}

void CCW_n(int n) {
  for (int i = 0; i < n; i++) {
    digitalWrite(CCW, HIGH);
    delayMicroseconds(1000);
    digitalWrite(CCW, LOW);
    delayMicroseconds(1000);
    current_angle = (current_angle - 30 + 360) % 360;
    current_direction = -1;
  }
}

void stopMotor() {
  digitalWrite(CW, LOW);
  digitalWrite(CCW, LOW);
  current_direction = 0;
}

void setup() {
  pinMode(CW, OUTPUT);
  pinMode(CCW, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();

    if (command == "CW") {
      CW_n(steps_per_30_deg); // Rotate 30 degrees clockwise
    } else if (command == "CCW") {
      CCW_n(steps_per_30_deg); // Rotate 30 degrees counterclockwise
    } else if (command == "STOP") {
      stopMotor();
    } else if (command == "GET_STATUS") {
      Serial.print("Current Angle: ");
      Serial.print(current_angle);
      Serial.print(", Direction: ");
      if (current_direction == 0) {
        Serial.println("Stopped");
      } else if (current_direction == 1) {
        Serial.println("CW");
      } else {
        Serial.println("CCW");
      }
    } else {
      // do nothing
    }
  }
}
