INCLUDE "../../shared/util.asm"

DEF COLS = 20
DEF ROWS = 18
DEF BYTES = COLS*ROWS*16
DEF COL_START = 0
DEF ROW_START = 0

SECTION	"Org $00",ROM0[$00]
RST_00:	
	jp	$100

	SECTION	"Org $08",ROM0[$08]
RST_08:	
	jp	$100

	SECTION	"Org $10",ROM0[$10]
RST_10:
	jp	$100

	SECTION	"Org $18",ROM0[$18]
RST_18:
	jp	$100

	SECTION	"Org $20",ROM0[$20]
RST_20:
	jp	$100

	SECTION	"Org $28",ROM0[$28]
RST_28:
	jp	$100

	SECTION	"Org $30",ROM0[$30]
RST_30:
	jp	$100

	SECTION	"Org $38",ROM0[$38]
RST_38:
	jp	$100

; reset to 8000 index addressing at start of frame
SECTION "VBLANK IRQ",ROM0[$40]
	jp vblank_irq

; change to 8800 index addressing in the middle of the frame
SECTION "LCD IRQ",ROM0[$48]
	jp lcd_irq

SECTION	"Serial IRQ Vector",ROM0[$58]
	reti

SECTION	"Joypad IRQ Vector",ROM0[$60]
	reti

SECTION	"start",ROM0[$0100]
    nop
    jp	begin


DB $CE,$ED,$66,$66,$CC,$0D,$00,$0B,$03,$73,$00,$83,$00,$0C,$00,$0D
DB $00,$08,$11,$1F,$88,$89,$00,$0E,$DC,$CC,$6E,$E6,$DD,$DD,$D9,$99
DB $BB,$BB,$67,$63,$6E,$0E,$EC,$CC,$DD,$DC,$99,$9F,$BB,$B9,$33,$3E

DB "LINKVIDEO",0,0,0,0,0,0   ; Cart name - 15bytes
DB $C0                       ; $143 - CGB support
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

lcd_irq:
	push af
	LCDON_BANK1
	pop af
	reti

vblank_irq:
	push af
	LCDON_BANK0
	pop af
	reti

begin:  
	; no interrupts needed
	di
	
	; Enter Double-speed mode
	DoubleSpeed

	; wait for a vblank
	WaitVBlank
	LCDOFF

	; enable auto-increment
	ld a, $80
	ld [$ff68], a

	; load black as our first color
	ld a, $00
	ld [$ff69], a
	ld [$ff69], a

	; dark grey
	ld a, %11001110
	ld [$ff69], a
	ld a, %00111001
	ld [$ff69], a

	; light grey
	ld a, %11010110
	ld [$ff69], a
	ld a, %01011010
	ld [$ff69], a

	; white
	ld a, $ff
	ld [$ff69], a
	ld [$ff69], a

  ; Set scroll registers to zero
	ld	a, 0
	ld	[$FF42], a
	ld	[$FF43], a

	; zero out all tiles
	ld hl, $8000
	ld b, $ff
	ld a, 0
zero_tile_data:
REPT 24
	ld [hli], a
ENDR
	dec b
	jp nz, zero_tile_data

	; set up tilemap with 0-256
	ld a, 0
DEF LINEADDR = $9800+(COL_START)+(ROW_START*32)
REPT ROWS
  ld	hl, LINEADDR
	DEF LINEADDR = LINEADDR + 32
	REPT COLS
		ld [hli], a
		inc a
	ENDR
ENDR

	; enable lcd interrupt + vblank interrupt
	ld a, %0000_0011
	ld [$ffff], a

	; LYC=LY compare, 
	ld a, 80
	ld [$ff45], a

	; STAT=LYC int
	ld a, %0100_0000
	ld [$ff41], a

	; clear out any residual values
	xor a, a
	ld [$ff0f], a
	
	ei

	VRAMBank 0

	LCDON

	; Wait for start of next frame
	WaitVBlank
	WaitVBlankEnd

loop:
	; if any buttons are pressed we need to go into a waiting state
	; so that the PIO can reset and sync to the bitstream
	ld a, %00100000
	ld [$ff00], a
	; youre just supposed to read it a bunch fuck me idk
	ld a, [$ff00]
	ld a, [$ff00]
	ld a, [$ff00]
	ld a, [$ff00]
	and %00000001
	jr z, loop

	; wait for end of a vblank
	WaitVBlank

	; sync to start of frame
	ld a, $00
	TransferByteInternalFast

	; i have no clue why i need this, i might not need to, who knows
	ld a, $ff
	TransferByteInternalFast

	; This is going to take 5 frames
	
	Transfer1024 $C000
	WaitVBlankEnd
	WaitVBlank
	DMA $C000, $8000, %0_011_1111
	WaitDMA

	Transfer1024 $C000
	WaitVBlankEnd
	WaitVBlank
	DMA $C000, $8400, %0_011_1111
	WaitDMA

	Transfer1024 $C000
	WaitVBlankEnd
	WaitVBlank
	DMA $C000, $8800, %0_011_1111
	WaitDMA

	Transfer1024 $C000
	WaitVBlankEnd
	WaitVBlank
	DMA $C000, $8C00, %0_011_1111
	WaitDMA

	; Transfer the last 1664 (104 tiles)
	Transfer1664 $C000
	WaitVBlankEnd
	WaitVBlank
	DMA $C000, $9000, %0_110_0111
	WaitDMA

	jp	loop

SECTION "RAM", WRAM0[$C000]
TILE_DATA: DS 2048