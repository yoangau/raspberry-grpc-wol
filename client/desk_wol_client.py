import sys

sys.path.extend(['..', '../protos/pythonpb2'])

import grpc
import protos.pythonpb2.desk_wol_pb2 as dw_pb2
import protos.pythonpb2.desk_wol_pb2_grpc as dw_pb2_grpc
from client.args_parser import ArgsParser
from client.signature_encrypter import SignatureEncrypter
from common.ports import desk_wol_port
from common.commands import *


class PowerClient:
    def __init__(self):
        self.args_parser = ArgsParser()
        self.channel = grpc.insecure_channel(f'localhost:{desk_wol_port}')
        self.stub = dw_pb2_grpc.PowerStub(self.channel)

        self.options = {
            power_on: self.stub.PowerOn,
            power_off: self.stub.PowerOff,
            hard_reset: self.stub.HardReset
        }

    def exec(self):
        args = self.args_parser.parser.parse_args()
        signature = SignatureEncrypter.encrypt_signature(args.key_file)
        power_request = dw_pb2.PowerRequest(token=signature)

        status_response: dw_pb2.StatusResponse = self.options[args.option](
            power_request)

        for status in status_response:
            print(status.info)


if __name__ == '__main__':
    power_client = PowerClient()
    power_client.exec()
