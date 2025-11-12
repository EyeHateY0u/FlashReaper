import serial
from rich.console import Console
from rich.panel import Panel

console = Console()


def info():
	return "Esp8266 wifi jamming script kit"

def start(COM_Port):
    ser = serial.Serial(COM_Port, 115200, timeout=2)
    
    import time
    time.sleep(2)
    
    ser.reset_input_buffer()
    
    console.print("|[blink yellow]sending activation...[/]|")
    ser.write(b"?\n")
    

    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            console.print(f"Received: {data}")
            
            if data == "READY":
                console.print("|[bold green]ready received![/]|")

                console.print(Panel.fit("1. Rapid Channel Hop\n2. Probe Request Flood", style='bold green'))
                
                attack = console.input("Attack [1/2]: ").strip()
                ser.write((attack + "\n").encode())
                console.print(f"Sent: {attack}")
                break