
from typing import Any

def serialise(obj: Any) -> dict:
  return { snake_to_camel_case(key): value for key, value in obj.__dict__.items() }

def deserialise(obj) -> dict:
  if isinstance(obj, list):
    return deserialise_list(obj)
  return { camel_to_snake_case(key): value for key, value in obj.items() }

def deserialise_list(obj):
  output = []
  for item in obj:
    output.append(deserialise(item))
  return output

def snake_to_camel_case(value: str) -> str:
  return value[0].lower() + value.title()[1:].replace('_','')

def camel_to_snake_case(value: str) -> str:
  return ''.join(['_'+c.lower() if c.isupper() else c for c in value]).lstrip('_')