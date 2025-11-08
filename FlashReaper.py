from rich.console import Console
from rich.panel import Panel
import importlib.util
from rich import box
import subprocess
import serial
import time
import os

console = Console()
logo = '''
                                                                                                              
 ▄▄▄▄▄▄▄▄  ▄▄▄▄                          ▄▄        ▄▄▄▄▄▄                                                     
 ██▀▀▀▀▀▀  ▀▀██                          ██        ██▀▀▀▀██                                                   
 ██          ██       ▄█████▄  ▄▄█████▄  ██▄████▄  ██    ██   ▄████▄    ▄█████▄  ██▄███▄    ▄████▄    ██▄████ 
 ███████     ██       ▀ ▄▄▄██  ██▄▄▄▄ ▀  ██▀   ██  ███████   ██▄▄▄▄██   ▀ ▄▄▄██  ██▀  ▀██  ██▄▄▄▄██   ██▀     
 ██          ██      ▄██▀▀▀██   ▀▀▀▀██▄  ██    ██  ██  ▀██▄  ██▀▀▀▀▀▀  ▄██▀▀▀██  ██    ██  ██▀▀▀▀▀▀   ██      
 ██          ██▄▄▄   ██▄▄▄███  █▄▄▄▄▄██  ██    ██  ██    ██  ▀██▄▄▄▄█  ██▄▄▄███  ███▄▄██▀  ▀██▄▄▄▄█   ██      
 ▀▀           ▀▀▀▀    ▀▀▀▀ ▀▀   ▀▀▀▀▀▀   ▀▀    ▀▀  ▀▀    ▀▀▀   ▀▀▀▀▀    ▀▀▀▀ ▀▀  ██ ▀▀▀      ▀▀▀▀▀    ▀▀      
                                                                                 ██
'''.strip()

def firmwareUpload(board):
	console.print("[bold green](@)[/] [blink cyan]Сompilation...[/]")
	result = subprocess.run(board[0], stdout=subprocess.PIPE)
	console.print(Panel.fit(result.stdout.decode('utf-8').strip()))
	console.print("[bold green](@)[/] [cyan]End compillation.[/]")

	console.print("[bold green](@)[/] [blink cyan]Uploading...[/]")			
	result = subprocess.run(board[1], stdout=subprocess.PIPE)
	console.print(Panel.fit(result.stdout.decode('utf-8').strip()))
	console.print("[bold green](@)[/] [cyan]End uploading.[/]")

def loadPlugin(plugin_path):
	spec = importlib.util.spec_from_file_location("plugin", plugin_path)
	serial_module = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(serial_module)

	return serial_module

def listFirmware():
	firmwareList = {}
	with os.scandir("firmware") as it:
		for entry in it:
			if entry.is_dir():
				file = open(f"firmware\\{entry.name}_Description.txt", 'r')
				description = file.read()
				file.close()

				firmwareList[entry.name] = description

				return firmwareList

def listPlugins():
	pluginList = {}
	with os.scandir("plugins") as it:
		for entry in it:
			if entry.name.endswith('.py'):
				file = open(f"plugins\\{entry.name.replace('.py', '')}_Description.txt", 'r')
				description = file.read()
				file.close()

				pluginList[entry.name.replace('.py', '')] = description

	return pluginList


def main():
	try:
		console.print(Panel.fit(logo, subtitle="Welcome to FlashReaper v.1.0", subtitle_align='left'), style='bold green')
		console.print(
		Panel.fit('''
1. Print COM ports 
2. Show available firmware
3. Upload firmware
4. Serial monitoring
5. Serial plugins'''.lstrip(), box=box.ASCII))

		while True:
			userInput = console.input("\n[bold green]#select#> ")

			if userInput == "1":
				result = subprocess.run(["arduino-cli", "board", "list"], stdout=subprocess.PIPE)
				console.print(Panel.fit(result.stdout.decode('utf-8').strip()))

			if userInput == "2":
				firmwareList = listFirmware()

				for firm, desc in firmwareList.items():
					console.print(Panel.fit(f"[bold green]|#|[/] [bold magenta]{firm}[/]: [bold cyan]{desc}[/]"))

			if userInput == "3":
				firmware = console.input("\n[bold green]#select firmware#> ")
				firmwareName = firmware.split('.')
				COM_Port = console.input("\n[bold green]#select COM port#> ")

				esp8266_uploading = [["arduino-cli", "compile", 
									"--fqbn", "esp8266:esp8266:nodemcuv2", 
									f"firmware\\{firmware}\\{firmware}.ino"], 
							["arduino-cli", "upload", "-p", COM_Port, 
									"--fqbn", "esp8266:esp8266:nodemcuv2", 
									f"firmware\\{firmware}\\{firmware}.ino"]]

				arduinoUno_uploading = [["arduino-cli", "compile", 
									"--fqbn", "arduino:avr:uno", 
									f"firmware\\{firmware}\\{firmware}.ino"],
								["arduino-cli", "upload", "-p", COM_Port, 
									"--fqbn", "arduino:avr:uno", 
									f"firmware\\{firmware}\\{firmware}.ino"]]

				if firmwareName[1] == "Esp8266": firmwareUpload(esp8266_uploading)
				elif firmwareName[1] == "ArduinoUno": firmwareUpload(arduinoUno_uploading)
				elif firmwareName[1] == "4all":
					boardName = console.input("Select your board ([bold green]Esp8266, ArduinoUno, etc.[/]): ")

					if boardName == "Esp8266": firmwareUpload(esp8266_uploading)
					elif boardName == "ArduinoUno": firmwareUpload(arduinoUno_uploading)

			if userInput == "4":
				COM_Port = console.input("\n[bold green]#select COM port#> ")
		
				console.print(Panel.fit("1. Standart (only data receiving)\n2. Load plugin", 
								style='bold green', title='modes', title_align='center', box=box.ASCII))
		
				mode = console.input("\n[bold green]#select mode#> ")

			
				if mode == "1":
					try:
						ser = serial.Serial(COM_Port, 115200)
					
					except serial.SerialException as e:
						console.print("\n[bold red](!)[/] [cyan]Serial error. See traceback.[/]")
						print(e)
						console.input("[bold green]\nPress enter to continue...[/]")
						break
					
					console.print("\n[bold green]($)[/] [cyan]Waiting for data...[/]")

					while True:
						try:
							if ser.in_waiting > 0:
								data = ser.readline().decode('utf-8', errors='replace').strip()
								console.print(Panel.fit(data, title='Data', title_align='center'))
						except serial.SerialException as e:
							console.print("\n[bold red](!)[/] [cyan]Serial error. See traceback.[/]")

				if mode == "2":
					pluginPath = 'plugins\\'+console.input("\n[bold green]#select plugin#> ")+'.py'

					plugin = loadPlugin(pluginPath)

					print('\n')
					console.print(Panel.fit(plugin.info(), 
									style='bold green', title='Plugin info', title_align='center'))
					print('\n')
					plugin.start(COM_Port)

					console.print("\n[bold green](@)[/] [cyan]Plugin end[/]")


			if userInput == "5":
				pluginList = listPlugins()

				for plug, desc in pluginList.items():
					console.print(Panel.fit(f"[bold green]|#|[/] [bold magenta]{plug}[/]: [bold cyan]{desc}[/]"))


	except Exception as e:
		console.print(f"[bold red]An critical error occured:[/] {e}")
		console.input("[bold green]\nPress enter to continue...[/]")

if __name__ == "__main__":
	while True:
		try:
			main()
		except KeyboardInterrupt:
			console.print("\n[yellow](X)[/] [cyan]EXIT...[/]")
			break
