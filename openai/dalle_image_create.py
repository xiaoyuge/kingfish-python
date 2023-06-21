import openai

response = openai.Image.create(
  prompt="江南小酒馆的内景、布满中式白酒瓷酒瓶的酒柜、中式的古典吧台、简洁，幽暗",
  n=2,
  size="1024x1024"
)

##image_url = response['data'][0]['url']
for i in range(len(response['data'])):
    image_url = response['data'][i]['url']
    print(image_url)
