ASM	= rgbasm
LINK = rgblink
FIX = rgbfix

BINS	= tile-data-20x18.gbc

all:	$(BINS)

compile.bat: Makefile
	@echo "REM Automatically generated from Makefile" > compile.bat
	@make -sn | sed y/\\//\\\\/ | grep -v make >> compile.bat

# Compile and link single file in one pass
%.gbc:	%.asm
	$(ASM) -o $@.o $<
	$(LINK) -t -w -o $@ -n $@.sym $@.o
	$(FIX) -v -C -p 0 $@

clean:
	rm -f *.o *.lst *.map *.gb *~ *.rel *.cdb *.ihx *.lnk *.sym *.noi *.gbc