# roms

ROM files for a gameboy color to decode data sent through the GBLink.

```bash
/stream/  # Video decoding ROMs
/test/    # Files to test link cable + GBLink
/demos/   # Demo ROMs
/shared/  # Shared routines
```

You can find the built ROM files [here](https://github.com/chromalock/CGBLinkVideo/releases/tag/1.0) if you don't want to make any modifications of your own.

# Build Requirements

You need the [RGBDS](https://github.com/gbdev/rgbds) build system if you want to build the ROMs.
You will also need `make`.

# Build

To build all the ROMs:

```bash
# builds all roms in all subdirectories
make all
# results will be in /roms/out/
```

To remove all build files and ROMs (if you need to):

```bash
# remove all build files
make clean
```

# ROM Descriptions

```bash
# Serial Test ROMS
high-speed.gbc        # periodically send a value at 512khz
med-speed.gbc         # periodically send a value at 16khz
low-speed.gbc         # periodically send a value at 8khz

td2018.gbc            # bw stream
td2018-vsync.gbc      # bw stream, but with larger transfers to reduce tearing

tdc2018.gbc           # color stream
tdc2018-vsync.gbc     # color stream, but with larger transfers to reduce tearing

tile-index.gbc        # the low-res stream that sends a new tilemap every frame
```