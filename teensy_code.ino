#include <Arduino.h>
#include <arm_math.h>


#define NUM_CHANNELS 4
#define SAMPLE_RATE 10000 // Hz (increased for better resolution)
#define NUM_SAMPLES 1024  // Increased for better FFT resolution
#define FFT_SIZE NUM_SAMPLES/2

const int channelPins[NUM_CHANNELS] = {A0, A1, A2, A3};
unsigned long lastSampleTime = 0;

// Buffers for ADC data and FFT results
q15_t sensorValues[NUM_SAMPLES];
q15_t complexBuffer[NUM_SAMPLES * 2];
q15_t magnitude[FFT_SIZE];

void setup() {
  Serial.begin(115200);
  analogReadResolution(12); // Set ADC resolution to 12-bit for better precision
}

void loop() {
  if (micros() - lastSampleTime >= 1000000 / SAMPLE_RATE) {
    lastSampleTime = micros();

    // Collect samples for FFT
    for (int i = 0; i < NUM_SAMPLES; i++) {
      sensorValues[i] = analogRead(channelPins[0]); // Read from channel 0 for demonstration
    }

    // Prepare complex buffer for FFT input
    for (int i = 0; i < NUM_SAMPLES; i++) {
      complexBuffer[2 * i] = sensorValues[i];
      complexBuffer[2 * i + 1] = 0;
    }

    // Perform FFT using SimRC
    SimRC::FFT(complexBuffer, NUM_SAMPLES);

    // Calculate magnitude of FFT results
    arm_cmplx_mag_q15(complexBuffer, magnitude, FFT_SIZE);

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














#include <Arduino.h>
const int readPin = A0;  // Define the analog pin for impedance data

void setup() {
  Serial.begin(9600);
  pinMode(readPin, INPUT);
}

void loop() {
  int impedanceValue = analogRead(readPin);  // Read analog input
  float voltage = impedanceValue * (3.3 / 1023.0);  // Convert the analog reading to voltage
  
  // Impedance reading logic based on voltage, conversion to Ohms etc.
  float impedance = calculateImpedance(voltage); // Dummy function to calculate impedance based on input voltage
  
  Serial.print("Impedance (Ohms): ");
  Serial.println(impedance);

  delay(1000);  // Wait for a second before next reading
}

float calculateImpedance(float voltage) {
  // Calculate impedance based on voltage reading (dummy logic for now)
  return 1000.0 / voltage;  // Placeholder formula, should be replaced with actual formula
}











#include <ADC.h>
#include <Wire.h>

ADC *adc = new ADC(); // ADC object for Teensy analog pins
const int analogPin = A0; // Assuming the nanostructure channel data is fed to analog pin A0

void setup() {
  Serial.begin(9600);
  adc->setResolution(12); // Set resolution to 12 bits for the Teensy LC or 4.1
  adc->setAveraging(16);  // Averaging for better resolution data, can be adjusted as per requirements
  adc->setConversionSpeed(ADC_CONVERSION_SPEED::VERY_LOW_SPEED); // Set slowest for maximum resolution
  adc->setSamplingSpeed(ADC_SAMPLING_SPEED::VERY_LOW_SPEED);
}

void loop() {
  uint16_t val = adc->analogRead(analogPin);  // Read analog value from the nanostructure channel
  Serial.println(val);  // Print the raw data to Serial
  delay(10); // Sampling rate
}

















// Example Teensy code fragment adapted for CNT measurement
#include <ADC.h>

ADC *adc = new ADC(); // ADC object for high-resolution readings

const int analogPin = A0; // Pin connected to CNT structure
int resolution = 12;      // 12-bit resolution for Teensy LC and 4.1
unsigned long previousMillis = 0;
const long interval = 1000;  // Interval for sending data (in ms)

void setup() {
  Serial.begin(115200);
  adc->setResolution(resolution);  // Set resolution to 10, 11, or 12 bits
}

void loop() {
  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;

    int sensorValue = adc->analogRead(analogPin);  // Read the CNT measurement
    float voltage = (sensorValue / 4095.0) * 3.3;  // Convert reading to voltage (12-bit resolution)
    
    // Send data over Serial in a format that Python can parse (CSV-like format)
    Serial.print("CNT_VALUE,");
    Serial.print(voltage, 6);  // Send voltage measurement with 6 decimal precision
    Serial.println();
  }
}
















#include <ADC.h>
#include <Wire.h>

ADC *adc = new ADC(); // ADC object for Teensy analog pins
const int analogPin = A0; // Assuming the nanostructure channel data is fed to analog pin A0

void setup() {
  Serial.begin(9600);
  adc->setResolution(12); // Set resolution to 12 bits for the Teensy LC or 4.1
  adc->setAveraging(16);  // Averaging for better resolution data, can be adjusted as per requirements
  adc->setConversionSpeed(ADC_CONVERSION_SPEED::VERY_LOW_SPEED); // Set slowest for maximum resolution
  adc->setSamplingSpeed(ADC_SAMPLING_SPEED::VERY_LOW_SPEED);
}

void loop() {
  uint16_t val = adc->analogRead(analogPin);  // Read analog value from the nanostructure channel
  Serial.println(val);  // Print the raw data to Serial
  delay(10); // Sampling rate
}

