from concurrent import futures

import grpc

import protos.pythonpb2.desk_wol_pb2 as dw_pb2
import protos.pythonpb2.desk_wol_pb2_grpc as dw_pb2_grpc
from server.signature_decrypter import SignatureDecrypter


class PowerService(dw_pb2_grpc.PowerServicer):

    @staticmethod
    def check_signature(request: dw_pb2.PowerRequest) -> dw_pb2.StatusResponse:
        return dw_pb2.StatusResponse(
            info=SignatureDecrypter.decrypt_signature(
                "../tests/id_rsa_test.pub", request.token))

    def PowerOn(self, request, context) -> dw_pb2.StatusResponse:
        return PowerService.check_signature(request)

    def PowerOff(self, request, context) -> dw_pb2.StatusResponse:
        return PowerService.check_signature(request)

    def HardReset(self, request, context) -> dw_pb2.StatusResponse:
        return PowerService.check_signature(request)

    @staticmethod
    def serve():
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
        dw_pb2_grpc.add_PowerServicer_to_server(
            PowerService(), server)
        server.add_insecure_port('[::]:50051')
        server.start()
        server.wait_for_termination()
