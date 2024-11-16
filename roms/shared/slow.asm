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

; 27 m cycles
