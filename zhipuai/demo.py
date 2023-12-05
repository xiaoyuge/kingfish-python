import zhipuai

# 定义一个函数，用于调用模型
zhipuai.api_key = '8895febba7f691d9f067a23913c7fca0.eRVl3bKLcRLSPq6P'

# 调用模型
response = zhipuai.model_api.invoke(
    model = 'chatglm_pro',
    prompt = [{'role':'user','content':'甲、乙、丙三个人分别住在红、蓝、绿三个颜色的房子里，他们喜欢的水果是苹果、香蕉和橙子，他们每个人都从事不同的职业。1. 在红房子里住的人喜欢苹果。2. 乙是医生。3. 丙住在蓝房子里。4. 不喜欢苹果的人住在绿房子里。问题：甲住在哪个颜色的房子里？'}],
    top_p=0.7,
    temperature=0.9
)

# 打印返回值
print(response)