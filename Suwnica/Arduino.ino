#define ENCODER_A1 2
#define ENCODER_B1 3
#define ENCODER_A2 4
#define ENCODER_B2 5
#define MOTOR_PWM1 9
#define MOTOR_DIR1 8
#define MOTOR_PWM2 10
#define MOTOR_DIR2 7

volatile long encoderCount1 = 0;
volatile long encoderCount2 = 0;
long maxPulses = 1000;

void encoder1ISR() {
    encoderCount1++;
}

void encoder2ISR() {
    encoderCount2++;
}

void setup() {
    pinMode(ENCODER_A1, INPUT);
    pinMode(ENCODER_B1, INPUT);
    pinMode(ENCODER_A2, INPUT);
    pinMode(ENCODER_B2, INPUT);
    
    pinMode(MOTOR_PWM1, OUTPUT);
    pinMode(MOTOR_DIR1, OUTPUT);
    pinMode(MOTOR_PWM2, OUTPUT);
    pinMode(MOTOR_DIR2, OUTPUT);
    
    attachInterrupt(digitalPinToInterrupt(ENCODER_A1), encoder1ISR, RISING);
    attachInterrupt(digitalPinToInterrupt(ENCODER_A2), encoder2ISR, RISING);
    
    Serial.begin(9600);
}

void moveMotor(int pwmPin, int dirPin, int speed, bool direction) {
    digitalWrite(dirPin, direction);
    analogWrite(pwmPin, speed);
}

void stopMotors() {
    analogWrite(MOTOR_PWM1, 0);
    analogWrite(MOTOR_PWM2, 0);
}

void loop() {
    if (Serial.available() > 0) {
        long pulses, speed;
        Serial.readStringUntil('\n').trim().toInt();
        pulses = Serial.parseInt();
        speed = Serial.parseInt();
        
        pulses = min(pulses, maxPulses);
        speed = constrain(speed, 0, 255);
        
        encoderCount1 = 0;
        encoderCount2 = 0;
        
        moveMotor(MOTOR_PWM1, MOTOR_DIR1, speed, HIGH);
        moveMotor(MOTOR_PWM2, MOTOR_DIR2, speed, HIGH);
        
        while (encoderCount1 < pulses && encoderCount2 < pulses) {
            delay(1);
        }
        
        stopMotors();
        delay(500);
        
        moveMotor(MOTOR_PWM1, MOTOR_DIR1, speed, LOW);
        moveMotor(MOTOR_PWM2, MOTOR_DIR2, speed, LOW);
        
        while (encoderCount1 > 0 || encoderCount2 > 0) {
            delay(1);
        }
        
        stopMotors();
        Serial.println("done");
    }
}
