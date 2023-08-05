# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from grebble_flow.grpc.proto import processor_pb2 as grebble__flow_dot_grpc_dot_proto_dot_processor__pb2


class ProcessorStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Execute = channel.unary_stream(
                '/grebble_flow.grpc.proto.Processor/Execute',
                request_serializer=grebble__flow_dot_grpc_dot_proto_dot_processor__pb2.FlowRequest.SerializeToString,
                response_deserializer=grebble__flow_dot_grpc_dot_proto_dot_processor__pb2.FlowResponse.FromString,
                )


class ProcessorServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Execute(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ProcessorServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Execute': grpc.unary_stream_rpc_method_handler(
                    servicer.Execute,
                    request_deserializer=grebble__flow_dot_grpc_dot_proto_dot_processor__pb2.FlowRequest.FromString,
                    response_serializer=grebble__flow_dot_grpc_dot_proto_dot_processor__pb2.FlowResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'grebble_flow.grpc.proto.Processor', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Processor(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Execute(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/grebble_flow.grpc.proto.Processor/Execute',
            grebble__flow_dot_grpc_dot_proto_dot_processor__pb2.FlowRequest.SerializeToString,
            grebble__flow_dot_grpc_dot_proto_dot_processor__pb2.FlowResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
