#include <Arduino.h>

int dir1v = A2;
int dir2v = A0;
int pwm1v = A3;
int pwm2v = A1;

void setup() {
    Serial.begin(115200);  // Match baud rate with ROS 2
    Serial.println("Arduino Ready to receive motor speeds");

    pinMode(dir1v, OUTPUT);
    pinMode(dir2v, OUTPUT);
    pinMode(pwm1v, OUTPUT);
    pinMode(pwm2v, OUTPUT);
}

void loop() {
    if (Serial.available() > 0) {
        String data = Serial.readStringUntil('\n');  // Read full line
        data.trim();  // Remove trailing newlines and spaces
        Serial.print("Raw Data Received: ");
        Serial.println(data);

        // Variables to store parsed values
        float dir1, dir2, pwm1, pwm2;

        // Ensure correct parsing
        int parsed = sscanf(data.c_str(), "%f,%f,%f,%f", &dir1, &dir2, &pwm1, &pwm2);

        // Debugging output
        Serial.print("Parsed Values: ");
        Serial.print(dir1); Serial.print(", ");
        Serial.print(dir2); Serial.print(", ");
        Serial.print(pwm1); Serial.print(", ");
        Serial.println(pwm2);

        if (parsed == 4) {  // Ensure parsing was successful
            // Convert to integers for digitalWrite
            digitalWrite(dir1v, (int)dir1);
            digitalWrite(dir2v, (int)dir2);

            // Convert floating PWM values (0 to 1) to PWM range (0-255)
            int pwm1_mapped = constrain(pwm1 * 255, 0, 255);
            int pwm2_mapped = constrain(pwm2 * 255, 0, 255);

            analogWrite(pwm1v, pwm1_mapped);
            analogWrite(pwm2v, pwm2_mapped);

        } else {
            Serial.println("⚠ Error: Failed to parse motor speeds");
        }
    }
}
