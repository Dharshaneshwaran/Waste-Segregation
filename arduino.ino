#define GREEN_LED 9
#define RED_LED 10

void setup() {
  Serial.begin(9600);
  pinMode(GREEN_LED, OUTPUT);
  pinMode(RED_LED, OUTPUT);
}

void loop() {
  if (Serial.available()) {
    char signal = Serial.read();

    if (signal == 'G') {
      digitalWrite(GREEN_LED, HIGH);
      delay(500);
      digitalWrite(GREEN_LED, LOW);
    }
    else if (signal == 'R') {
      digitalWrite(RED_LED, HIGH);
      delay(500);
      digitalWrite(RED_LED, LOW);
    }
  }
}
