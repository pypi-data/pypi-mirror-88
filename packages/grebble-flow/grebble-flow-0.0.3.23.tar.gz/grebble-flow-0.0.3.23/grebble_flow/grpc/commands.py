from pathlib import Path

import pkg_resources


def install_proto():
    import grpc_tools.protoc

    cwd = Path(pkg_resources.resource_filename("grebble_flow", "")).parents[0]
    proto_include = pkg_resources.resource_filename("grebble_flow", "grpc/proto/")
    python_out = pkg_resources.resource_filename("grebble_flow", "grpc/base/")
    for file in ["processor.proto", "app.proto"]:
        grpc_tools.protoc.main(
            [
                "grpc_tools.protoc",
                f"--proto_path={cwd}",
                f"--python_out=./",
                f"--grpc_python_out=./",
                f"{proto_include}{file}",
            ]
        )
