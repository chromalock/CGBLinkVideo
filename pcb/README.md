# pcb

# Principle Of Operation

3.3V is supplied to the board via the RPi pico, and 5V supplied from the Gameboy Color's link port.\*

Capacitors `C1, C2` are decoupling capacitors.

Diodes `D1, D2` are status LEDs for the 3.3V and 5V power rails, current-limited by `Rx, Ry`.

ICs `U1, U2, U3` are noninverting schmitt-trigger buffers [SN74LVC1G17-Q1](https://www.ti.com/lit/ds/symlink/sn74lvc1g17-q1.pdf?ts=1731651431162).
They increase signal quality and convert between 3.3V and 5V signals on the TX, RX, and Clock lines.


\**Using 5V from the pico results in dropped bits for reasons I am unqualified to answer. Seems to be related to backfeeding into the gameboy.*

# Circuit Diagram

# Limitations

Due to using a unidirectional level shifter on the clock line, the RPi Pico is unable to act as a controller, relying on the gameboy to initiate transactions.
Attempting to use the RPi Pico as a controller could result in shorting the output of the clock level shifter to ground. It would be unlikely that this would damage
the gameboy, but would potentially damage both the GBLink board and the RPi Pico.