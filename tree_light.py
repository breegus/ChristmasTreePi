from threading import Thread, Event
import RPi.GPIO as GPIO
from time import sleep
from random import randint

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
        self._thread = Thread(target=self.__flicker)
        self._event = Event()

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

    def set_flicker(self, flicker: bool) -> None:
        self._enableFlicker = flicker

        if self._enableFlicker and self.number != 24:  # Exclude star from flicker effect
            self._thread = Thread(target=self.__flicker)
            self._thread.start()

    def __flicker(self):
        if not self._isEnabled:
            self.set_enabled(True)
        if not self._enableFlicker:
            return

        while not self._event.is_set() or not self._enableFlicker:
            brightness = randint(1, self._brightness)
            speed = randint(50, 100) / 100  # 0.5 - 1.0

            if self._duty < brightness:  # Increasing fade
                for pwm in range(self._duty, brightness + 1):
                    if pwm >= self._brightness:
                        self._pwm.ChangeDutyCycle(self._brightness)
                    else:
                        self._pwm.ChangeDutyCycle(pwm)
                    self._duty = pwm
                    sleep(0.01)

            elif self._duty > brightness:  # Decreasing fade
                for pwm in reversed(range(brightness, self._duty + 1)):
                    if pwm >= self._brightness:
                        self._pwm.ChangeDutyCycle(self._brightness)
                    else:
                        self._pwm.ChangeDutyCycle(pwm)
                    self._duty = pwm
                    sleep(0.01)

            sleep(speed)
