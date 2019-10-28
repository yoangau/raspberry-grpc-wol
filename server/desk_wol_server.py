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
from server.signature_decrypter import SignatureDecrypter


class PowerService(dw_pb2_grpc.PowerServicer):

    def __init__(self):
        self.channel = grpc.insecure_channel(f'localhost:{gpio_port}')
        self.stub = dw_pb2_grpc.GPIOStub(self.channel)

    @staticmethod
    def check_signature(request: dw_pb2.PowerRequest) -> dw_pb2.StatusResponse:
        return dw_pb2.StatusResponse(
            info=SignatureDecrypter.decrypt_signature(
                "../tests/id_rsa_test.pub", request.token))

    def __signal(self, request, signal) -> [dw_pb2.StatusResponse]:
        status_infos = [PowerService.check_signature(request)]
        signal_request = dw_pb2.SignalRequest(signal=signal)
        signal_response = dw_pb2.StatusResponse(info=f"Signal success : {self.stub.Signal(signal_request).status}")
        status_infos.append(signal_response)
        return status_infos

    def PowerOn(self, request, context) -> dw_pb2.StatusResponse:
        return self.__signal(request, "POWERON")

    def PowerOff(self, request, context) -> dw_pb2.StatusResponse:
        return self.__signal(request, "POWEROFF")

    def HardReset(self, request, context) -> dw_pb2.StatusResponse:
        return self.__signal(request, "HARDRESET")

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
