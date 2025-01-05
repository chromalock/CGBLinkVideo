# firmware

```bash
/pico/      # code to be flashed to an rpi pico (USE THIS ONE)
/pico-old/  # old code kept around for archival reasons. not compatible with the current scripts.
```

# Flashing

You will need the [Arduino IDE](https://www.arduino.cc/en/software) and the [RPi Pico Core](https://github.com/earlephilhower/arduino-pico),
as well as the [Serial Transfer](https://github.com/PowerBroker2/SerialTransfer) arduino library, which can be installed through the Arduino IDE.


Assuming you have a GBLink PCB and the dependencies installed, the process is simple:
1. Connect the RPi Pico to the computer via USB
2. Open the `/pico/pico.ino` sketch in the Arduino IDE
3. Unless you have other serial devices connected, the RPi pico should be the only option available in the dropdown next to the upload button. Select the port and set it as `Raspberry RPi Pico` (If you do not see this option, you need to install the core like outlined above)
4. Upload 

WARNING: Do not open the serial monitor while in the arduino ide. No debug information is provided and this will block any scripts from communicating.