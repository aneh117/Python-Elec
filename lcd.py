import I2C_LCD_driver  # Import the library
from time import sleep

LCD = I2C_LCD_driver.lcd()  # Instantiate an LCD object

def display_message(line1, line2="", delay=2):
    """Displays a message on the LCD screen for a specified time."""
    LCD.lcd_clear()
    LCD.lcd_display_string(line1, 1)  # Display text on line 1
    LCD.lcd_display_string(line2, 2)  # Display text on line 2 (if any)
    sleep(delay)
def lcd_display():
    while True:
        display_message("Police 999")
        display_message("Ambulance 995")
        display_message("Son", "84173859")
        
lcd_display()
