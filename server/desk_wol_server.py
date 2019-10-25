import grpc
from concurrent import futures
import protos.pythonpb2.desk_wol_pb2 as dw_pb2
import protos.pythonpb2.desk_wol_pb2_grpc as dw_pb2_grpc
from server.signature_decrypter import SignatureDecrypter


class PowerServicer(dw_pb2_grpc.PowerServicer):

    @staticmethod
    def check_signature(request: dw_pb2.PowerRequest) -> dw_pb2.StatusResponse:
        return dw_pb2.StatusResponse(
            info=SignatureDecrypter.decrypt_signature(
                "/home/yoangau/Documents/raspberry-grpc-wol/tests/id_rsa_test.pub", request.token))

    def PowerOn(self, request, context):
        status = PowerServicer.check_signature(request)

        if status.info is SignatureDecrypter.invalid_signature:
            return status
        yield status

        return dw_pb2.StatusResponse(info=f"Power on ...")

    def PowerOff(self, request, context):
        status = PowerServicer.check_signature(request)

        if status.info is SignatureDecrypter.invalid_signature:
            return status
        yield status

        return dw_pb2.StatusResponse(info=f"Power off ...")

    def HardReset(self, request, context):
        status = PowerServicer.check_signature(request)

        if status.info is SignatureDecrypter.invalid_signature:
            return status
        yield status

        return dw_pb2.StatusResponse(info=f"Hard reset ...")

    @staticmethod
    def serve():
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        dw_pb2_grpc.add_PowerServicer_to_server(
            PowerServicer(), server)
        server.add_insecure_port('[::]:50051')
        server.start()
        server.wait_for_termination()
