import bruhapy
import requests as req
import json
def taco():
    response = req.get(f'https://bruhapi.xyz/taco')
    if response.status_code != 200:
      raise bruhapy.RequestError("The endpoint is having an error, either it was moved or it is currently offline.")
    rej = json.loads(response.text)
    return rej['res']