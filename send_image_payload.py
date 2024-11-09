import base64
import json                   

import requests

api = 'https://239e-91-194-240-2.ngrok-free.app/add-record'
image_file = '/Users/muditashakya/Downloads/20231107_105349.jpg'

from PIL import Image 
with open(image_file, "rb") as image_file:
    img = Image.open(image_file.stream)
blob = json.dumps(img.encode("base64"))
# print(im_b64)
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
  
payload = json.dumps({"image": blob})
response = requests.post(api, data=payload, headers=headers, verify=False)
try:
    data = response.json()     
    print(data)                
except requests.exceptions.RequestException:
    print(response.text)