import time
import sys
from pyfingerprint.pyfingerprint import PyFingerprint

def initialize_sensor():
    """Initialize the fingerprint sensor."""
    try:
        sensor = PyFingerprint('/dev/serial0', 57600, 0xFFFFFFFF, 0x00000000)

        if not sensor.verifyPassword():
            raise ValueError('The fingerprint sensor password is incorrect.')

        print('\n✅ Fingerprint sensor initialized.')
        print(f'📦 Templates stored: {sensor.getTemplateCount()}')
        print(f'🧠 Capacity: {sensor.getStorageCapacity()}')
        return sensor

    except Exception as e:
        print('❌ Initialization error:', e)
        sys.exit(1)

def scan_fingerprint(sensor):
    """Scan a fingerprint and search for a match."""
    try:
        print('\n👉 Place your finger on the sensor...')

        while not sensor.readImage():
            time.sleep(0.1)

        print('🖼️ Image captured.')
        sensor.convertImage(0x01)
        result = sensor.searchTemplate()
        position, accuracy = result

        if position >= 0:
            print(f'✅ Match found! ID #{position}, Accuracy: {accuracy}')
        else:
            print('❌ No match found.')

    except Exception as e:
        print('💥 Scan error:', e)

# 🚀 NEW LOGIC: Runs immediately
sensor = initialize_sensor()
while True:
    scan_fingerprint(sensor)
    time.sleep(3)
