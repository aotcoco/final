import time
import sys
from pyfingerprint.pyfingerprint import PyFingerprint

def initialize_sensor():
    """Initialize the fingerprint sensor via UART."""
    try:
        sensor = PyFingerprint('/dev/serial0', 57600, 0xFFFFFFFF, 0x00000000)

        if not sensor.verifyPassword():
            raise ValueError('The fingerprint sensor password is wrong.')

        print('\n✅ Sensor initialized.')
        print(f'📦 Templates stored: {sensor.getTemplateCount()}')
        print(f'🧠 Capacity: {sensor.getStorageCapacity()}')
        return sensor

    except Exception as e:
        print('❌ Initialization error:', e)
        sys.exit(1)

def scan_fingerprint(sensor):
    """Scan and search for a fingerprint match."""
    try:
        print('\n👉 Place your finger on the sensor...')

        while not sensor.readImage():
            time.sleep(0.1)

        print('🖼️ Image captured.')

        sensor.convertImage(0x01)
        result = sensor.searchTemplate()
        position, accuracy = result

        if position >= 0:
            print(f'✅ Match found at ID #{position}, accuracy: {accuracy}')
        else:
            print('❌ No match found.')

    except Exception as e:
        print('💥 Error during scan:', e)

# ✅ Main logic starts here — correctly written
if _name_ == '_main_':
    sensor = initialize_sensor()
    while True:
        scan_fingerprint(sensor)
        time.sleep(3)