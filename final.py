from pyfingerprint.pyfingerprint import PyFingerprint
import time
import sys

def initialize_sensor():
    """Initializes the AS608 fingerprint sensor using /dev/serial0."""
    try:
        sensor = PyFingerprint('/dev/serial0', 57600, 0xFFFFFFFF, 0x00000000)

        if not sensor.verifyPassword():
            raise ValueError('Wrong fingerprint sensor password!')

        print('\n✅ Fingerprint sensor initialized')
        print('📦 Stored templates :', sensor.getTemplateCount())
        print('🧠 Storage capacity :', sensor.getStorageCapacity())
        return sensor

    except Exception as e:
        print('\n❌ Sensor initialization failed')
        print('💥 Error:', str(e))
        sys.exit(1)

def search_fingerprint(sensor):
    """Captures and searches for a fingerprint match."""
    try:
        print('\n👉 Place your finger on the sensor...')

        # Wait until a finger is placed
        while not sensor.readImage():
            time.sleep(0.1)

        print('🖼️ Fingerprint image captured.')

        # Convert the image to a template
        sensor.convertImage(0x01)

        # Search the template
        result = sensor.searchTemplate()

        position_number = result[0]
        accuracy_score = result[1]

        if position_number >= 0:
            print(f'✅ Match found! Template ID: {position_number}')
            print(f'🎯 Accuracy score: {accuracy_score}')
        else:
            print('❌ No match found.')

    except Exception as e:
        print('💥 Failed to process fingerprint:')
        print('Error:', str(e))

if _name_ == '_main_':
    sensor = initialize_sensor()
    while True:
        search_fingerprint(sensor)
        print('\n⏳ Ready for next scan in 3 seconds...\n')
        time.sleep(3)