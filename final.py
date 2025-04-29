import time
import board
import busio
from adafruit_fingerprint import Adafruit_Fingerprint

# Initialize UART on GPIO14 (TX) and GPIO15 (RX)
uart = busio.UART(board.TX, board.RX, baudrate=57600)

# Initialize the sensor
finger = Adafruit_Fingerprint(uart)

def get_fingerprint():
    print("Waiting for finger...")
    while finger.get_image() != Adafruit_Fingerprint.OK:
        pass

    if finger.image_2_tz(1) != Adafruit_Fingerprint.OK:
        return False

    if finger.finger_search() != Adafruit_Fingerprint.OK:
        return False

    print("Found fingerprint!")
    print("Fingerprint ID:", finger.finger_id)
    print("Confidence:", finger.confidence)
    return True

if _name_ == "_main_":
    while True:
        try:
            if get_fingerprint():
                print("Access granted.")
            else:
                print("No match found.")
        except Exception as e:
            print("Error:", e)
        time.sleep(2)