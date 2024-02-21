
void setup() {
  Serial.begin(9600);
}
uint8_t timer = 10;
String buf;
uint16_t  value;
void loop() {
  timer--;
  // send random data every 10s
  if (timer == 0) {
    timer = 10;
    value = rand() % 30;
    // Concatenation: ghép chuỗi
    buf = String("!temp:");
    buf += value;
    buf += '#';
    // send temperature data
    writeString(buf);
    value = rand() % 100;
    // Concatenation: ghép chuỗi
    buf = String("!humid:");
    buf += value;
    buf += '#';
    // send humidity data
    writeString(buf);
    value = rand() % 200;
    // Concatenation: ghép chuỗi
    buf = String("!bright:");
    buf += value;
    buf += '#';
    // send brightness data
    writeString(buf);
  }


  delay(1000);
}

void writeString(String stringData) { // Used to serially push out a String with Serial.write()

  for (int i = 0; i < stringData.length(); i++)
  {
    if (Serial.availableForWrite())
      Serial.write(stringData[i]);   // Push each char 1 by 1 on each loop pass
  }

}// end writeString
