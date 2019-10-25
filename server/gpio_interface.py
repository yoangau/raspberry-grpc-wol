import time

import RPi.GPIO as GPIO


class GPIOInterface:
    short_signal: float = .2
    hard_reset_signal: float = 10.0
    power_pin: int = 23
    status_pin: int = 24
    button_pin: int = 4

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.power_pin, GPIO.OUT)
        GPIO.setup(self.status_pin, GPIO.IN)
        GPIO.setup(self.button_pin, GPIO.IN)

    def power_status(self) -> bool:
        return GPIO.input(self.status_pin)

    def power_on(self) -> bool:
        GPIO.output(self.power_pin, GPIO.HIGH)
        time.sleep(self.short_signal)
        GPIO.output(self.power_pin, GPIO.LOW)
        return self.power_status()

    def hard_reset(self) -> bool:
        GPIO.output(self.power_pin, GPIO.HIGH)
        time.sleep(self.hard_reset_signal)
        GPIO.output(self.power_pin, GPIO.LOW)
        return not self.power_status()

    def physical_repeater(self) -> None:
        while True:
            try:
                GPIO.wait_for_edge(self.button_pin, GPIO.RISING)
                print("Power Button Pressed")
                status = self.power_on()
                print(f'It {"did" if status else "did not"} work')
            except KeyboardInterrupt:
                print("Error with repeater")
                return


if __name__ == '__main__':
    gpio_interface = GPIOInterface()
    gpio_interface.physical_repeater()
    GPIO.cleanup()
