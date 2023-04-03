import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

#列一下fine-tune job
response = openai.FineTune.list()
job_list = response.data

#遍历一下，拿到最后一个fine tune job
for i in range(len(job_list)):
    job_id = job_list[i].id
    job_status = job_list[i].status
    print(f"fine_job_id:{job_id};fine_job_status:{job_status}")

my_model_id = ""

if job_status == "succeeded":
    #获取最后一个fine_tune_job_id对应的模型
    response = openai.FineTune.retrieve(id=f"{job_id}")
     # 获取训练的新模型的id
    my_model_id = response.fine_tuned_model

# 对新训练的模型提问
print(f"开始对新训练的模型{my_model_id}提问：")
response = openai.Completion.create(
    model=f'{my_model_id}',
    prompt='王兴渝今年多大了? \n\n###\n\n',
    stop=[". end"],
    temperature=0,
    max_tokens = 100
)

print(response.choices[0].text)
    


