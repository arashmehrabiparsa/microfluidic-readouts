#include "Teensy_PWM.h"

#define USING_FLEX_TIMERS true

#if USING_FLEX_TIMERS
uint32_t PWM_Pins[] = { 4, 5, 6, 7 };
#else
uint32_t PWM_Pins[] = { 10, 11, 14, 15 };
#endif

uint32_t ADC_Pins[] = { A10, A11, A12, A13 };  // Adjust this to your required ADC pins
float dutyCycle[] = { 50.0f, 50.0f, 50.0f, 50.0f };  // 50% for each PWM pin
float frequency = 2000.0f;  // Frequency in Hz

#define NUM_OF_PINS (sizeof(PWM_Pins) / sizeof(uint32_t))

Teensy_PWM* PWM_Instance[NUM_OF_PINS];

void setup() {
  Serial.begin(921600);

  // PWM setup for each pin
  for (uint8_t i = 0; i < NUM_OF_PINS; i++) {
    PWM_Instance[i] = new Teensy_PWM(PWM_Pins[i], frequency, dutyCycle[i]);
    if (PWM_Instance[i]) {
      PWM_Instance[i]->setPWM();
    }
  }

  // Display initial setup details
  Serial.println("Pin\tPWM_Freq\tDutyCycle\tActual_Freq");
  for (uint8_t i = 0; i < NUM_OF_PINS; i++) {
    if (PWM_Instance[i]) {
      Serial.print(PWM_Pins[i]);
      Serial.print("\t");
      Serial.print(frequency);
      Serial.print("\t\t");
      Serial.print(dutyCycle[i]);
      Serial.print("\t\t");
      Serial.println(PWM_Instance[i]->getActualFreq(), 4);
    }
  }
}

void loop() {
  Serial.println("ADC Readings:");
  for (uint8_t i = 0; i < NUM_OF_PINS; i++) {
    int adcValue = analogRead(ADC_Pins[i]);
    float voltage = (adcValue / 1023.0) * 3.3;
    Serial.print("ADC Pin: A");
    Serial.print(10 + i);
    Serial.print(", ADC Value: ");
    Serial.print(adcValue);
    Serial.print(", Voltage: ");
    Serial.print(voltage, 4);
    Serial.println(" V");
  }
  delay(100);  // Lower delay for more frequent reads
}
