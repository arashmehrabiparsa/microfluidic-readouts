#define _PWM_LOGLEVEL_       4

#include "Teensy_PWM.h"

#define USING_FLEX_TIMERS      true

#if USING_FLEX_TIMERS
uint32_t PWM_Pins[] = { 4, 5, 6, 7 };
#else
uint32_t PWM_Pins[] = { 10, 11, 14, 15 };
#endif

uint32_t ADC_Pins[] = { A10, A11, A12, A13 };

// Same duty cycle and frequency for all pins
float dutyCycle[]   = { 50.0f, 50.0f, 50.0f, 50.0f };  // 50% duty cycle for all channels
float frequency = 2000.0f;  // Same frequency for all channels

#define NUM_OF_PINS       ( sizeof(PWM_Pins) / sizeof(uint32_t) )

Teensy_PWM* PWM_Instance[NUM_OF_PINS];

void setup() {
  /*Serial.begin(115200);*/
  Serial.begin(921600);

  while (!Serial && millis() < 5000);
  delay(500);

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
  // Capture the PWM signals using ADC on A10-A14
  Serial.println("Capturing PWM signals from ADC pins (A10-A14):");

  for (uint8_t i = 0; i < NUM_OF_PINS; i++) {
    int adcValue = analogRead(ADC_Pins[i]);
    float voltage = (adcValue / 1023.0) * 3.3;  // Teensy ADC is 10-bit, max value is 1023 and reference voltage is 3.3V

    Serial.print("ADC Pin: A");
    Serial.print(10 + i);  // Mapping A10-A14
    Serial.print(", ADC Value: ");
    Serial.print(adcValue);
    Serial.print(", Voltage: ");
    Serial.print(voltage, 4);
    Serial.println(" V");
  }

  delay(1000);  // Reduce the delay for more frequent reads
}
