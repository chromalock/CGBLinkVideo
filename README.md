# gb-link-video

Playing media on a gameboy color over the link cable, with the help of an [RP2040](https://www.raspberrypi.com/products/rp2040/)

# System Requirements
- Linux (MacOS may work)
  - Open to PRs adding windows support
- Python 3.6+
- FFMpeg

# Hardware Requirements
- Gameboy Color + Link Cable
- Raspberry PI Pico
- GBLink Board (or some other method of level shifting)
- Flash Cartridge

# Conceptual Overview

```
| PC | <--UART--> | RPi Pico + GBLink Board | <--PIO--> | Gameboy Color | 
```

PC Handles video encoding, then sends the encoded data to the RPi pico over UART, which is stored in a buffer (may be double buffered). 
This happens at roughly 1Mbps.

Meanwhile, the Gameboy color makes requests to the RPi Pico over its serial port, with the voltage levels being shifted by the GBLink board.
The PIO handle the job of parsing these signals and shifting data out to the gameboy.

# Repo Structure

You can find more detailed information on the individual components in the following locations:

```
/pico/ | Firmware + PIO programs for an RP2040/RPi Pico (W)
/rom/  | Gameboy Color ROMs
/py/   | Python package + scripts for streaming data to the gameboy color 
/pcb/  | Schematics, PCB designs, and gerber files for the GBLink board.
```

# Usage

# Explanation Video
