# FlashReaper v1.0
 FlashReaper - python firmware uploader for arduino/ESP boards
 ## Features
 - **Interactive menu system**
 - **Custom firmware support**
 - **Custom COM plugin support**
 - **COM ports detection**
 - **Serial port monitoring**
 - **One-click flashing**
 -  **Easy UI**
 ## Supported Boars
 - Arduino (Uno)
 -  Esp8266 (NodeMCU)
 ## Quick Start
 ### Prerequisites
 - Python 3.8 or higher
 - Arduino CLI installed
- Supported development  board
### Installation
```bash
# Clone the repository
git clone https://github.com/EyeHateY0u/FlashReaper.git
cd FlashReaper

# Install python dependencies
pip install -r requirements.txt
```
### Arduino CLI Setup
```
# Inititalize and configure Arduino CLI
arduino-cli config init
aurdino-cli core update-index

# Install supported cores
arudino-cli core install esp8266:esp8266
arduino-cli core install arduino:avr
```
### Usage 
`python FlashReaper.py`

## Details
- Language: Python 3.8+
-  Key Librarires: pyserial, rich
- Build System: Arduino CLI
- Serial Protocol: 115200 baud
## How to Use
#### Launch Application
`python FlashReaper.py`
#### Discover Ports
- Select 1 to view avaliable serial devices
- Note your board's COM port number
#### Browse Firmware
- Select 2 to view avaliable sketches
- Choose from pre-buit examples or add your own
#### Flash Board
- Select 3 to start 
-  Select firmware
-  Input COM port
-  Wait.
- #### Work with Serial Port
- Select 4 to start
- Input COM port
- Select mode (Standart or plugin)
# Author
**EyeHateY0u a.k.a D0pef1end**
- Github: @eyehatey0u
- Project Link: https://github.com/EyeHateY0u/FlashReaper
## If you find this project useful, please give it a star!