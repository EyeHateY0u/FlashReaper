#include <ESP8266WiFi.h>

void setup() {
	WiFi.mode(WIFI_STA);
	WiFi.disconnect();
	WiFi.setOutputPower(20.5);
	Serial.begin(115200);
	pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
	if (Serial.available() > 0) {
		String input = Serial.readString();
		input.trim();

		if (input == "?") {
			Serial.println("READY");

			waitForAttackCommand();

		}
	}
}

void waitForAttackCommand() {
	while (Serial.available() == 0) {
		digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));
		delay(500);
	}

	String attackType = Serial.readString();
	attackType.trim();

	if (attackType == "1") rapidChannelHop();
	else if (attackType == "2") probeRequestFlood();
}

void probeRequestFlood() {
	for (int i = 0; i < 100; i++) {
		digitalWrite(LED_BUILTIN, LOW);
		WiFi.scanNetworks(true, true);
		delay(1);
		WiFi.scanDelete();
	}
}

void rapidChannelHop() {
	for (int channel; channel < 13; channel++) {
		digitalWrite(LED_BUILTIN, LOW);
		wifi_set_channel(channel);
		delay(50);
	}
}