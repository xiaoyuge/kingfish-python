import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

response = openai.Image.create(
  prompt="Several good friends are drinking at the seaside bar, and the sun is setting now",
  n=2,
  size="1024x1024"
)

for i in range(len(response['data'])):
    image_url = response['data'][i]['url']
    print(image_url)
