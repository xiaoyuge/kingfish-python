import openai

response = openai.Image.create(
  prompt="青春煮酒",
  n=2,
  size="1024x1024"
)

##image_url = response['data'][0]['url']
for i in range(len(response['data'])):
    image_url = response['data'][i]['url']
    print(image_url)
