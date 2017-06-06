#include "DHT11.h"
#include <Servo.h>
int pin=2;
int speakerpin = 10; //œºÇÇÄ¿°¡ ¿¬°áµÈ µðÁöÅÐÇÉ Œ³Á€
int door = 12;
String inputString = "";
boolean flag = HIGH;
int Sw_Pin=9;
int SW_state = 1;
int door_state = 0;
int emg=0;


Servo myservo;
DHT11 dht11(pin);        
 
void setup() {                
  Serial.begin(9600);
  pinMode(Sw_Pin, INPUT);
  pinMode(door, OUTPUT);   
  myservo.attach(11); 
  myservo.write(110); 
}
 
void loop() 
{
  int err;
  float temp, humi;
  String readString = ""; 
  if((err=dht11.read(humi, temp))==0)
  {
    Serial.print("temperature:");
    Serial.print(temp);
    Serial.print("  humidity:");
    Serial.print(humi);
    if(temp>=50)
    {
      tone(speakerpin,1000,1000);  //500: ÀœÀÇ ³ô³·ÀÌ(ÁÖÆÄŒö), 1000: ÀœÀÇ ÁöŒÓœÃ°£(1ÃÊ)
      delay(1000); 
      if (emg==0)
      {
      Serial.print("open\n");
      doorOpen();
      emg=1;
      delay(1000);
      myservo.write(30);
      }
    }
    Serial.println();
  }
  delay(100);
   
  while(Serial.available())
  {
    if(Serial.available() > 0)
    {
      char c = Serial.read();
      readString += c;
    }
  }
  Serial.println(readString);
  if(readString == "OPEN")
  {
    Serial.println("OPEN");
    doorOpen();
  }
  readString = "";

  /*
  if(SW_state != (int)digitalRead(Sw_Pin))
  {
       if(SW_state == 1)
       {
         Serial.print("open\n");
         doorOpen();
       }
       SW_state = !SW_state;
  }*/
}
 
void doorOpen() {
/* 
  if(door_state == 0)
  {
    digitalWrite(door, HIGH);
    door_state = 1;
  }
  else
  {
    digitalWrite(door, LOW);
    door_state = 0;
  }*/
   digitalWrite(door, HIGH);
   Serial.print("Reached\n");
  delay(500);
  digitalWrite(door, LOW);
}

