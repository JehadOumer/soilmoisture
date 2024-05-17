// Define the pin numbers
int sensorPin = A0;   // Soil moisture sensor output connected to A0
int relayPin = 2;     // Relay switch connected to pin 2
int redLED = 13;      // Red LED connected to pin 13
int yellowLED = 12;   // Yellow LED connected to pin 12
int greenLED = 11;    // Green LED connected to pin 11
int buzzerPin = 10;   // Buzzer connected to pin 10

// Define delay times in milliseconds
const int stabilizationDelay = 2000; // Time for sensor to stabilize after relay is activated
const int readingInterval = 500;     // Time between sensor readings
const int readingDuration = 5000;    // Total time to take readings
const int cycleDelay = 1000;         // Delay before the next cycle starts

// Variable to store the sum of readings and number of readings
int sumMoisture = 0;
int numReadings = 0;

// Setup routine runs once when you press reset
void setup() {
  Serial.begin(9600);
  pinMode(relayPin, OUTPUT);
  pinMode(redLED, OUTPUT);
  pinMode(yellowLED, OUTPUT);
  pinMode(greenLED, OUTPUT);
  pinMode(buzzerPin, OUTPUT);
}

// Function to update LED and Buzzer states
void updateIndicators(String category) {
  digitalWrite(redLED, LOW);
  digitalWrite(yellowLED, LOW);
  digitalWrite(greenLED, LOW);
  digitalWrite(buzzerPin, LOW);
  
  if (category == "Very Dry") {
    digitalWrite(redLED, HIGH);
    digitalWrite(buzzerPin, HIGH); // Activate buzzer for Very Dry
  } else if (category == "Dry") {
    digitalWrite(yellowLED, HIGH);
  } else if (category == "Humid") {
    digitalWrite(greenLED, HIGH);
  }
}

// Loop routine runs over and over again forever
void loop() {
  digitalWrite(relayPin, HIGH);
  Serial.println("Relay activated");
  delay(stabilizationDelay); // Allow sensor to stabilize

  sumMoisture = 0;
  numReadings = 0;

  unsigned long startTime = millis();
  while (millis() - startTime < readingDuration) {
    int sensorValue = analogRead(sensorPin);
    sumMoisture += sensorValue;
    numReadings++;
    Serial.print("Sensor reading: ");
    Serial.println(sensorValue);
    delay(readingInterval); // Delay between readings
  }

  int average = sumMoisture / numReadings;
  digitalWrite(relayPin, LOW);

  // Determine the category and relative moisture value
  String category;
  float relativeMoisture = map(average, 0, 1023, 100, 0) / 100.0; // Convert to a range from 0.00 to 1.00
  if (relativeMoisture > 0.66) {
    category = "Humid";
  } else if (relativeMoisture > 0.33) {
    category = "Dry";
  } else {
    category = "Very Dry";
  }

  updateIndicators(category);

  Serial.print("Average Moisture Level: ");
  Serial.print(category);
  Serial.print(", ");
  Serial.print(relativeMoisture, 2);  // Print as a floating point number with two decimal places
  Serial.println();

  delay(cycleDelay); // Delay before the next cycle starts
}
