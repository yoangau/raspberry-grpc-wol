import os
import sys

# Todo: Dockerimage could be rebuild to add the right PYTHONPATH env var instead of this:
sys.path.extend([os.environ['SERVERPATH'], f"{os.environ['SERVERPATH']}/protos/pythonpb2"])

import time
from concurrent import futures

import RPi.GPIO as GPIO
import grpc

import protos.pythonpb2.desk_wol_pb2 as dw_pb2
import protos.pythonpb2.desk_wol_pb2_grpc as dw_pb2_grpc
from common.ports import gpio_port


class GPIOService(dw_pb2_grpc.GPIOServicer):
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

    def __send_signal(self, sleep_time: int or float) -> None:
        GPIO.output(self.power_pin, GPIO.HIGH)
        time.sleep(sleep_time)
        GPIO.output(self.power_pin, GPIO.LOW)

    def SignalOn(self, request, context):
        return dw_pb2.SignalResponse(info=self.__send_signal(self.short_signal))

    def SignalOff(self, request, context):
        return dw_pb2.SignalResponse(info=self.__send_signal(self.short_signal))

    def SignalHardReset(self, request, context):
        return dw_pb2.SignalResponse(info=self.__send_signal(self.hard_reset_signal))

    def power_status(self) -> bool:
        return GPIO.input(self.status_pin)

    def __physical_repeater(self) -> None:
        print("Power Button Pressed")
        status = self.power_on()
        print(f'It {"did" if status else "did not"} work')

    def physical_repeater(self) -> None:
        GPIO.add_event_detect(self.button_pin, GPIO.RISING, callback=self.__physical_repeater,
                              bouncetime=self.debounce_time)

    def serve(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
        dw_pb2_grpc.add_GPIOServicer_to_server(self, server)
        server.add_insecure_port(f'[::]:{gpio_port}')
        server.start()
        server.wait_for_termination()


if __name__ == '__main__':
    gpio_service = GPIOService()
    gpio_service.physical_repeater()
    gpio_service.serve()
    GPIO.cleanup()
