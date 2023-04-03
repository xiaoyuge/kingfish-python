
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def delete_train_file():

    #先删除之前上传过的训练文件
    response = openai.File.list()
    train_file_list = response.data

    for i in range(len(train_file_list)):
        file_id = train_file_list[i].openai_id
        delete_file_result = openai.File.delete(f"{file_id}")
        print(f"{delete_file_result.id} is deleted:{delete_file_result.deleted}")

    #再查询一遍训练文件
    response = openai.File.list()

    if len(response.data) == 0:
        print("train file delete complete!")
    else:
        for i in range(len(response.data)):
            file_id = response.data[i].openai_id
            print(f"{file_id} is not deleted")


if __name__ == "__main__":
    delete_train_file()
