const int LDR = A0;
int input_val = 0;
bool lights, hot;


#define RT0 10000   // Ω
#define B 3977      // K
#define VCC 5    //Supply voltage
#define R 10000  //R=10KΩ
//Variables
float RT, VR, ln, TX, T0, VRT, ref;


void setup()
{
  pinMode(11, OUTPUT);    // sets the digital pin 13 as output
  pinMode (2,INPUT); // The PIR Sensor
  pinMode (12,OUTPUT); // The LED for PIR
  digitalWrite(11, LOW);  // sets the digital pin 13 off
  Serial.begin(9600);
  lights = false;
  hot = false;

  pinMode(3, OUTPUT);    // sets the digital pin 3 as output
  Serial.begin(9600);
  T0 = 25 + 273.15;                 //Temperature T0 from datasheet, conversion from Celsius to kelvin
}

void loop()
{
  input_val = analogRead(LDR);
  //Serial.print("LDR Value is: ");
  //Serial.println(input_val);
  delay(500);
  if (input_val < 500 & !lights){
      Serial.println("  TURN LIGHTS ON  ");
      lights = true;
      digitalWrite(11, HIGH); // sets the digital pin 13 on
  }
  else 
    if (input_val > 600 & lights){
      Serial.println("  TURN LIGHTS OFF  ");
      lights = false;
      digitalWrite(11, LOW);  // sets the digital pin 13 off
    }

   int val=digitalRead(2);
    if (val==1){ //When object passed
        Serial.print("     MOVEMENT\n");
        digitalWrite(12,HIGH);//ON
        delay(400);         //Wait
        digitalWrite(12,LOW); //Off
    }else{      // When No Object Passed
        digitalWrite(12,LOW); //off
    }

  VRT = analogRead(A1);              //Acquisition analog value of VRT
  ref = VRT;
  VRT = (5.00 / 1023.00) * VRT;      //Conversion to voltage
  VR = VCC - VRT;
  RT = VRT / (VR / R);               //Resistance of RT
 
  ln = log(RT / RT0);
  TX = (1 / ((ln / B) + (1 / T0))); //Temperature from thermistor
 
  TX = TX - 273.15;                 //Conversion to Celsius
  //Serial.print(ref);
  //Serial.print("\n");
  if (ref < 900.00 & !hot){
    Serial.print("   TOO HOT\n");
    hot = true;
    digitalWrite(3,HIGH);//ON
  }
  if(ref > 910.00 & hot){
      Serial.print("   NORMAL TEMPRATURE\n");
      hot = false;
      digitalWrite(3,LOW);//ON
  }    
  
  /*Serial.print("Temperature:");
  Serial.print("\t");
  Serial.print(TX);
  Serial.print("C\t\t");
  Serial.print(TX + 273.15);        //Conversion to Kelvin
  Serial.print("K\t\t");
  Serial.print((TX * 1.8) + 32);    //Conversion to Fahrenheit
  Serial.println("F");*/
  delay(100);

    
}
