# CGBLinkVideo

Playing media on a gameboy color over the link cable, with the help of an [RPi Pico](https://www.raspberrypi.com/products/raspberry-pi-pico/)

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/purple_img.png)](https://buymeacoffee.com/contactchrh)

# Inspiration

This project was heavily inspired by [Staacks/wifi-game-boy-cartridge](https://github.com/Staacks/wifi-game-boy-cartridge), and
borrows utility macros, cartridge headers, and some random python snippets.

# Repo Structure

You can find more detailed information on the individual components in the following locations:

```
/firmware/  |   Firmware + PIO programs for an RPi Pico (W)
/pcb/       |   Schematics, PCB designs, and gerber files for the GBLink board.
/roms/      |   Gameboy Color ROMs
/scripts/   |   Python package + scripts for streaming data to the gameboy color 
/stream/    |   Wrapper scripts for hooking up video sources to the gameboy script
```

# System Requirements
```
- Python 3  (3.10.12 for me)
- FFMpeg    (4.4.2-0ubuntu0.22.04.1 for me)
- RGBASM    (v0.7.0-37-gc70cecc2 for me)        <-- only if you want to build the roms yourself
```

# Hardware Requirements
```
- Gameboy Color + Link Cable
- Raspberry PI Pico
- GBLink Board (or some other method of level shifting)
- GBC Flash Cartridge
```

# Conceptual Overview

```
| PC | <--UART--> | RPi Pico + GBLink Board | <--PIO--> | Gameboy Color | 
```

PC Handles video encoding, then sends the encoded data to the RPi pico over UART, which is stored in a buffer (triple buffered). 
This happens at roughly 1Mbps.

Meanwhile, the Gameboy color makes requests to the RPi Pico over its serial port, with the voltage levels being shifted by the GBLink board.
The PIO handle the job of parsing these signals and shifting data out to the gameboy.

# Explanation Video


[![I Streamed To A Game Boy](https://img.youtube.com/vi/yPI6gURLLUs/0.jpg)](https://www.youtube.com/watch?v=yPI6gURLLUs)


# Getting Started

TODO