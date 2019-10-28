import os
import sys

# Todo: Dockerimage could be rebuild to add the right PYTHONPATH env var instead of this:
sys.path.extend([os.environ['SERVERPATH'], f"{os.environ['SERVERPATH']}/protos/pythonpb2"])

import logging

from concurrent import futures

import grpc

import protos.pythonpb2.desk_wol_pb2 as dw_pb2
import protos.pythonpb2.desk_wol_pb2_grpc as dw_pb2_grpc
from common.ports import desk_wol_port, gpio_port
from common.commands import *
from server.signature_decrypter import SignatureDecrypter


class PowerService(dw_pb2_grpc.PowerServicer):

    def __init__(self):
        self.channel = grpc.insecure_channel(f'gpio:{gpio_port}')
        self.stub = dw_pb2_grpc.GPIOStub(self.channel)

    @staticmethod
    def check_signature(request: dw_pb2.PowerRequest) -> dw_pb2.StatusResponse:
        return dw_pb2.StatusResponse(
            info=SignatureDecrypter.decrypt_signature(
                "../tests/id_rsa_test.pub", request.token))

    def __signal(self, request, signal: str) -> [dw_pb2.StatusResponse]:
        command_map = {
            power_on: self.stub.SignalOn,
            power_off: self.stub.SignalOff,
            hard_reset: self.stub.SignalHardReset
        }

        status_infos = [PowerService.check_signature(request)]
        signal_response = dw_pb2.StatusResponse(info=f"Signal success : {command_map[signal]().info}")
        status_infos.append(signal_response)

        return status_infos

    def PowerOn(self, request, context) -> dw_pb2.StatusResponse:
        return self.__signal(request, power_on)

    def PowerOff(self, request, context) -> dw_pb2.StatusResponse:
        return self.__signal(request, power_off)

    def HardReset(self, request, context) -> dw_pb2.StatusResponse:
        return self.__signal(request, hard_reset)

    @staticmethod
    def serve():
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
        dw_pb2_grpc.add_PowerServicer_to_server(
            PowerService(), server)
        server.add_insecure_port(f'[::]:{desk_wol_port}')
        server.start()
        server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    PowerService.serve()
