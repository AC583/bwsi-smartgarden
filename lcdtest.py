import spidev
import time
from PIL import Image, ImageDraw, ImageFont

# ILI9341 display settings
DC = 24  # Data/Command pin
RST = 25  # Reset pin
SPI_SPEED = 32000000  # SPI speed

# Initialize SPI
spi = spidev.SpiDev()
spi.open(0, 0)  # Open SPI bus 0, device 0
spi.max_speed_hz = SPI_SPEED

# Function to send command to the display
def send_command(cmd):
    spi.xfer2([cmd])

# Function to send data to the display
def send_data(data):
    spi.xfer2([data])

# Function to initialize the display
def init_display():
    send_command(0x01)  # Software reset
    time.sleep(0.1)
    send_command(0x28)  # Display off
    send_command(0xCF)  # Power control B
    send_data(0x00)
    send_data(0xC1)
    send_data(0x30)
    send_command(0xED)  # Power on sequence control
    send_data(0x64)
    send_data(0x03)
    send_data(0x12)
    send_data(0x81)
    send_command(0xE8)  # Driver timing control A
    send_data(0x85)
    send_data(0x00)
    send_data(0x78)
    send_command(0xCB)  # Power control A
    send_data(0x39)
    send_data(0x2C)
    send_data(0x00)
    send_data(0x34)
    send_data(0x02)
    send_command(0xF7)  # Pump ratio control
    send_data(0x20)
    send_command(0xEA)  # Driver timing control B
    send_data(0x00)
    send_data(0x00)
    send_command(0xB1)  # Frame rate control
    send_data(0x00)
    send_data(0x1B)
    send_command(0xB6)  # Display function control
    send_data(0x0A)
    send_data(0xA2)
    send_command(0xC0)  # Power control 1
    send_data(0x26)
    send_command(0xC1)  # Power control 2
    send_data(0x11)
    send_command(0xC5)  # VCOM control 1
    send_data(0x35)
    send_data(0x3E)
    send_command(0xC7)  # VCOM control 2
    send_data(0xBE)
    send_command(0x36)  # Memory access control
    send_data(0x48)
    send_command(0x3A)  # Pixel format
    send_data(0x55)
    send_command(0xB0)  # Interface control
    send_data(0x00)
    send_command(0x11)  # Sleep out
    time.sleep(0.1)
    send_command(0x29)  # Display on

# Function to clear the display
def clear_display():
    send_command(0x2C)  # Memory write
    for _ in range(240 * 320):
        send_data(0x00)  # Fill with black

# Function to display a message
def display_message(message):
    # Create an image with white background
    image = Image.new('RGB', (240, 320), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    
    # Load a font
    font = ImageFont.load_default()
    
    # Draw the message
    draw.text((10, 10), message, fill=(0, 0, 0), font=font)
    
    # Send the image data to the display
    send_command(0x2C)  # Memory write
    for y in range(320):
        for x in range(240):
            r, g, b = image.getpixel((x, y))
            send_data(b >> 3 | (g << 3) & 0xFC | (r << 8) & 0xF800)  # Convert RGB to 16-bit color

# Main function
if __name__ == "__main__":
    init_display()
    clear_display()
    display_message("Hello, World!")
    time.sleep(5)  # Display for 5 seconds
    clear_display()  # Clear the display before exiting
    spi.close()