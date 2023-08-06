import requests
import json

class Translation(object):
  """The translation object"""
  def __init__(self,dictionary):
    self.lang = dictionary['lang']
    self.tr = dictionary['text']
    self.original = dictionary['original']

def joke():
    response = requests.get(f'https://bruhapi.xyz/joke/')
    rej = json.loads(response.text)
    return rej['res']

def translate(text):
    response = requests.get(f'https://bruhapi.xyz/translate/{text}')
    rej = json.loads(response.text)
    return Translation(rej)