#!/usr/bin/fish

pip install -r requirements.txt
python -m grpc_tools.protoc -Iprotos --python_out=protos/out --grpc_python_out=protos/out protos/desk_wol.proto
set -x PYTHONPATH (pwd)/protos/out:(pwd)/protos:(pwd):(pwd)/client
