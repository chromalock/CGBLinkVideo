; Video Stream for WiFi Game Boy Cartridge

SECTION	"start",ROM0[$0100]
    nop
    jp	begin


DB $CE,$ED,$66,$66,$CC,$0D,$00,$0B,$03,$73,$00,$83,$00,$0C,$00,$0D
DB $00,$08,$11,$1F,$88,$89,$00,$0E,$DC,$CC,$6E,$E6,$DD,$DD,$D9,$99
DB $BB,$BB,$67,$63,$6E,$0E,$EC,$CC,$DD,$DC,$99,$9F,$BB,$B9,$33,$3E

DB "LINKVIDEO",0,0,0,0,0,0   ; Cart name - 15bytes
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
	
	; Enter Double-speed mode
	ld a, 1
	ld [$ff4d], a
	stop

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

	; lighter black
	ld a, %11001110
	ld [$ff69], a
	ld a, %00111001
	ld [$ff69], a

	; lighter-lighter black
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

	; load tiles
	ld hl, $8000
	ld de, TILES
	ld b, $ff
copy_loop:
REPT 16
	ld a, [de]
	ld [hli], a
	inc de
ENDR
	dec b
	jp nz, copy_loop

	LCDON

	; Wait for start of next frame
	WaitVBlank
	WaitVBlankEnd

loop:
	; if any buttons are pressed we need to go into a waiting state
	; so that the PIO can reset and sync to the bitstream
	ld a, %00100000
	ld [$ff00], a
	ld a, [$ff00]
	ld a, [$ff00]
	ld a, [$ff00]
	ld a, [$ff00]
	and %00000001
	jr z, loop

	; wait for end of a vblank
	WaitVBlankEnd

	; sync to start of frame
	ld a, $00
	TransferByteInternalFast

	; i have no clue why i need this
	ld a, $ff
	TransferByteInternalFast

	; load all tile indexes over serial into buffer
DEF LINEADDR = $C000
REPT 18
	ld	hl, LINEADDR
	DEF LINEADDR = LINEADDR + 32
	REPT 20
		ld a, $ff
		TransferByteInternalFast
		ld [hli], a
	ENDR
ENDR

	; wait for a vblank
	WaitVBlank

	; Configure DMA
	
	; Source
	ld a, $C0
	ld [$ff51], a		; source high = $C0
	ld a, $00
	ld [$ff52], a		; source low = $00

	; Destination (0x9800)
	ld a, $98
	ld [$ff53], a
	ld a, $00
	ld [$ff54], a

	; Start general dma, 1024 bytes
	ld a, %0_011_1111
	ld [$ff55], a

	; wait for dma to complete
dma_active_loop:
	ld a, [$ff55]
	and $80
	jr z, dma_active_loop

	jp	loop


TILES:
INCBIN "../../shared/tiles.2bpp"


SECTION "RAM", WRAM0[$C000]
TILE_BUFFER: DS 1024				; this has to be 1024 bytes because the tilemap 
														; is 32x32 even though we only see 20x18