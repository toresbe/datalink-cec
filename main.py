import cec
import serial

cec.init()

ser = serial.Serial('/dev/ttyACM1', 230400)
tv = cec.Device(cec.CECDEVICE_TV)

def send_remote_code(codes):
    cec.transmit(cec.CECDEVICE_PLAYBACKDEVICE1, 0x44, codes)
    cec.transmit(cec.CECDEVICE_PLAYBACKDEVICE1, 0x45)

BEO4_TV = b'00000000010000000'
BEO4_LEFT = b'00000000000110010'
BEO4_RIGHT = b'00000000000110100'
BEO4_UP = b'00000000000011110'
BEO4_DOWN = b'00000000000011111'
BEO4_GO = b'00000000000110101'
BEO4_STANDBY = b'00000000000001100'
BEO4_STOP = b'00000000000110110'
BEO4_MENU = b'00000000001011100'
BEO4_EXIT = b'00000000001111111'

handlers = {
        BEO4_TV: tv.power_on,
        BEO4_STANDBY: tv.standby,
        BEO4_RIGHT: lambda: send_remote_code(b'\x04'),
        BEO4_LEFT: lambda: send_remote_code(b'\x03'),
        BEO4_DOWN: lambda: send_remote_code(b'\x02'),
        BEO4_UP: lambda: send_remote_code(b'\x01'),
        BEO4_GO: lambda: send_remote_code(b'\x00'),
        BEO4_STOP: lambda: send_remote_code(b'\x46'),
        BEO4_MENU: lambda: send_remote_code(b'\x09'),
        BEO4_EXIT: lambda: send_remote_code(b'\x0d'),
}

while True:
    stx, data, etx = ser.readline().split(b" ")
    print(data)
    handler = handlers.get(data)
    if handler:
        handler()
