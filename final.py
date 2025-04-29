from pyfingerprint.pyfingerprint import PyFingerprint
import time
import sys

def initialize_sensor():
    """Initializes the AS608 fingerprint sensor using UART (/dev/serial0)."""
    try:
        sensor = PyFingerprint('/dev/serial0', 57600, 0xFFFFFFFF, 0x00000000)

        if not sensor.verifyPassword():
            raise ValueError('Wrong fingerprint sensor password!')

        print('\n✅ Fingerprint sensor initialized successfully.')
        print(f'📦 Stored templates: {sensor.getTemplateCount()}')
        print(f'🧠 Storage capacity: {sensor.getStorageCapacity()}')
        return sensor

    except Exception as e:
        print('\n❌ Failed to initialize sensor.')
        print(f'💥 Error: {e}')
        sys.exit(1)

def search_fingerprint(sensor):
    """Captures and searches for a fingerprint match."""
    try:
        print('\n👉 Place your finger on the sensor...')

        # Wait until a finger is placed
        while not sensor.readImage():
            time.sleep(0.1)

        print('🖼️ Fingerprint image captured.')

        # Convert image to template
        sensor.convertImage(0x01)

        # Search for a match
        result = sensor.searchTemplate()
        position_number, accuracy_score = result

        if position_number >= 0:
            print(f'✅ Match found! Template ID: {position_number}')
            print(f'🎯 Accuracy score: {accuracy_score}')
        else:
            print('❌ No match found.')

    except Exception as e:
        print('💥 Error during fingerprint matching:')
        print(f'⚠️ {e}')

# ✅ Corrected block to run the main logic
if _name_ == '_main_':
    sensor = initialize_sensor()
    while True:
        search_fingerprint(sensor)
        print('\n⏳ Ready for next scan in 3 seconds...')
        time.sleep(3)