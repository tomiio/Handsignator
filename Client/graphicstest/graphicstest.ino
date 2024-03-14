/**************************************************************************
  This is a library for several Adafruit displays based on ST77* drivers.

  Works with the Adafruit 1.8" TFT Breakout w/SD card
    ----> http://www.adafruit.com/products/358
  The 1.8" TFT shield
    ----> https://www.adafruit.com/product/802
  The 1.44" TFT breakout
    ----> https://www.adafruit.com/product/2088
  The 1.14" TFT breakout
  ----> https://www.adafruit.com/product/4383
  The 1.3" TFT breakout
  ----> https://www.adafruit.com/product/4313
  The 1.54" TFT breakout
    ----> https://www.adafruit.com/product/3787
  The 1.69" TFT breakout
    ----> https://www.adafruit.com/product/5206
  The 2.0" TFT breakout
    ----> https://www.adafruit.com/product/4311
  as well as Adafruit raw 1.8" TFT display
    ----> http://www.adafruit.com/products/618

  Check out the links above for our tutorials and wiring diagrams.
  These displays use SPI to communicate, 4 or 5 pins are required to
  interface (RST is optional).

  Adafruit invests time and resources providing this open source code,
  please support Adafruit and open-source hardware by purchasing
  products from Adafruit!

  Written by Limor Fried/Ladyada for Adafruit Industries.
  MIT license, all text above must be included in any redistribution
 **************************************************************************/

#include <Adafruit_GFX.h>    // Core graphics library
#include <Adafruit_ST7735.h> // Hardware-specific library for ST7735
#include <Adafruit_ST7789.h> // Hardware-specific library for ST7789
#include <SPI.h>

//#include <bitmapsLarge.h>

#define TFT_CS  27 //34
#define TFT_DC  28 //37
#define TFT_RST 29 //38

#define PIN_SPI2_MOSI 35
#define PIN_SPI2_SCLK 36
#define PIN_SPI2_MISO 9

// #if defined(ARDUINO_FEATHER_ESP32) // Feather Huzzah32
//   #define TFT_CS         14
//   #define TFT_RST        15
//   #define TFT_DC         32

// #elif defined(ESP8266)
//   #define TFT_CS         4
//   #define TFT_RST        16                                            
//   #define TFT_DC         5

// #else
//   // For the breakout board, you can use any 2 or 3 pins.
//   // These pins will also work for the 1.8" TFT shield.
//   #define TFT_CS        10
//   #define TFT_RST        9 // Or set to -1 and connect to Arduino RESET pin
//   #define TFT_DC         8
// #endif

// OPTION 1 (recommended) is to use the HARDWARE SPI pins, which are unique
// to each board and not reassignable. For Arduino Uno: MOSI = pin 11 and
// SCLK = pin 13. This is the fastest mode of operation and is required if
// using the breakout board's microSD card.

// For 1.44" and 1.8" TFT with ST7735 use:
Adafruit_ST7735 tft = Adafruit_ST7735(TFT_CS, TFT_DC, TFT_RST);

// For 1.14", 1.3", 1.54", 1.69", and 2.0" TFT with ST7789:
//Adafruit_ST7789 tft = Adafruit_ST7789(TFT_CS, TFT_DC, TFT_RST);


// OPTION 2 lets you interface the display using ANY TWO or THREE PINS,
// tradeoff being that performance is not as fast as hardware SPI above.
//#define TFT_MOSI 11  // Data out
//#define TFT_SCLK 13  // Clock out

// For ST7735-based displays, we will use this call
//Adafruit_ST7735 tft = Adafruit_ST7735(TFT_CS, TFT_DC, TFT_MOSI, TFT_SCLK, TFT_RST);

// OR for the ST7789-based displays, we will use this call
//Adafruit_ST7789 tft = Adafruit_ST7789(TFT_CS, TFT_DC, TFT_MOSI, TFT_SCLK, TFT_RST);


void setup(void) {
  //SPI(2);
  //SPIClass spi2(SPI);
  SPI.begin(PIN_SPI2_SCLK, PIN_SPI2_MISO, PIN_SPI2_MOSI, TFT_CS);

  Serial.begin(9600);
  Serial.print(F("Hello! ST77xx TFT Test"));

  // Use this initializer if using a 1.8" TFT screen:
  //tft.initR(INITR_BLACKTAB);      // Init ST7735S chip, black tab

  // OR use this initializer if using a 1.8" TFT screen with offset such as WaveShare:
  tft.initR(INITR_GREENTAB);      // Init ST7735S chip, green tab


  Serial.println(F("Initialized"));

  uint16_t time = millis();
  tft.fillScreen(ST77XX_BLACK);
  time = millis() - time;

  Serial.println(time, DEC);
  delay(500);

  // // large block of text
  // tft.fillScreen(ST77XX_BLACK);
  // testdrawtext("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur adipiscing ante sed nibh tincidunt feugiat. Maecenas enim massa, fringilla sed malesuada et, malesuada sit amet turpis. Sed porttitor neque ut ante pretium vitae malesuada nunc bibendum. Nullam aliquet ultrices massa eu hendrerit. Ut sed nisi lorem. In vestibulum purus a tortor imperdiet posuere. ", ST77XX_WHITE);
  // delay(1000);

  // // tft print function!
  // tftPrintTest();
  // delay(4000);

    // large block of text
  tft.fillScreen(ST77XX_BLACK);
  testdrawtext("Xin chào!! Toi ten la Nguyen Van A.", ST77XX_WHITE);
  delay(5000);

  // // tft print function!
  // tftPrintTest();
  // delay(4000);
  // tft.fillScreen(ST77XX_WHITE);
  // //Case 2: Multi Colored Images/Icons
  // int h = 127,w = 127, row, col, buffidx=0;
  // for (row=0; row<h; row++) { // For each scanline...
  //   for (col=0; col<w; col++) { // For each pixel...
  //     //To read from Flash Memory, pgm_read_XXX is required.
  //     //Since image is stored as uint16_t, pgm_read_word is used as it uses 16bit address
  //     tft.drawPixel(col, row, pgm_read_word(evive_in_hand + buffidx));
  //     buffidx++;
  //     } // end pixel
  //   }
  // delay(5000);



  // // a single pixel
  // tft.drawPixel(tft.width()/2, tft.height()/2, ST77XX_GREEN);
  // delay(500);

}

void loop() {
  //Serial.println("Hello!");
  
  // tft.invertDisplay(true);
  // delay(500);
  // tft.invertDisplay(false);
  // delay(500);

  // tft.fillScreen(ST77XX_BLACK);
  // delay(1000);
  // tft.fillScreen(ST77XX_RED);
  // delay(1000);
  // tft.fillScreen(ST77XX_GREEN);
  // delay(1000);
  // tft.fillScreen(ST77XX_BLUE);
  // delay(1000);
}

void testdrawtext(char *text, uint16_t color) {
  tft.setCursor(0, 0);
  tft.setTextColor(color);
  tft.setTextWrap(true);
  tft.print(text);
}
