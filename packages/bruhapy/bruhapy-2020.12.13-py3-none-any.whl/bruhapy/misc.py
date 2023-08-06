import requests
import json

class Response(object):
  """The translation object"""
  def __init__(self,dictionary):
    self.res = dictionary['res']
    self.query = dictionary['query']

def cb(text):
    response = requests.get(f'https://bruhapi.xyz/cb/{text}')
    rej = json.loads(response.text)
    return Response(rej)

def sponge(text):
    response = requests.get(f'https://bruhapi.xyz/sponge/{text}')
    rej = json.loads(response.text)
    return rej['res']

def tts(text):
  response = requests.get(f'https://bruhapi.xyz/tts/{text}')
  rej = json.loads(response.text)
  return rej['res']