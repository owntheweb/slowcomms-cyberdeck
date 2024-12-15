import serial
import serial.tools.list_ports
import time
from PIL import Image
import sys

def find_pico():
    """Find the Pico device port."""
    ports = serial.tools.list_ports.comports()
    for port in ports:
        # Look for typical Pico device descriptions
        if "USB Serial Device" in port.description or "Pico" in port.description:
            return port.device
    return None

def send_image_to_pico(image_path):
    # Find Pico port
    pico_port = find_pico()
    if not pico_port:
        print("Pico device not found!")
        return False
    
    try:
        # Open serial connection
        ser = serial.Serial(pico_port, 115200, timeout=1)
        time.sleep(2)  # Wait for connection to establish
        
        # Open and resize image
        img = Image.open(image_path)
        img = img.resize((320, 240))  # Adjust to your display size
        pixels = img.load()
        
        # Send pixel data
        for y in range(img.height):
            for x in range(img.width):
                r, g, b = pixels[x, y]
                data = f"{x},{y},{r},{g},{b}\n"
                ser.write(data.encode())
                time.sleep(0.001)  # Small delay to prevent overwhelming the Pico
                
        ser.close()
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python computer_sender.py <image_path>")
        sys.exit(1)
        
    image_path = sys.argv[1]
    if send_image_to_pico(image_path):
        print("Image sent successfully!")
    else:
        print("Failed to send image.")