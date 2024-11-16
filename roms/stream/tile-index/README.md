# tile-index

Video decoder that uses a pre-generated tileset.

## How It Works

Every frame, the gameboy will perform the following actions:

Send `0x00` at the start of a frame.

Send `0xff` 360 times to retrieve all the bytes. 