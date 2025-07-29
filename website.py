from flask import Flask, render_template, Response
import requests
import RPi.GPIO as GPIO
import dht11
from smbus2 import SMBus
import time
import Adafruit_ILI9341 as ILI9341
from PIL import Image, ImageDraw, ImageFont
import spidev  # Import the spidev library for SPI communication
import imageCapture
from classify import classify_image  # Import the classify_image function
# Initialize Flask app
app = Flask(__name__)

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Set the GPIO pin number for the DHT11 sensor
DHT_PIN = 22  # Change this to the pin you are using

# Create an instance of the DHT11 class
sensor = dht11.DHT11(pin=DHT_PIN)

# Initialize I2C bus for RTC
bus = SMBus(1)  # Use 1 for Raspberry Pi
RTC_ADDRESS = 0x68  # I2C address for DS1307 RTC


def read_rtc():
    # Read the time from the RTC
    data = bus.read_i2c_block_data(RTC_ADDRESS, 0x00, 7)
    seconds = data[0] & 0x7F
    minutes = data[1]
    hours = data[2] & 0x3F
    day = data[3]
    date = data[4]
    month = data[5]
    year = data[6] + 2000  # Adjust for the year

    return f"{hours:02}:{minutes:02}:{seconds:02}", f"{date:02}/{month:02}/{year}"


@app.route('/')
def index():
    # Read data from the DHT11 sensor
    result = sensor.read()
    if result.is_valid():
        temperature = result.temperature
        humidity = result.humidity
    else:
        temperature = None
        humidity = None

    # Read time from RTC
    time_now, date_now = read_rtc()

    return render_template('index.html', temperature=temperature, humidity=humidity, time=time_now, date=date_now)

@app.route('/', methods=['GET', 'POST'])
def call_function():
    num = 1
    imageCapture.capture_image(num)
    message = classify_image(f"photo_{num}.jpg")

    
    return render_template('index.html', message=message)

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000)  # Run the app on all interfaces
    except KeyboardInterrupt:
        print("Program stopped by User")
    finally:
        GPIO.cleanup()