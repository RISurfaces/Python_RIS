// RIS on drone simulation steering.

#include <Arduino.h>

// defines pins numbers
#define stepPin 9
#define dirPin 8
#define stycznik_1 10
#define stycznik_2 11

bool dir = true;

void setup()
{
  // Sets the two pins as Outputs
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
  pinMode(stycznik_1, INPUT_PULLUP);
  pinMode(stycznik_2, INPUT_PULLUP);
  Serial.begin(9600);
}

void rotateCW()
{
  digitalWrite(dirPin, LOW);
  digitalWrite(stepPin, HIGH);
  delayMicroseconds(1000);
  digitalWrite(stepPin, LOW);
  delayMicroseconds(1000);
}
void rotateCCW()
{
  digitalWrite(dirPin, HIGH);
  digitalWrite(stepPin, HIGH);
  delayMicroseconds(1000);
  digitalWrite(stepPin, LOW);
  delayMicroseconds(1000);
}

void rotate(bool dir)
{
  if (dir == true)
  {
    digitalWrite(dirPin, HIGH);
  }
  else
  {
    digitalWrite(dirPin, LOW);
  }
  digitalWrite(stepPin, HIGH);
  delayMicroseconds(1000);
  digitalWrite(stepPin, LOW);
  delayMicroseconds(1000);
}
void stop()
{
  digitalWrite(stepPin, LOW);
}

void loop()
{
  if (digitalRead(stycznik_1) == LOW)
  {
    Serial.println(1);
    delay(1000);
    stop();
    dir = true;
  }
  else if (digitalRead(stycznik_2) == LOW)
  {
    Serial.println(2);
    delay(1000);
    stop();
    dir = false;
  }
  rotate(dir);
}
