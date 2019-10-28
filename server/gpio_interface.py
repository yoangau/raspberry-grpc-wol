import time

import RPi.GPIO as GPIO


class GPIOInterface:
    short_signal: float = .2
    hard_reset_signal: float = 10.0
    power_pin: int = 23
    status_pin: int = 24
    button_pin: int = 4
    debounce_time: int = 100

    def __init__(self) -> None:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.power_pin, GPIO.OUT)
        GPIO.setup(self.status_pin, GPIO.IN)
        GPIO.setup(self.button_pin, GPIO.IN)

    def __send_signal(self, sleep_time: int) -> None:
        GPIO.output(self.power_pin, GPIO.HIGH)
        time.sleep(sleep_time)
        GPIO.output(self.power_pin, GPIO.LOW)

    def power_status(self) -> bool:
        return GPIO.input(self.status_pin)

    def power_on(self) -> bool:
        self.__send_signal(self.short_signal)
        return self.power_status()

    def hard_reset(self) -> bool:
        self.__send_signal(self.hard_reset_signal)
        return not self.power_status()

    def physical_repeater(self) -> None:
        while True:
            try:
                GPIO.wait_for_edge(self.button_pin, GPIO.RISING, bouncetime=self.debounce_time)
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
