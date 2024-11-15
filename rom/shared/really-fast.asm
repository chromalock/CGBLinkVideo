; b needs to contain $80
; c needs to contain $02
MACRO TransferByteReallyFast
	; initiate transfer 
	ld a, b									; 1
	ldh [c], a							; 2
	; todo DELAY heree
	ldh a, $01							; 3
ENDM

; 12 m cycles
; requires register b to contain `$80`
; requires register c to contain `$02`

; CHANGES
; makes it "read-only", cannot send bytes 
; uses the `ldh` instruction more 

; 6 cycles (+ 3ish )