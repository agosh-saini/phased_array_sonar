// Defining COnstants

// Sonar pins
const int trig1 = 3;
const int echo1 = 2;
const int trig2 = 5;
const int echo2 = 4;
const int trig3 = 6;
const int echo3 = 7;

// LED pin
const int ledPin = 13;

// setup 
void setup() {
  Serial.begin(9600);

  pinMode(trig1, OUTPUT); pinMode(echo1, INPUT);
  pinMode(trig2, OUTPUT); pinMode(echo2, INPUT);
  pinMode(trig3, OUTPUT); pinMode(echo3, INPUT);

  pinMode(ledPin, OUTPUT);

}


void loop() {

  digitalWrite(ledPin, HIGH); 
  delay(50);
  digitalWrite(ledPin, LOW); 

  float d1 = readDistance(trig1, echo1);
  float d2 = readDistance(trig2, echo2);
  float d3 = readDistance(trig3, echo3);

  // sanity check
  if (d1 < 0 || d2 < 0 || d3 < 0) return;


  Serial.print(d1); Serial.print(",");
  Serial.print(d2); Serial.print(",");
  Serial.println(d3);

  delay(100);
}


// distance function
float readDistance(int sensorTrig, int sensorEcho) {
  digitalWrite(sensorTrig, LOW);
  delayMicroseconds(2);

  digitalWrite(sensorTrig, HIGH);
  delayMicroseconds(10);

  digitalWrite(sensorTrig, LOW);

  long duration = pulseIn(sensorEcho, HIGH, 30000);

  float distance = duration * 0.034 / 2;

  if (duration == 0) return -1.0;
  return distance;
}
