# Import necessary libraries
import RPi.GPIO as GPIO
import dht11
import time
import sys

# --- Configuration ---
# Set the GPIO pin connected to the DHT sensor.
# Use the BCM (Broadcom SOC channel) number, not the physical pin number.
# For example, if connected to GPIO 4 (physical pin 7), set to 4.
# You'll need to adjust this based on how you've wired your DHT11 sensor.
GPIO_PIN = 22 # <--- IMPORTANT: Change this to your actual GPIO pin number!

# --- Initialize GPIO ---
GPIO.setwarnings(False) # Disable warnings for GPIO setup
GPIO.setmode(GPIO.BCM)  # Use BCM numbering for GPIO pins
# GPIO.cleanup() # This is generally not recommended in a continuous loop,
                 # but can be used at the end of a script if exiting.

# Create an instance of the DHT11 sensor reader
# Pass the GPIO BCM pin number to the constructor
sensor_instance = dht11.DHT11(pin=GPIO_PIN)

# --- Main script logic ---
def read_dht11():
    """
    Reads temperature and humidity from the DHT11 sensor using the dht11 library.
    """
    print(f"Attempting to read from DHT11 sensor on GPIO pin {GPIO_PIN}...")
    result = sensor_instance.read()

    if result.is_valid():
        print(f"Temperature: {result.temperature:.1f}°C")
        print(f"Humidity: {result.humidity:.1f}%")
        return result.temperature, result.humidity
    else:
        print(f"Failed to retrieve data from DHT sensor. Error code: {result.error_code}")
        print("Common issues: Incorrect wiring, wrong GPIO pin, or sensor not responding.")
        return None, None

if __name__ == "__main__":
    # Before running this script, you need to install the dht11 library
    # and ensure RPi.GPIO is installed.
    # Open your Raspberry Pi's terminal and run these commands:
    #
    # 1. Install RPi.GPIO (usually pre-installed, but good to check/update):
    #    sudo apt-get update
    #    sudo apt-get install python3-rpi.gpio
    #
    # 2. Install the dht11 library:
    #    pip3 install dht11
    #
    # If `pip3` is not found, you might need to install it:
    #    sudo apt-get install python3-pip
    #
    # After installation, you can run this script using:
    #    python3 your_script_name.py

    try:
        while True:
            read_dht11()
            # Wait for a few seconds before reading again.
            # DHT11 typically has a minimum read interval of 1-2 seconds.
            time.sleep(3) # Increased to 3 seconds for robustness
    except KeyboardInterrupt:
        print("\nScript terminated by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
    finally:
        # Clean up GPIO settings when the script exits
        GPIO.cleanup()

