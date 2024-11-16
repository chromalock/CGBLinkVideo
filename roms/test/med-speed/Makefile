ASM	= rgbasm
LINK = rgblink
FIX = rgbfix

BINS	= med-speed.gbc

all:	$(BINS)

# Compile and link single file in one pass
%.gbc:	%.asm
	$(ASM) -o $@.o $<
	$(LINK) -t -w -o $@ -n $@.sym $@.o
	$(FIX) -v -C -p 0 $@

clean:
	rm -f *.o *.lst *.map *.gb *~ *.rel *.cdb *.ihx *.lnk *.sym *.noi *.gbc