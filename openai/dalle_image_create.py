import openai

response = openai.Image.create(
  prompt="江南小酒馆的内景、摆着中式白酒瓶和酒杯的酒柜、酒柜前是中式古典吧台、吧台上摆着一些酒瓶和酒具、整体风格简洁，幽暗、古风",
  n=2,
  size="1024x1024"
)

##image_url = response['data'][0]['url']
for i in range(len(response['data'])):
    image_url = response['data'][i]['url']
    print(image_url)
