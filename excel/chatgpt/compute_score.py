import pandas as pd

# 读取excel文件
df = pd.read_excel("data/成绩表.xlsx", sheet_name="score_detail")

# 按班级汇总计算平均分
grouped = df.groupby("班级").mean()[["语文", "数学", "英语"]].reset_index()

# 将结果保存到新的excel文件中
writer = pd.ExcelWriter("data/成绩汇总表.xlsx")
grouped.to_excel(writer, sheet_name="score_summary", index=False)
writer.save()
