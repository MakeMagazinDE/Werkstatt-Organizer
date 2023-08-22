import machine
import neopixel
import ure
import urequests
import socket
import time

# Konfiguration der den Boxen zugehörigen Neopixel
NEOPIXEL_CONFIG = {
    1: [0, 1],
    2: [2, 3],
    3: [4, 5],
    4: [6, 7],
    5: [8, 9],
    # Add more groups as needed
}

# Konfiguration der Anzahl von Neopixel und des ESP32 Pins zur Ansteuerung 
PIXEL_PIN = machine.Pin(2, machine.Pin.OUT)
NUM_PIXELS = 10


strip = neopixel.NeoPixel(PIXEL_PIN, NUM_PIXELS)

# Function to control the NeoPixel strip
def set_neopixels(group):
    if group in NEOPIXEL_CONFIG:
        pixels = NEOPIXEL_CONFIG[group]
        for pixel in pixels:
            strip[pixel] = (0, 255, 0)  # Set neopixel to GREEN

        # Update the neopixel strip
        strip.write()

# Start the web server
def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)
 
    while True:
        try:
            cl, addr = s.accept()
        except OSError:
            pass
        else:
            # Read the request data
            request = cl.recv(1024)
            request = str(request)

            # Extract the value of 'b' from the query string
            match = ure.search("GET /\?b=(\d)", request)
            print (match)

            if match:
                # Get the group number from the query parameter
                group = int(match.group(1))
                print(group)
                if (group==0):
                    # Turn off all neopixels
                    strip.fill((0, 0, 0))
                else:
                    # Set the neopixels based on the group number
                    set_neopixels(group)

                strip.write()

            # Send the response
            response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\nOK"
            cl.send(response)

            # Close the connection
            cl.close()

# Start the web server
start_server()
