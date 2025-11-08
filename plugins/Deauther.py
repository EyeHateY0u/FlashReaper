import serial
from rich.console import Console

console = Console()

def read_until_marker(ser, marker):
    lines = []
    while True:
        if ser.in_waiting > 0:
            raw_data = ser.readline()
            try:
                line = raw_data.decode('utf-8', errors='ignore').strip()
                if line == marker:
                    break
                if line:
                    lines.append(line)
            except:
                pass
    return lines

def info():
    return "Deauther communication plugin"

def start(COM):
    try:
        ser = serial.Serial(COM, 115200, timeout=1)
        console.print(f"[yellow]Connected to {COM}[/yellow]")
        
        # Тест - чи отримуємо щось від прошивки
        ser.write("!\n".encode())
        ser.flush()
        console.print("[yellow]Sent '!' signal[/yellow]")
        
        # Чекаємо 2 секунди і перевіряємо буфер
        import time
        time.sleep(2)
        
        if ser.in_waiting > 0:
            console.print(f"[green]Data available: {ser.in_waiting} bytes[/green]")
            raw_data = ser.read(ser.in_waiting)
            console.print(f"[green]Raw data: {raw_data}[/green]")
        else:
            console.print("[red]No data received from device[/red]")
            return
            
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")