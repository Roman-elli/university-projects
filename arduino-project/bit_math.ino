int number1;
int number2;

int result_AND;
int result_OR;
int result_XOR;
int contadorrgb;
int result;
int tempo_inicial = 0;
int tempo_reset;

int lastButtonState = HIGH;
long lastDebounceTime = 0;
long debounceDelay = 50;

int buttonState;
int buttonPin = 2;

int valorpressionado = -2;

void setup() {
  Serial.begin(9600);

  // NUMBER 1
  pinMode(13, OUTPUT);
  pinMode(12, OUTPUT);
  pinMode(11, OUTPUT);
  pinMode(10, OUTPUT);

  // NUMBER 2
  pinMode(9, OUTPUT);
  pinMode(8, OUTPUT);
  pinMode(7, OUTPUT);
  pinMode(6, OUTPUT);

  // RGB
  pinMode(5, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(3, OUTPUT);

  // BUTTON
  pinMode(buttonPin, INPUT_PULLUP);
}

void loop() {
  if (valorpressionado == -2) {
    Serial.println("Press button to start!");
    valorpressionado = -1;
  }

  int reading = digitalRead(buttonPin);

  if (reading != lastButtonState) {
    lastDebounceTime = millis();
  }

  if ((millis() - lastDebounceTime) > debounceDelay) {
    if (buttonState != reading) buttonState = reading;
  }

  if (((millis() - tempo_inicial) == 3500) && (valorpressionado > -1))
    Serial.println("50% of the time has passed.");
  if ((millis() - tempo_inicial) == (0.75 * 7000) && (valorpressionado > -1))
    Serial.println("75% of the time has passed.");

  // Start:
  if (reading == LOW) {
    // Start game timer
    if (tempo_inicial == 0) {
      tempo_inicial = millis();
    }

    tempo_reset = millis();

    if (valorpressionado == -1) {
      // Generate random numbers
      int number1 = random(1, 16);
      int number2 = random(1, 16);

      // Logic operations
      int result_AND = (number2 & number1);
      int result_OR = (number2 | number1);
      int result_XOR = (number2 ^ number1);
      int contadorrgb = random(0, 3);
      int tempo_inicial = 0;

      // AND
      if (contadorrgb == 0) {
        digitalWrite(5, HIGH);
        result = result_AND;
      }
      // OR
      else if (contadorrgb == 1) {
        digitalWrite(4, HIGH);
        result = result_OR;
      }
      // XOR
      else if (contadorrgb == 2) {
        digitalWrite(3, HIGH);
        result = result_XOR;
      }

      // Display number2 on LEDs
      for (int digit = 0; digit < 4; digit++) {
        digitalWrite(10 + digit, (number2 >> digit) & 1);
      }

      // Display number1 on LEDs
      for (int digit = 0; digit < 4; digit++) {
        digitalWrite(6 + digit, (number1 >> digit) & 1);
      }
    }

    // User pressed button
    valorpressionado++;
    if (valorpressionado >= 0) {
      Serial.print("ANSWER: ");
      Serial.print(valorpressionado);
      Serial.println("  ** Press the button to add 1 to your answer! **");
      delay(100);
    }

    // Reset function
    while (reading == LOW) {
      reading = digitalRead(buttonPin);
      if (reading == HIGH) {
        tempo_reset = millis();
      }
      if (((millis() - tempo_reset) >= 1000) && ((millis() - tempo_reset) <= 1500)) {
        Serial.println("RESET in 3");
        delay(1000);
        Serial.println("RESET in 2");
        delay(1000);
        Serial.println("RESET in 1");
        delay(1000);
        result = 200;
      }
    }
  }

  // End of game
  if (result == 200) {
    Serial.println("Game reset.");

    // LED scanning
    int counter = 7;
    for (int count = 6; count <= 13; count++) {
      digitalWrite(count, LOW);
    }
    for (int count1 = 0; count1 <= 2; count1++) {
      for (int count = 6; count <= 9; count++) {
        digitalWrite(count, HIGH);
        digitalWrite(count + counter, HIGH);
        delay(400);
        digitalWrite(count + counter, LOW);
        digitalWrite(count, LOW);
        counter -= 2;
      }
      counter = 7;
    }

    // RGB blinking
    for (int count = 6; count <= 13; count++) {
      digitalWrite(count, LOW);
    }
    for (int countrgb = 3; countrgb <= 5; countrgb++) {
      digitalWrite(countrgb, HIGH);
      delay(5000 / 6);
      digitalWrite(countrgb, LOW);
      delay(5000 / 6);
    }

    valorpressionado = -2;
    result = 0;
  }

  if (((millis() - tempo_inicial) % 7000 == 0)) {

    // Victory mode
    if (valorpressionado == result) {
      Serial.println("You won the game!");
      for (int count1 = 0; count1 <= 4; count1++) {
        for (int count2 = 6; count2 <= 13; count2++) {
          digitalWrite(count2, LOW);
        }
        delay(500);
        for (int count2 = 6; count2 <= 13; count2++) {
          digitalWrite(count2, HIGH);
        }
        delay(500);
      }

      // LED scanning
      int counter = 7;
      for (int count = 6; count <= 13; count++) {
        digitalWrite(count, LOW);
      }
      for (int count1 = 0; count1 <= 2; count1++) {
        for (int count = 6; count <= 9; count++) {
          digitalWrite(count, HIGH);
          digitalWrite(count + counter, HIGH);
          delay(400);
          digitalWrite(count + counter, LOW);
          digitalWrite(count, LOW);
          counter -= 2;
        }
        counter = 7;
      }
      valorpressionado = -2;
    }

    // Defeat mode
    if ((valorpressionado != result) && ((millis() - tempo_inicial) % 7000 == 0) && (valorpressionado > -1)) {
      Serial.println("You lost the game.");
      Serial.print("Correct answer: ");
      Serial.println(result);

      // RGB blinking
      for (int count = 6; count <= 13; count++) {
        digitalWrite(count, LOW);
      }
      for (int countrgb = 3; countrgb <= 5; countrgb++) {
        digitalWrite(countrgb, HIGH);
        delay(5000 / 6);
        digitalWrite(countrgb, LOW);
        delay(5000 / 6);
      }

      // Reset timer
      valorpressionado = -2;
    }
  }

  if (valorpressionado == -1) {
    tempo_inicial = millis();
    tempo_reset = millis();
  }

  lastButtonState = reading;
}