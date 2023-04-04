import os
import openai
import time
import delete_train_file
import delete_train_model

#获取访问api的key
openai.api_key = os.getenv("OPENAI_API_KEY")

#删除之前的训练文件
delete_train_file.delete_train_file()

#删除之前训练的模型
delete_train_model.delete_train_model()

#上传训练数据
response = openai.File.create(
  file=open("data/resume_data_prepared.jsonl"), #用工具处理后的训练数据
  #file=open("data/resume_data.jsonl"),#原始训练数据
  #file=open("data/resume_data_small.jsonl"),#用小数据集试一下
  purpose='fine-tune'
)

#获取training_file的file-id
file_id = response.id
print(f"新创建的训练文件:{file_id}")

#创建fine-tune job并执行
response = openai.FineTune.create(
    training_file=f"{file_id}",
    model="davinci",#davinci、babbage、curie、ada
    batch_size = 10,
    n_epochs=10,
    #learning_rate_multiplier=0.2
)

#获取fine-job-id
fine_tune_job_id = response.id
print(f"新开始的fine_tune_job:{fine_tune_job_id}")

#循环判断fine-job是否执行完成
succeed = False
my_model_id = ""
while succeed == False:
    response = openai.FineTune.retrieve(id=f"{fine_tune_job_id}")
    if response.status == "succeeded":
        # 获取训练的新模型的id
        my_model_id = response.fine_tuned_model
        succeed = True
        print(f"fine_tune_job:{fine_tune_job_id}已完成，新训练的模型是{my_model_id}")
    else:
        print(f"fine_tune_job:{fine_tune_job_id}未完成，状态是：{response.status},等待30秒。。。")
        time.sleep(30)

# 对新训练的模型提问
print(f"开始对新训练的模型{my_model_id}提问：")
q1 = "王兴渝的最高学历是？"
response = openai.Completion.create(
    model=f'{my_model_id}',
    prompt=f"{q1} ->",
    stop=[". end"],
    temperature=0,
    max_tokens = 10
)
print(response.choices[0].text)

q2 = "王兴渝工作时间最长的公司是？"
response = openai.Completion.create(
    model=f'{my_model_id}',
    prompt=f"{q2} ->",
    stop=[". end"],
    temperature=0,
    max_tokens = 50
)
print(response.choices[0].text)

q3 = "王兴渝擅长的技术领域是？"
response = openai.Completion.create(
    model=f'{my_model_id}',
    prompt=f"{q3} ->",
    stop=[". end"],
    temperature=0,
    max_tokens = 100
)
print(response.choices[0].text)



