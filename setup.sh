#!/usr/bin/bash

pip install -r requirements.txt
python -m grpc_tools.protoc -Iprotos --python_out=protos/pythonpb2 --grpc_python_out=protos/pythonpb2 protos/desk_wol.proto
