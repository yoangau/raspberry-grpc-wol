import sys

sys.path.extend(['..', '../protos/pythonpb2'])

import grpc

import protos.pythonpb2.desk_wol_pb2 as dw_pb2
import protos.pythonpb2.desk_wol_pb2_grpc as dw_pb2_grpc
from client.args_parser import ArgsParser
from client.signature_encrypter import SignatureEncrypter
from common.ports import desk_wol_port


class PowerClient:
    def __init__(self):
        self.args_parser = ArgsParser()
        self.channel = grpc.insecure_channel(f'localhost:{desk_wol_port}')
        self.stub = dw_pb2_grpc.PowerStub(self.channel)

    def exec(self):
        args = self.args_parser.parser.parse_args()
        signature = SignatureEncrypter.encrypt_signature(args.key_file)
        power_request = dw_pb2.PowerRequest(token=signature)
        status_response: dw_pb2.StatusResponse = None

        if args.option == ArgsParser.power_on:
            status_response = self.stub.PowerOn(power_request)

        if args.option == ArgsParser.power_off:
            status_response = self.stub.PowerOff(power_request)

        if args.option == ArgsParser.hard_reset:
            status_response = self.stub.HardReset(power_request)

        for status in status_response:
            print(status.info)


if __name__ == '__main__':
    power_client = PowerClient()
    power_client.exec()
