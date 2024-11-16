; Video Stream for WiFi Game Boy Cartridge

SECTION	"start",ROM0[$0100]
    nop
    jp	begin

 DB $CE,$ED,$66,$66,$CC,$0D,$00,$0B,$03,$73,$00,$83,$00,$0C,$00,$0D
 DB $00,$08,$11,$1F,$88,$89,$00,$0E,$DC,$CC,$6E,$E6,$DD,$DD,$D9,$99
 DB $BB,$BB,$67,$63,$6E,$0E,$EC,$CC,$DD,$DC,$99,$9F,$BB,$B9,$33,$3E

 DB "LINKTEST",0,0,0,0,0,0,0  ; Cart name - 15bytes
 DB $C0                       ; $143 - CGB support (supports both)
 DB 0,0                       ; $144 - Licensee code
 DB 0                         ; $146 - SGB Support indicator
 DB $02                       ; $147 - Cart type
 DB $00                       ; $148 - ROM Size
 DB $02                       ; $149 - RAM Size
 DB 1                         ; $14a - Destination code
 DB $33                       ; $14b - Old licensee code
 DB 0                         ; $14c - Mask ROM version
 DB 0                         ; $14d - Complement check
 DW 0                         ; $14e - Checksum


INCLUDE "../../shared/util.asm"

begin:
  ; no interrupts needed
	di

	LCDOFF

; turn lcd on and start serial data loop
	LCDON
	ld b, $0
loop:
	; send byte
	ld a, b
	TransferByteInternalSlow
	inc b
	; just a delay
REPT 60
	WaitVBlank
	WaitVBlankEnd
ENDR
	jp	loop


SECTION "RAM", WRAM0[$C000]