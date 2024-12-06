#include <Arduino.h>
#include <ADC.h>
#include <arm_math.h>

#define NUM_CHANNELS 4
#define SAMPLE_RATE 10000 // Hz
#define NUM_SAMPLES 1024
#define FFT_SIZE (NUM_SAMPLES / 2)

ADC *adc = new ADC(); // ADC object for Teensy analog pins
const int channelPins[NUM_CHANNELS] = {A0, A1, A2, A3};
unsigned long lastSampleTime = 0;

// Use float32_t consistently for better compatibility with ARM DSP functions
float32_t sensorValues[NUM_SAMPLES * 2];  // Doubled size for real and imaginary parts
float32_t magnitude[FFT_SIZE];

// Declare the FFT instance
arm_cfft_instance_f32 fft_instance;

void setup() {
  Serial.begin(115200);
  analogReadResolution(12); // Set ADC resolution to 12-bit for better precision
  
  // Initialize ADC
  for (int i = 0; i < NUM_CHANNELS; i++) {
    adc->setAveraging(16, channelPins[i]);  // Set averaging to 16 samples
    adc->setResolution(12, channelPins[i]); // Set ADC resolution to 12 bits
    adc->setConversionSpeed(ADC_CONVERSION_SPEED::VERY_LOW_SPEED, channelPins[i]);
    adc->setSamplingSpeed(ADC_SAMPLING_SPEED::VERY_LOW_SPEED, channelPins[i]);
  }
  
  // Initialize the CFFT instance
  arm_cfft_init_f32(&fft_instance, NUM_SAMPLES);
}

void loop() {
  if (micros() - lastSampleTime >= 1000000 / SAMPLE_RATE) {
    lastSampleTime = micros();

    // Collect samples for FFT
    for (int i = 0; i < NUM_SAMPLES; i++) {
      sensorValues[2*i] = (float32_t)adc->analogRead(channelPins[0]); // Read from channel 0
      sensorValues[2*i+1] = 0.0f; // Imaginary part set to 0
    }

    // Perform FFT
    arm_cfft_f32(&fft_instance, sensorValues, 0, 1);

    // Calculate magnitude of FFT results
    arm_cmplx_mag_f32(sensorValues, magnitude, FFT_SIZE);

    // Compress and transmit FFT results
    for (int i = 0; i < FFT_SIZE; i += 4) { // Sending every 4th point for compression
      Serial.print(i * SAMPLE_RATE / NUM_SAMPLES); // Frequency
      Serial.print(",");
      Serial.print(magnitude[i]);
      Serial.print(";");
    }
    Serial.println();
  }
}