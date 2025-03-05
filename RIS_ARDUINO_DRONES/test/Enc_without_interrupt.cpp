//    Stepper Motor using a Rotary Encoder

#include<Arduino.h>

// defines pins numbers
 #define stepPin 8 
 #define dirPin  9
 #define outputA 10
 #define outputB 11

 int counter = 0;
 int angle = 0; 
 int aState;
 int aLastState;  
 
void setup() {
  // Sets the two pins as Outputs
  pinMode(stepPin,OUTPUT); 
  pinMode(dirPin,OUTPUT);
  pinMode (outputA,INPUT);
  pinMode (outputB,INPUT);
  aLastState = digitalRead(outputA);
  Serial.begin(9600);


}

void rotateCW() {
  digitalWrite(dirPin,LOW);
    digitalWrite(stepPin,HIGH);
    delayMicroseconds(1000);
    digitalWrite(stepPin,LOW);
    delayMicroseconds(1000); 
}
void rotateCCW() {
  digitalWrite(dirPin,HIGH);
    digitalWrite(stepPin,HIGH);
    delayMicroseconds(1000);
    digitalWrite(stepPin,LOW);
    delayMicroseconds(1000);   
}

void loop() {
  aState = digitalRead(outputA);
  if (aState != aLastState){     
     if (digitalRead(outputB) != aState) { 
       Serial.println(counter);
       counter ++;
       //Serial.println(angle);
       angle ++;
       //rotateCW();  
     }
     else {
      Serial.println(counter);
      counter--;
      angle --;
      //rotateCCW(); 
     }
     //Serial.println("Position: ");
     //Serial.println(int(angle*(-1.8)));
     //Serial.println("deg\n"); 
   }
  aLastState = aState;
}

