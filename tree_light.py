from threading import Thread
import RPi.GPIO as GPIO

class TreeLight:
    def __init__(self, number: int, pin: int) -> None:
        self.number = number  # Date number on tree
        self.pin = pin  # GPIO pin number (BCM)

        GPIO.setup(self.pin, GPIO.OUT)  # Init GPIO for my pin
        GPIO.output(self.pin,GPIO.LOW)

        self._isEnabled = False  # LED On / Off
        self._brightness = 100  # Duty (brightness 0-100)
        self._enableFlicker = False  # Flicker effect

        self._pwm = GPIO.PWM(self.pin, self._brightness)

        self.set_enabled(False)  # Off by default

    def set_enabled(self, enabled: bool) -> None:
        self._isEnabled = enabled

        if self._isEnabled:
            self._pwm.start(self._brightness)
        else:
            self._pwm.stop()

    def set_brightness(self, brightness: int) -> None:
        self._brightness = brightness
        if self._brightness <= 0:
            self.set_enabled(False)
        else:
            if not self._isEnabled:
                self.set_enabled(True)
            self._pwm.ChangeDutyCycle(self._brightness)
