junctionKey="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"
from openai import OpenAI
import openai
import base64
import json
# Replace with your OpenAI API key
client = OpenAI(api_key=junctionKey)
# client.api_key= junctionKey

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')


def extract_information(base64_image, prompt):
    '''

    :param base64_image:
    :param prompt:
    :return: dict('primary':{},
                  'secondary':{}
                  )
    '''
    # Open the image file in binary mode
    response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": prompt,
          },
          {
            "type": "image_url",
            "image_url": {
              "url": f"data:image/jpeg;base64,{base64_image}",
              "detail": "high"
            },
          },
        ],
      }
    ],)
    res = response.choices[0].message.content
    star_idx = res.find('json') + 4
    end_idx = -3
    attributes = json.loads(res[star_idx:end_idx])
    return attributes

if __name__ == '__main__':
  image_path = "../Junction 2024/Pictures/20220517_114912.jpg"
  base64_image = encode_image(image_path)

  prompt = ("Analyze the image and make two dictionary of key-value pairs of the information present in the image. "
            "The first dictionary should have all the main attributes in large/bold font. "
            "Second dictionary should have the secondary attributes represented in small font. "
            " The output should be in json format of { 'primary' :{'key1':'value1',. . }, 'secondary' :['key1':'value1',. . ]}.")

  attributes = extract_information(base64_image, prompt)
  print(attributes)