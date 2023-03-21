import os
import openai

"""
list the openai model api
"""

openai.organization = "org-EB9Hewj27svx8CRq6TB0RKa3"
openai.api_key = os.getenv("OPENAI_API_KEY")
model_list = openai.Model.list()
print(model_list)
    