#include <Arduino.h>
// Definicja stanów
enum State
{
    IDLE,
    RUNNING
};

// dDefinicja pinów
#define stepPin 9
#define dirPin 8
#define stycznik_1 10
#define stycznik_2 11

State currentState = IDLE; // Początkowy stan
int repeatCount = 0;       // Ile razy ma być wykonana czynność
int currentIteration = 0;  // Która iteracja aktualnie
bool dir = true;

void setup()
{
    Serial.begin(9600);
    Serial.println("System gotowy. Komendy:");
    Serial.println("START <liczba_powtórzeń>  - np. START 5");
    Serial.println("STOP");
    Serial.println("RESET");
    // Sets the two pins as Outputs
    pinMode(stepPin, OUTPUT);
    pinMode(dirPin, OUTPUT);
    pinMode(stycznik_1, INPUT_PULLUP);
    pinMode(stycznik_2, INPUT_PULLUP);
    Serial.begin(9600);
}

void loop()
{
    // Odbieranie komendy z Serial
    if (Serial.available() > 0)
    {
        String command = Serial.readStringUntil('\n');
        command.trim(); // Usuń spacje i znaki nowej linii
        handleCommand(command);
    }

    // Obsługa stanu RUNNING
    if (currentState == RUNNING)
    {
        if (currentIteration < repeatCount)
        {
            Serial.print("Wykonywanie iteracji ");
            Serial.print(currentIteration + 1);
            Serial.print(" z ");
            Serial.println(repeatCount);

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
            currentIteration++;
        }
        else
        {
            Serial.println("Zakończono powtarzanie. Stan: IDLE.");
            currentState = IDLE;
        }
    }
}

void handleCommand(String command)
{
    if (command.startsWith("START"))
    {
        if (currentState == IDLE)
        {
            int spaceIndex = command.indexOf(' ');
            if (spaceIndex != -1 && spaceIndex < command.length() - 1)
            {
                String numberPart = command.substring(spaceIndex + 1);
                numberPart.trim();
                int value = numberPart.toInt();
                if (value > 0)
                {
                    repeatCount = value;
                    currentIteration = 0;
                    currentState = RUNNING;
                    Serial.print("Start: ");
                    Serial.print(repeatCount);
                    Serial.println(" powtórzeń.");
                }
                else
                {
                    Serial.println("Błąd: liczba powtórzeń musi być > 0.");
                }
            }
            else
            {
                Serial.println("Błąd: użyj formatu 'START <liczba>'.");
            }
        }
        else
        {
            Serial.println("Już w stanie RUNNING.");
        }
    }
    else if (command == "STOP")
    {
        currentState = IDLE;
        currentIteration = 0;
        Serial.println("Zatrzymano. Stan: IDLE.");
    }
    else if (command == "RESET")
    {
        currentState = IDLE;
        repeatCount = 0;
        currentIteration = 0;
        Serial.println("Reset. Stan: IDLE.");
    }
    else
    {
        Serial.print("Nieznana komenda: ");
        Serial.println(command);
    }
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
