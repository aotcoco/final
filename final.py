from pyfingerprint.pyfingerprint import PyFingerprint
import time
import sys

def initialize_sensor():
    """Initializes the fingerprint sensor on serial0."""
    try:
        sensor = PyFingerprint('/dev/serial0', 57600, 0xFFFFFFFF, 0x00000000)

        if not sensor.verifyPassword():
            raise ValueError('Wrong sensor password!')

        print('✅ Sensor initialized successfully.')
        print('📦 Stored templates:', sensor.getTemplateCount())
        print('🧠 Available storage slots:', sensor.getStorageCapacity())
        return sensor

    except Exception as e:
        print('❌ Failed to initialize sensor.')
        print('💥 Error:', str(e))
        sys.exit(1)

def search_fingerprint(sensor):
    """Searches for a fingerprint match."""
    try:
        print('\n👉 Waiting for finger...')

        while not sensor.readImage():
            time.sleep(0.1)

        print('🖼️ Fingerprint image captured.')

        sensor.convertImage(0x01)
        result = sensor.searchTemplate()

        position_number = result[0]
        accuracy_score = result[1]

        if position_number >= 0:
            print(f'✅ Match found at ID #{position_number}')
            print(f'🎯 Accuracy score: {accuracy_score}')
        else:
            print('❌ No match found.')

    except Exception as e:
        print('💥 Error during fingerprint scan:', str(e))

if _name_ == '_main_':
    sensor = initialize_sensor()
    while True:
        search_fingerprint(sensor)
        print('\n⏳ Scan again in 3 seconds...')
        time.sleep(3)