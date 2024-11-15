; Video Stream for WiFi Game Boy Cartridge

DEF READY_STATUS = 3
DEF READY_ACK = 2
DEF BYTE_ACK = 4
DEF CHANNELS = 1
DEF COLS = 20
DEF ROWS = 18
DEF VIDEO_BYTES = COLS*ROWS
DEF COL_START = 0
DEF ROW_START = 0

SECTION	"start",ROM0[$0100]
    nop
    jp	begin


 DB $CE,$ED,$66,$66,$CC,$0D,$00,$0B,$03,$73,$00,$83,$00,$0C,$00,$0D
 DB $00,$08,$11,$1F,$88,$89,$00,$0E,$DC,$CC,$6E,$E6,$DD,$DD,$D9,$99
 DB $BB,$BB,$67,$63,$6E,$0E,$EC,$CC,$DD,$DC,$99,$9F,$BB,$B9,$33,$3E

 DB "BADAPPLE",0,0,0,0,0,0,0  ; Cart name - 15bytes
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

MACRO WaitForMode
	ld	c, $41
	.waitMode\@:
		ldh	a, [c]
		and	a, %00000011
		cp  a, \1
    jr	nz, .waitMode\@
	ENDM

MACRO TransferByte
	; load byte for sending
	ld [$ff01], a
	; initiate transfer
	ld a, $80
	ld [$ff02], a
	; wait for confirmation
.serial_wait\@:
	ld a, [$ff02]
	and $80
	jr nz, .serial_wait\@
	ld a, [$ff01]
ENDM

MACRO LCDON
ld	a, %10010001	;LCD on, BG Tile Data 0x8000, BG ON
ld	[$ff40], a
ENDM

MACRO LCDOFF
ld	a, %00010001	;LCD off, BG Tile Data 0x8000, BG ON
ld	[$ff40], a
ENDM

begin:
  ; no interrupts needed
	di

	; Enter Double-speed mode
	ld a, 1
	ld [$ff4d], a
	stop

	LCDOFF

	; setup serial (external clock)
	ld a, 0
	ld [$ff02], a

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

; set tile indexes (0-256 for debugging)
	ld a, $ff
DEF LINEADDR = $9800+(COL_START)+(ROW_START*32)
REPT ROWS
  ld	hl, LINEADDR
	DEF LINEADDR = LINEADDR + 32
	REPT COLS
		ld [hli], a
		dec a
	ENDR
ENDR

; turn lcd on and start serial data loop
	LCDON
loop:
; notify nano that we're ready for the next frame
nano_notify:
	ld a, READY_STATUS
	TransferByte
	cp a, READY_ACK
	jr nz, nano_notify

; load all tile indexes over serial into buffer
	ld hl, TILE_BUFFER
REPT VIDEO_BYTES
	ld a, BYTE_ACK
	TransferByte
	ld [hli], a
ENDR


	; TODO DMA 
	; wait for a vblank
	WaitForMode %00000001	


; copy tile map buffer into actual map 
; NOTE: this code must take less time than the 
; VBlank period in order to work (which it does)
ld de, TILE_BUFFER
DEF LINEADDR = $9800+(COL_START)+(ROW_START*32)
REPT ROWS
  ld	hl, LINEADDR
	DEF LINEADDR = LINEADDR + 32
	REPT COLS
		ld a, [de]
		ld [hli], a
		inc de
	ENDR
ENDR


	jp	loop


TILES:
INCBIN "./tiles.2bpp"

SECTION "RAM", WRAM0[$C000]
TILE_BUFFER: DS VIDEO_BYTES