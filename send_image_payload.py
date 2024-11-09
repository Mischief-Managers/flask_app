import base64
import json   
import pandas as pd                

import requests

api = 'https://dc7c-91-194-240-2.ngrok-free.app/add-record'
image_files = ['/Users/muditashakya/Downloads/OneDrive_1_11-9-2024/20200124_091405.jpg',
              '/Users/muditashakya/Downloads/OneDrive_1_11-9-2024/20201104_104139.jpg',
              '/Users/muditashakya/Downloads/OneDrive_1_11-9-2024/20220517_114912.jpg',
              '/Users/muditashakya/Downloads/OneDrive_1_11-9-2024/IMG_2316.jpg',
              '/Users/muditashakya/Downloads/OneDrive_1_11-9-2024/20201104_104217.jpg',
              '/Users/muditashakya/Downloads/OneDrive_1_11-9-2024/20200124_092048.jpg',
              '/Users/muditashakya/Downloads/OneDrive_1_11-9-2024/20200124_090359.jpg']

def image_to_base64(image_path):
    import base64
    import os
    
    # Get the file extension
    file_extension = os.path.splitext(image_path)[1].lower()
    
    # Map file extensions to MIME types
    mime_types = {
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.gif': 'image/gif',
        '.bmp': 'image/bmp',
        '.webp': 'image/webp'
    }
    
    # Get MIME type
    mime_type = mime_types.get(file_extension, 'image/jpeg')
    
    try:
        # Read binary file
        with open(image_path, 'rb') as image_file:
            # Encode to base64
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            
            # Create data URI
            data_uri = f'data:{mime_type};base64,{encoded_string}'
            
            return {
                'success': True,
                'data_uri': data_uri,
                'raw_base64': encoded_string,
                'mime_type': mime_type
            }
            
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

df = pd.read_csv('maintenance-data.txt')

for i, image_file in enumerate(image_files):
    data = df.iloc[i].to_dict()
    # print(df.iloc[i].to_dict(orient='records'))
    result = image_to_base64(image_files[i])
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    payload_obj = {"image": result["raw_base64"]}
    for key in data.keys():
        payload_obj[key] = data[key]
    payload = json.dumps(payload_obj)
    with open("payload.json", "w") as f:
        json.dump(payload, f)
    response = requests.post(api, data=payload, headers=headers, verify=False)
    try:
        data = response.json()     
        print(data)                
    except requests.exceptions.RequestException:
        print(response.text)