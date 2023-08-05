# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from cogneed_protos.ai.cogneed.api import common_pb2 as cogneed__protos_dot_ai_dot_cogneed_dot_api_dot_common__pb2
from cogneed_protos.ai.cogneed.api.trainui import config_pb2 as cogneed__protos_dot_ai_dot_cogneed_dot_api_dot_trainui_dot_config__pb2


class ConfigServiceStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.read = channel.unary_unary(
        '/ai.cogneed.api.trainui.config.ConfigService/read',
        request_serializer=cogneed__protos_dot_ai_dot_cogneed_dot_api_dot_trainui_dot_config__pb2.ReadRequest.SerializeToString,
        response_deserializer=cogneed__protos_dot_ai_dot_cogneed_dot_api_dot_trainui_dot_config__pb2.Config.FromString,
        )
    self.update = channel.unary_unary(
        '/ai.cogneed.api.trainui.config.ConfigService/update',
        request_serializer=cogneed__protos_dot_ai_dot_cogneed_dot_api_dot_trainui_dot_config__pb2.UpdateTarget.SerializeToString,
        response_deserializer=cogneed__protos_dot_ai_dot_cogneed_dot_api_dot_common__pb2.AckResponse.FromString,
        )


class ConfigServiceServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def read(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def update(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_ConfigServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'read': grpc.unary_unary_rpc_method_handler(
          servicer.read,
          request_deserializer=cogneed__protos_dot_ai_dot_cogneed_dot_api_dot_trainui_dot_config__pb2.ReadRequest.FromString,
          response_serializer=cogneed__protos_dot_ai_dot_cogneed_dot_api_dot_trainui_dot_config__pb2.Config.SerializeToString,
      ),
      'update': grpc.unary_unary_rpc_method_handler(
          servicer.update,
          request_deserializer=cogneed__protos_dot_ai_dot_cogneed_dot_api_dot_trainui_dot_config__pb2.UpdateTarget.FromString,
          response_serializer=cogneed__protos_dot_ai_dot_cogneed_dot_api_dot_common__pb2.AckResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'ai.cogneed.api.trainui.config.ConfigService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
