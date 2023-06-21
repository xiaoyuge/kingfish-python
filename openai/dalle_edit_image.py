import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

openai.Image.create_edit(
  image=open("/Users/joyce/kingfish-python/kingfish-python/openai/image/pub-3.png", "rb"),
  prompt="酒瓶边缘更清晰",
  n=2,
  size="1024x1024"
)
