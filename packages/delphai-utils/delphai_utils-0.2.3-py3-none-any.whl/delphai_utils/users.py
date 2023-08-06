from typing import Dict, List, Tuple, Union
from base64 import b64decode
import json
from grpc.aio import ServicerContext


def get_user(context: ServicerContext) -> Dict:
  metadata = dict(context.invocation_metadata())
  user64 = metadata['x-delphai-user']
  user = b64decode(user64)
  return json.loads(user)


def get_groups(context: ServicerContext) -> List[str]:
  """
  Gets groups of calling identity

  :param grpc.aio.ServicerContext context: context passed to grpc endpoints
  :return raw roles passed from keycloak
  :rtype List[str]
  """
  assert isinstance(context, object)
  user = get_user(context)
  return user['groups']


def get_affiliation(context: ServicerContext) -> Union[Tuple[str, str], None]:
  """
  Gets organization and department of user

  :param grpc.aio.ServicerContext context: context passed to grpc endpoints
  :return organization and department as a tuple or None if not affiliated
  :rtype Union[Tuple[str, str], None]
  """

  raw_groups = get_groups(context)
  if len(raw_groups) == 0:
    return None
  else:
    return raw_groups[0].split('/')[1:3]
