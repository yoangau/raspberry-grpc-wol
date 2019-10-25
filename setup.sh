#!/usr/bin/bash

pip install -r requirements.txt
python -m grpc_tools.protoc -Iprotos --python_out=client --grpc_python_out=client protos/desk_wol.proto
python -m grpc_tools.protoc -Iprotos --python_out=server --grpc_python_out=server protos/desk_wol.proto
