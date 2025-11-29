from tree_light import TreeLight
from homeassistant import HomeAssistant

import RPi.GPIO as GPIO
import traceback
from time import sleep
from datetime import datetime

def main() -> None:
    print("Main code start")

    prev_day = -1
    now = datetime.now()  # Update date
    if int(now.strftime('%m')) == 12:  # If december
        day = 24 if int(now.strftime('%d')) > 24 else int(now.strftime('%d'))  # Cap day at 24
        for led in range(0, day):
            TreeLights[led].start_flicker()
        prev_day = day

    while True:
        now = datetime.now()  # Update date

        if int(now.strftime('%m')) == 12:  # If december
            day = 24 if int(now.strftime('%d')) > 24 else int(now.strftime('%d'))  # Cap day at 24
            if day != prev_day:
                led = TreeLights[day]
                led.set_flicker(True)
                prev_day = day

        sleep(60)

if __name__ == '__main__':
    # Dates:    1, 2,  3,  4,  5,  6, 7, 8,  9, 10, 11, 12, 13, 14, 15,16, 17, 18, 19, 20, 21, 22, 23, 24, 25 (star)
    TreePins = [4, 15, 13, 21, 25, 8, 5, 10, 16, 17, 27, 26, 24, 9, 12, 6, 20, 19, 14, 18, 11, 7, 23, 22, 2]
    TreeLights = []

    try:
        # Setup GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)  # Turn off warnings for overriding pin functions (we are using nearly all of them)

        # Setup tree lights and drivers
        for i in range(0, len(TreePins)):  # Create pin objects/drivers
            TreeLights.append(TreeLight(i, TreePins[i]))
            print("Created light driver: num={0}, pin={1}".format(i, TreePins[i]))

        # Setup homeassistant
        HA = HomeAssistant()

        # Begin
        main()

    except KeyboardInterrupt:  # Exit
        print("Exiting cleanly...")
        for light in TreeLights:  # Stop tree light effects cleanly
            light.set_enabled(False)
        GPIO.cleanup()  # Reset GPIO

    except Exception as e:  # Unknown exception
        traceback.print_exception(e)  # Output error to console
        for light in TreeLights:  # Attempt to stop tree light effects cleanly
            light.set_enabled(False)
        GPIO.cleanup()  # Reset GPIO
        quit()  # Exit
