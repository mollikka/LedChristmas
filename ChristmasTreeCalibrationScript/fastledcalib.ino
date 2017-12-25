#include <FastLED.h>
#define NUM_LEDS 150
#define DATA_PIN 13
#define INPUTPIN 2

CRGB leds[NUM_LEDS];

volatile int chosen = 0;

unsigned long lastclick = millis();

void setup() {
  // put your setup code here, to run once:
  FastLED.addLeds<WS2811, DATA_PIN>(leds, NUM_LEDS);
  pinMode(INPUTPIN, INPUT);
  attachInterrupt(digitalPinToInterrupt(INPUTPIN), inputClick, CHANGE);
}

void inputClick() {
  if (millis() - lastclick < 1000) {return;}
  if (digitalRead(INPUTPIN)==HIGH) {
    lastclick = millis();
    chosen++;
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  // First, clear the existing led values
  FastLED.clear();
  leds[chosen%150] = CHSV( 255, 0, 255); 
  FastLED.show();
}

/*
void loop() {
  FastLED.clear();
  int j = millis()/50;
  for(int led = 0; led < 20; led++) {
    leds[(led+j)%NUM_LEDS] = CHSV( 255,255,led*11 );
    leds[(NUM_LEDS/3+led+j)%NUM_LEDS] = CHSV( 255/3,255,led*11 );
    leds[(NUM_LEDS/3*2+led+j)%NUM_LEDS] = CHSV( 255/3*2,255,led*11 );
  }
  FastLED.show();
}
*/
/*
void loop() {
  // put your main code here, to run repeatedly:
  // First, clear the existing led values
  FastLED.clear();
  for(int led = 0; led < NUM_LEDS; led++) { 
    leds[led] = CHSV( 0, 0, 255); 
  }
  FastLED.show();
}
*/
