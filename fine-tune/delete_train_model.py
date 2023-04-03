
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def delete_train_model():

    #查询fine-tune job
    response = openai.FineTune.list()

    #遍历fine-tune job,删除之前训练的模型
    for i in range(len(response.data)):
        fine_tune_job_id = response.data[i].id
        fine_tune_model = response.data[i].fine_tuned_model
        print(f"开始删除fine-tune-job:{fine_tune_job_id}对应的模型：{fine_tune_model}")
        try:
            response = openai.Model.delete(f"{fine_tune_model}")
            print(f"模型{response.id} is deleted:{response.deleted}")
        except Exception as e:
            print('Delete model Excepiton:' + e.user_message)
            
if __name__ == "__main__":
    delete_train_model()



