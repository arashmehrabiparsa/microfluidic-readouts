#define _PWM_LOGLEVEL_       4

#include "Teensy_PWM.h"

#define USING_FLEX_TIMERS      true

// Define PWM pins
uint32_t PWM_Pins[] = { 4, 5, 6, 7, 0, 1, 2, 3, 8, 9, 10, 11, 28, 29, 36, 37, 13, 33 };

// Define ADC pins
uint32_t ADC_Pins[] = {A0, A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, A11, A12, A13, A14, A15, A16, A17};

// Same duty cycle and frequency for all pins
float dutyCycle[]   = { 50.0f, 50.0f, 50.0f, 50.0f, 50.0f, 50.0f, 50.0f, 50.0f, 50.0f, 50.0f, 50.0f, 50.0f, 50.0f, 50.0f, 50.0f, 50.0f };  
float frequency = 2000.0f;  // Same frequency for all channels

#define NUM_OF_PINS       ( sizeof(PWM_Pins) / sizeof(uint32_t) )

Teensy_PWM* PWM_Instance[NUM_OF_PINS];

const int ledPin = LED_BUILTIN;  // Use built-in LED pin
unsigned long previousMillis = 0;  
const long interval = 500;  // Interval for blinking (milliseconds)

void setup() {
  Serial.begin(921600);
  while (!Serial && millis() < 5000);
  delay(500);

  pinMode(ledPin, OUTPUT);  // Set LED pin as output
  for (int i = 0; i < 18; i++) {
    pinMode(ADC_Pins[i], INPUT);
  }
  for (uint8_t index = 0; index < NUM_OF_PINS; index++) {
    PWM_Instance[index] = new Teensy_PWM(PWM_Pins[index], frequency, dutyCycle[index]);
    if (PWM_Instance[index]) {
      PWM_Instance[index]->setPWM();
    }
  }

  Serial.println("Pin\tPWM_freq\tDutyCycle\tActual Freq");
  for (uint8_t index = 0; index < NUM_OF_PINS; index++) {
    if (PWM_Instance[index]) {
      Serial.print(PWM_Pins[index]);
      Serial.print("\t");
      Serial.print(frequency);
      Serial.print("\t\t");
      Serial.print(dutyCycle[index]);
      Serial.print("\t\t");
      Serial.println(PWM_Instance[index]->getActualFreq(), 4);
    }
  }
}

void loop() {
  // Blink the LED
  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;
    digitalWrite(ledPin, !digitalRead(ledPin));  // Toggle LED state
  }

  // Capture the PWM signals using ADC on defined ADC pins
  Serial.println("Capturing PWM signals from ADC pins:");

  for (uint8_t i = 0; i < NUM_OF_PINS; i++) {
    int adcValue = analogRead(ADC_Pins[i]);
    float voltage = (adcValue / 1023.0) * 3.3;  // Teensy ADC is 10-bit, max value is 1023 and reference voltage is 3.3V

    Serial.print("ADC Pin: A");
    Serial.print(10 + i);  // Adjust based on the ADC mapping
    Serial.print(", ADC Value: ");
    Serial.print(adcValue);
    Serial.print(", Voltage: ");
    Serial.print(voltage, 4);
    Serial.println(" V");
  }

  delay(1000);  // Reduce the delay for more frequent reads
}
