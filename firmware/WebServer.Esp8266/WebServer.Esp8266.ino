#include <ESP8266WebServer.h>
#include <ESP8266WiFi.h>

ESP8266WebServer server(80);

void setup() {
	pinMode(LED_BUILTIN, OUTPUT);
	WiFi.mode(WIFI_AP_STA);
	WiFi.disconnect();
	WiFi.softAP("D0peServer", "12345678");

	server.on("/", handleRoot);

	startServer();

}

void loop(){
	server.handleClient();
}

void startServer(){
	server.begin();
	digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));
	delay(1000);
	digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));
}

void handleRoot(){
	String mainPage = scanNetworks();

	server.send(200, "text/html", mainPage);
}

String scanNetworks() {
	String html = "<html><body<h1>Found Networks:</h1><ul>";

	int networks = WiFi.scanNetworks();

	for (int i = 0; i < networks; i++) {
		html += "<li>|SSID: " + WiFi.SSID(i) + "|" + WiFi.BSSIDstr(i) + "|" + WiFi.RSSI(i) +"dBm|</li>";
		html += "<li>[Channel: " + String(WiFi.channel(i)) + "]</li>";
		html += "<li>[Encryption: " + Encryption(WiFi.encryptionType(i)) + "]</li>";
		html += "<li>[Hidden: " + String(WiFi.isHidden(i) ? "Yes" : "No") + "]</li></ul><br><br>";
	}

	return html;

} 

String Encryption(int encryptionType) {
	switch (encryptionType) {
	case ENC_TYPE_NONE:
		return "Open - EASY TARGET";
	case ENC_TYPE_WEP:
		return "WEP - VULNERABLE";
	case ENC_TYPE_TKIP:
		return "WPA/PSK - SECURE";
	case ENC_TYPE_CCMP:
		return "WPA2/PSK - SECURE";
	case ENC_TYPE_AUTO:
		return "Auto";
	default:
		return "Uknown";
	}
}