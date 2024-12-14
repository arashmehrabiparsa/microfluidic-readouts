#define _PWM_LOGLEVEL_       4

#include "Teensy_PWM.h"

#define USING_FLEX_TIMERS      true
#define SAMPLE_RATE 100

#if USING_FLEX_TIMERS
uint32_t PWM_Pins[] = { 4, 5, 6, 7 };
#else
uint32_t PWM_Pins[] = { 10, 11, 14, 15 };
#endif

uint32_t ADC_Pins[] = {A0, A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, A11, A12, A13, A14, A15, A16, A17};

// Same duty cycle and frequency for all pins
float dutyCycle[]   = { 50.0f, 50.0f, 50.0f, 50.0f };  // 50% duty cycle for all channels
float frequency = 2000.0f;  // Same frequency for all channels

#define NUM_OF_PINS       ( sizeof(PWM_Pins) / sizeof(uint32_t) )
#define NUM_ADC_PINS sizeof(ADC_Pins) / sizeof(uint32_t)
Teensy_PWM* PWM_Instance[NUM_OF_PINS];

const int bufferSize = NUM_ADC_PINS * 2;
int sampleRate = SAMPLE_RATE; 
IntervalTimer sampleTimer;
uint8_t buffer1[2000][bufferSize];
volatile bool bufferReady = false;
volatile int bufferHead=0;
volatile int bufferTail=2;
volatile int bufferIndex = 0;


void sampleData() {
  for (uint16_t i = 0; i < NUM_ADC_PINS; i++) {
    int sensorValue = analogRead(ADC_Pins[i]);
    buffer1[bufferTail][bufferIndex++] = sensorValue & 0xFF; // Lower byte
    buffer1[bufferTail][bufferIndex++] = sensorValue>>8; // Upper byte
  }

  
  bufferIndex=0;
  bufferTail++;
  if(bufferTail>=2000){
    bufferTail=0;
  }

}


void setup() {
  /*Serial.begin(115200);*/
  Serial.begin(921600);

  while (!Serial && millis() < 5000);
  delay(500);
  for (int i = 0; i < NUM_ADC_PINS; i++) {
    pinMode(ADC_Pins[i], INPUT);
  }
  for (uint8_t index = 0; index < NUM_OF_PINS; index++) {
    PWM_Instance[index] = new Teensy_PWM(PWM_Pins[index], frequency, dutyCycle[index]);
    if (PWM_Instance[index]) {
      PWM_Instance[index]->setPWM();
    }
  }
  sampleTimer.begin(sampleData, 1000000 / sampleRate);
  delay(2);

}

void loop() {

    while(bufferHead!=bufferTail){

    Serial.write(buffer1[bufferHead],36);
    bufferHead++;
    if(bufferHead>=2000){
      bufferHead=0;
    }
  }


}
