# gbstream.py

A program and library for sending data to a gameboy color through GBLink.

# Installation

```bash
pip install -r ./requirements.txt
```

# Usage

```bash
python gbstream.py -p /dev/ttyACM0 -b 921600 -i ./video.mp4   # take input from stdin
python gbstream.py -p /dev/ttyACM0 -b 921600 -i -             # take input from stdin
```

```bash
usage: gbstream.py [-h] -p PORT [-b BAUD] [-i INPUT]

options:
  -h, --help            show this help message and exit
  -p PORT, --port PORT
  -b BAUD, --baud BAUD
  -i INPUT, --input INPUT
```