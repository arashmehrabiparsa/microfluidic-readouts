#include <Arduino.h>
#include <arm_math.h>

#define NUM_CHANNELS 18
#define SAMPLE_RATE 10000  // Hz
#define NUM_SAMPLES 1024
#define FFT_SIZE (NUM_SAMPLES / 2)

#define IMPEDANCE_INTERVAL 500  // ms for impedance check
#define CNT_INTERVAL 1000       // ms for CNT voltage measurement
#define LED_PIN 13              // Pin for the LED (Change as needed)
#define LED_BLINK_INTERVAL 3000 // LED blink interval in milliseconds

unsigned long lastSampleTime = 0;
unsigned long lastImpedanceTime = 0;
unsigned long lastCNTTime = 0;
unsigned long lastLEDBlinkTime = 0; // Time for the LED blink
bool ledState = LOW; // Current state of the LED
// {A0, A1, A2, A3, A4, A5, A6, A7, A8, A9} == {0, 1, 2, 3, 4, 5, 6, 7, 8, 9} pin mapping 
// {A15, A16, A17} == {10, 11, 12} pin mapping
// {A10, A11} == {36, 37} pin mapping for white cables
// {A12} == {28}
// {A13} == {29}
// {A14} == {GND}
const int channelPins[NUM_CHANNELS] = {A0, A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, A11, A12, A13, A14, A15, A16, A17}; // Fill in pins
q15_t sensorValues[NUM_SAMPLES];
q15_t complexBuffer[NUM_SAMPLES * 2];
q15_t magnitude[FFT_SIZE];

// Declare the real FFT instance
arm_rfft_instance_q15 fftInstance;

void setup() {
  Serial.begin(115200);
  analogReadResolution(12);  // 12-bit ADC resolution
  pinMode(LED_PIN, OUTPUT);   // Set LED pin as output
  
  // Initialize the real FFT instance for a 1024-point FFT
  arm_rfft_init_q15(&fftInstance, FFT_SIZE, 0, 1);
}

float calculateImpedance(float voltage) {
  return 1000.0 / voltage;  // Replace with your actual formula
}

void loop() {
  unsigned long currentTime = millis();

  // Blink LED every 3 seconds
  if (currentTime - lastLEDBlinkTime >= LED_BLINK_INTERVAL) {
    lastLEDBlinkTime = currentTime;
    ledState = !ledState; // Toggle LED state
    digitalWrite(LED_PIN, ledState); // Set the LED state
  }

  // FFT Sampling
  if (micros() - lastSampleTime >= (1000000 / SAMPLE_RATE)) {
    lastSampleTime = micros();

    for (int ch = 0; ch < NUM_CHANNELS; ch++) {
      // Collect samples for FFT
      for (int i = 0; i < NUM_SAMPLES; i++) {
        sensorValues[i] = analogRead(channelPins[ch]);  // Read from each channel
      }

      // Prepare complex buffer for FFT (interleaving real and imaginary parts)
      for (int i = 0; i < NUM_SAMPLES; i++) {
        complexBuffer[2 * i] = sensorValues[i];  // Real part
        complexBuffer[2 * i + 1] = 0;  // Imaginary part (set to 0)
      }

      // Perform real FFT
      arm_rfft_q15(&fftInstance, complexBuffer, magnitude);

      // Send FFT data with label "FFT"
      Serial.print("FFT,");
      for (int i = 0; i < FFT_SIZE; i += 4) {  // Send every 4th frequency bin
        Serial.print(i * SAMPLE_RATE / NUM_SAMPLES);  // Frequency bin
        Serial.print(",");
        Serial.print(magnitude[i]);  // Magnitude
        Serial.print(";");
      }
      Serial.println();
    }
  }

  // Impedance Measurement
  if (currentTime - lastImpedanceTime >= IMPEDANCE_INTERVAL) {
    lastImpedanceTime = currentTime;

    Serial.print("IMPEDANCE,");
    for (int ch = 0; ch < NUM_CHANNELS; ch++) {
      int impedanceValue = analogRead(channelPins[ch]);
      float voltage = impedanceValue * (3.3 / 4095.0);
      float impedance = calculateImpedance(voltage);
      Serial.print("Ch");
      Serial.print(ch);
      Serial.print(",");
      Serial.print(impedance);
      Serial.print(";");
    }
    Serial.println();
  }

  // CNT Voltage Measurement
  if (currentTime - lastCNTTime >= CNT_INTERVAL) {
    lastCNTTime = currentTime;

    Serial.print("CNT,");
    for (int ch = 0; ch < NUM_CHANNELS; ch++) {
      int cntValue = analogRead(channelPins[ch]);
      float cntVoltage = cntValue * (3.3 / 4095.0);
      Serial.print("Ch");
      Serial.print(ch);
      Serial.print(",");
      Serial.print(cntVoltage);
      Serial.print(";");
    }
    Serial.println();
  }
}
