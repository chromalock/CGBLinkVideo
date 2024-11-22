from pySerialTransfer import pySerialTransfer as transfer
import time

link = transfer.SerialTransfer("/dev/ttyACM0")

link.open()
print("waiting for ")
time.sleep(2)


state = True
while True:
    send_size = 0
    send_size += link.tx_obj(state)
    link.send(send_size, 0)
    print(send_size)
    time.sleep(0.25)
    state = not state
