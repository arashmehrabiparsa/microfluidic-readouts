#include <Arduino.h>
#include <arm_math.h>

#define NUM_CHANNELS 18
#define SAMPLE_RATE 10  // Hz
#define NUM_SAMPLES 1024
#define FFT_SIZE (NUM_SAMPLES / 2)
#define IMPEDANCE_INTERVAL 500  // ms for impedance check
#define CNT_INTERVAL 1000      // ms for CNT voltage measurement
#define LED_PIN 13             
#define LED_BLINK_INTERVAL 3000
#define PWM_FREQ 10000        // PWM frequency in Hz
#define PWM_RES 12            // 12-bit PWM resolution

// Timing variables
unsigned long lastSampleTime = 0;
unsigned long lastImpedanceTime = 0;
unsigned long lastCNTTime = 0;
unsigned long lastLEDBlinkTime = 0;
unsigned long lastPWMToggleTime = 0;
bool ledState = LOW;
bool pwmState = LOW;

// Pin definitions
const int channelPins[NUM_CHANNELS] = {A0, A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, A11, A12, A13, A14, A15, A16, A17};
const int pwmPins[] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 28, 29, 33, 36, 37};
const int NUM_PWM = 18;

// FFT variables
q15_t sensorValues[NUM_SAMPLES];
q15_t complexBuffer[NUM_SAMPLES * 2];
q15_t magnitude[FFT_SIZE];
arm_rfft_instance_q15 fftInstance;

void setupPWM() {
    analogWriteResolution(PWM_RES);  // Set PWM resolution
    
    for(int i = 0; i < NUM_PWM; i++) {
        pinMode(pwmPins[i], OUTPUT);
        analogWriteFrequency(pwmPins[i], PWM_FREQ);
        analogWrite(pwmPins[i], 0);  // Initialize all pins to 0V
    }
}

void updatePWM(bool state) {
    for(int i = 0; i < NUM_PWM; i++) {
        if(state) {
            analogWrite(pwmPins[i], 4095);  // Full high (3.3V)
        } else {
            analogWrite(pwmPins[i], 0);     // Full low (0V)
        }
    }
}

void setup() {
    Serial.begin(115200);
    analogReadResolution(12);  // 12-bit ADC resolution
    pinMode(LED_PIN, OUTPUT);  // Set LED pin as output
    
    // Setup PWM pins
    setupPWM();
    
    // Initialize the real FFT instance for a 1024-point FFT
    arm_rfft_init_q15(&fftInstance, FFT_SIZE, 0, 1);
}

float calculateImpedance(float voltage) {
    return 1000.0 / voltage;  // Replace with your actual formula
}

void loop() {
    unsigned long currentTime = millis();
    unsigned long currentMicros = micros();

    // Generate square wave using PWM
    // Toggle every 50 microseconds (10kHz)
    if(currentMicros - lastPWMToggleTime >= 50) {
        lastPWMToggleTime = currentMicros;
        pwmState = !pwmState;
        updatePWM(pwmState);
    }

    // Blink LED every 3 seconds
    if (currentTime - lastLEDBlinkTime >= LED_BLINK_INTERVAL) {
        lastLEDBlinkTime = currentTime;
        ledState = !ledState;
        digitalWrite(LED_PIN, ledState);
    }

    // FFT Sampling
    if (currentMicros - lastSampleTime >= (1000000 / SAMPLE_RATE)) {
        lastSampleTime = currentMicros;
        
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