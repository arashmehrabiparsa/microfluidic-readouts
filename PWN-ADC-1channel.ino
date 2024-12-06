// PWM Configuration for Teensy 4.1 to Generate a ±1.65V Square Wave Centered at 0V
const int pwmPin = 9;       // PWM output pin on Teensy 4.1 (choose any PWM-capable pin)
const int ledPin = 13;      // LED pin (onboard LED, or choose another pin if external)
const int adcPin = A0;      // ADC pin for reading analog values (A0 as an example)
const int frequency = 1000; // PWM frequency in Hz (1 kHz)
const int blinkInterval = 500; // LED blink interval in milliseconds

void setup() {
  // Initialize the LED pin
  pinMode(ledPin, OUTPUT);

  // Initialize the PWM output pin
  pinMode(pwmPin, OUTPUT);
  
  // Set the PWM frequency on the chosen pin
  analogWriteFrequency(pwmPin, frequency);
  
  // Set initial PWM duty cycle to 50% (square wave)
  analogWrite(pwmPin, 128);  // 128 is 50% of 255
  
  // Initialize serial communication to output ADC readings
  Serial.begin(115200);
}

void loop() {
  // Blink the LED at a regular interval
  digitalWrite(ledPin, HIGH);   // Turn the LED on
  delay(blinkInterval);         // Wait for half of the blink interval
  digitalWrite(ledPin, LOW);    // Turn the LED off
  delay(blinkInterval);         // Wait for half of the blink interval
  
  // PWM signal is continuously generated on pin 9
  // You can modify the duty cycle if desired (this is just 50% as an example)
  analogWrite(pwmPin, 128);     // Set to 50% duty cycle for a square wave
  
  // Read from the ADC pin
  int adcValue = analogRead(adcPin);  // Read the analog value from pin A0
  
  // Output the ADC value to the serial monitor
  Serial.print("ADC Value: ");
  Serial.println(adcValue);
  
  // Optionally, you could adjust the PWM duty cycle dynamically
  // to create a more complex behavior based on the ADC readings.
}
