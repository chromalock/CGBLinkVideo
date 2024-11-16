; b needs to contain $80
; c needs to contain $02
MACRO TransferByteFast
	; initiate transfer 
	ld a, b									; 1
	ldh [c], a							; 2
	; wait for confirmation
	; TODO could this be replaced with a certain # of nops?
.serial_wait\@:
	ldh a, [c]							; 2
	and b										; 1
	jr nz, .serial_wait\@		; 2-3
	ldh a, $01							; 3
ENDM

; 12 m cycles
; requires register b to contain `$80`
; requires register c to contain `$02`

; CHANGES
; makes it "read-only", cannot send bytes 
; uses the `ldh` instruction more 