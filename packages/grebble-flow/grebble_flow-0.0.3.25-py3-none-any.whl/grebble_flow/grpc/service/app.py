import json

from grebble_flow.managment.info import generate_package_info

from grebble_flow.grpc.proto import app_pb2_grpc, app_pb2


class AppService(app_pb2_grpc.AppServicer):
    def __init__(self, *args, **kwargs):
        pass

    def AppInfo(self, request, context):
        info = generate_package_info()

        result = app_pb2.AppInfoResponse()
        result.processors.extend(
            [app_pb2.ProcessorInfo(name=processor["name"], attributeSchema=json.dumps(processor["attributes_schema"])) for processor in info["processors"]]
        )
        return result
