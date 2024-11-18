MACRO WaitForMode
	ld	c, $41
	.waitMode\@:
		ldh	a, [c]
		and	a, %00000011
		cp  a, (\1)
    jr	nz, .waitMode\@
	ENDM

MACRO WaitVBlank
	WaitForMode %00000001
ENDM

MACRO WaitVBlankEnd
	WaitForMode %00000011
ENDM

MACRO SerialWait
.serial_wait\@:
	ld a, [$ff02]
	and $80
	jr nz, .serial_wait\@
ENDM

MACRO TransferByteExternal
	; load byte for sending
	ld [$ff01], a
	; initiate transfer
	ld a, $80
	ld [$ff02], a
	; wait for confirmation
	SerialWait
	ld a, [$ff01]
ENDM

MACRO TransferByteInternalFast
	; load byte for sending
	ld [$ff01], a
	; initiate transfer (internal clock, high speed)
	ld a, $83
	ld [$ff02], a
	; wait for confirmation
	SerialWait
	ld a, [$ff01]
ENDM

MACRO WaitDMA
	; wait for dma to complete
.dma_active_loop\@:
	ld a, [$ff55]
	and $80
	jr z, .dma_active_loop\@
ENDM

MACRO DMA
	; Source
	ld a, HIGH(\1)
	ld [$ff51], a
	ld a, LOW(\1)
	ld [$ff52], a

	; Destination
	ld a, HIGH(\2)
	ld [$ff53], a
	ld a, LOW(\2)
	ld [$ff54], a
	
	; Start DMA
	ld a, LOW(\3)
	ld [$ff55], a
ENDM

MACRO TransferByteInternalSlow
	; load byte for sending
	ld [$ff01], a
	; initiate transfer (internal clock, low speed)
	ld a, $81
	ld [$ff02], a
	; wait for confirmation
.serial_wait\@:
	ld a, [$ff02]
	and $80
	jr nz, .serial_wait\@
	ld a, [$ff01]
ENDM

macro Delay
	ld a, $ff
.delay\@:
	dec a
	jr nz, .delay\@ 
ENDM

MACRO LCDON
	ld	a, %10010000	;LCD on, BG Tile Data 0x8000, BG ON
	ld	[$ff40], a
ENDM

MACRO LCDOFF
	ld	a, %00010000	;LCD off, BG Tile Data 0x8000, BG ON
	ld	[$ff40], a
ENDM

MACRO DoubleSpeed
	; Enter Double-speed mode
	ld a, 1
	ld [$ff4d], a
	stop
ENDM

MACRO VRAMBank
	ld a, LOW(\1)
	ld [$ff4f], a
ENDM