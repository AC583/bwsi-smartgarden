import RPi.GPIO as GPIO
import time

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin for the relay controlling the water pump
RELAY_PIN = 25

# Set up the relay pin as an output
GPIO.setup(RELAY_PIN, GPIO.OUT)

try:
    # Turn on the relay (activate the water pump)
    print("Activating the water pump...")
    GPIO.output(RELAY_PIN, GPIO.HIGH)  # Turn on the relay
    time.sleep(5)  # Keep the pump on for 5 seconds

    # Turn off the relay (deactivate the water pump)
    print("Deactivating the water pump...")
    GPIO.output(RELAY_PIN, GPIO.LOW)  # Turn off the relay

finally:
    # Clean up the GPIO settings
    GPIO.cleanup()
    print("Test complete. GPIO cleaned up.")