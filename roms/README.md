# roms

ROM files for a gameboy color to decode data sent through the GBLink.

```bash
/stream/  # Video decoding ROMs
/test/    # Files to test link cable + GBLink
/demos/   # Demo ROMs
/shared/  # Shared routines
```

# Build Requirements

You need the [RGBDS](https://github.com/gbdev/rgbds) build system if you want to build the ROMs.
You will also need `make`.

# Build

To build all the ROMs:

```bash
# builds all roms in all subdirectories
make all
```

To remove all build files and ROMs (if you need to):

```bash
# remove all build files
make clean
```