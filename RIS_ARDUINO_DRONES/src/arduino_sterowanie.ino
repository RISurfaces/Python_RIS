#include <Arduino.h>

#define stepPin 9
#define dirPin 8
#define stycznik_sciana 10
#define stycznik_okno 11

int speed = 0;
bool dir = false;
bool running = false;
bool paused = false;
bool initialized = false;
String serialBuffer = "";

void setup()
{
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
  pinMode(stycznik_okno, INPUT_PULLUP);
  pinMode(stycznik_sciana, INPUT_PULLUP);
  Serial.begin(9600);

  // Inicjalny powrót do pozycji startowej (okno)
  dir = false;
  digitalWrite(dirPin, LOW);
  analogWrite(stepPin, 100);
  running = true;
}

void rotate(bool dir)
{
  digitalWrite(dirPin, dir ? HIGH : LOW);
  analogWrite(stepPin, speed);
  running = true;
  paused = false;
}

void stop()
{
  analogWrite(stepPin, 0);
  running = false;
}

void handleSerial()
{
  while (Serial.available() > 0)
  {
    char c = Serial.read();
    if (c == '\n' || c == '\r')
    {
      if (serialBuffer.length() > 0)
      {
        serialBuffer.trim();

        if (serialBuffer == "reset")
        {
          stop();
          dir = false;
          digitalWrite(dirPin, LOW);
          analogWrite(stepPin, 100);
          running = true;
          paused = false;
          initialized = false;
        }
        else if (serialBuffer == "stop")
        {
          stop();
          paused = true;
        }
        else if (serialBuffer == "start")
        {
          if (paused && speed > 0)
          {
            rotate(dir);
          }
        }
        else
        {
          // Interpretuj jako nową prędkość
          int newSpeed = serialBuffer.toInt();
          if (newSpeed > 0 && newSpeed <= 255)
          {
            speed = newSpeed;
            dir = true; // w kierunku ściany
            rotate(dir);
            initialized = true;
          }
        }

        serialBuffer = "";
      }
    }
    else
    {
      serialBuffer += c;
    }
  }
}

void loop()
{
  handleSerial();

  if (running && !paused)
  {
    // Detekcja końców pozycji
    if (digitalRead(stycznik_sciana) == LOW && dir)
    {
      stop();
      Serial.println("end");
      delay(500);
      dir = false;
      rotate(dir); // Powrót do okna
    }
    else if (digitalRead(stycznik_okno) == LOW && !dir)
    {
      stop();
      delay(500);
      Serial.println("Done");

      if (!initialized)
      {
        // Zatrzymaj po powrocie na starcie
        running = false;
      }
    }
  }
}
