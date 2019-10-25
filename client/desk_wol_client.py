import grpc

from client.args_parser import ArgsParser
from client.signature_encrypter import SignatureEncrypter
from protos.out import desk_wol_pb2
from protos.out import desk_wol_pb2_grpc


class PowerClient:
    def __init__(self):
        self.args_parser = ArgsParser()
        self.channel = grpc.insecure_channel('localhost:50051')
        self.stub = desk_wol_pb2_grpc.PowerStub(self.channel)
        self.signature = SignatureEncrypter.encrypt_signature("tests/id_rsa_test")

    def exec(self):
        option = self.args_parser.parser.parse_args().option
        power_request = desk_wol_pb2.PowerRequest(token=self.signature)
        status_response: desk_wol_pb2.StatusResponse = None

        if option == ArgsParser.power_on:
            status_response = self.stub.PowerOn(power_request)

        if option == ArgsParser.power_off:
            status_response = self.stub.PowerOff(power_request)

        if option == ArgsParser.hard_reset:
            status_response = self.stub.HardReset(power_request)

        if status_response:
            for status in status_response:
                print(status.info)


power_client = PowerClient()
power_client.exec()
