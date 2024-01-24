import xlwings as xw

excel_path = '/Users/joyce/Desktop/excel/'

#获取模版表格的列宽数据
def get_template_format(col):##因为无需读取整个excel所有列的列宽，所以这里传入一个读取的列宽范围参数
    wb = xw.Book(excel_path+ "template.xlsx")  # 建立于template.xlsx文件的连接
    sheet = wb.sheets["sheet1"] #打开template.xlsx文件的sheet1
    format = []
    for i in range(col):
        format.append(sheet[0,i].column_width)
    print('列宽:'+str(format)) 
    wb.close()
    return format

#美化表格
def beautiful_sheet(excel_name,row,col,format):
     #设置颜色
    wb2 = xw.Book(excel_name)  # 建立excel表连接

    sheets_name= [st.name for st in wb2.sheets]
    for st in  sheets_name:
        sheet2 = wb2.sheets[st]
        sheet2[0:row,0:col].font.name = '微软雅黑'# 设置字体格式为微软雅黑
        #sheet2[0:row, 0:col].api.HorizontalAlignment = '-4108'  #设置字体居中
        #sheet2[:,17].number_format = '$1,234'    #“单价”这一列单元格设置为分割格式显示
        sheet2[:,13].font.color = (0, 150, 255) #设置标签列颜色为绿色
        for i in range(row): ##行遍历
                if i==0:
                    sheet2[i, 0:col].color = (0, 150, 255) #设置标题背景颜色为蓝色
                    sheet2[i, 0:col].font.color = (255, 255, 255) #设置标题字体颜色为白色
                    sheet2[i, 0:col].font.bold = True #设置为粗体
                elif i%2 ==0:
                    sheet2[i,0:col].color = [183, 222, 232]    #设置偶数行背景颜色格式为浅蓝色
        #for i,item in enumerate(format): #列遍历,根据sample.xlsx中的列宽进行调整
         #   sheet2[0,i].column_width = item
        sheet2.autofit()
    wb2.save()#保存excel
    wb2.close()#关闭excel
    return None


if __name__ == '__main__':
    excel_name = excel_path  + "苏州二手房数据.xlsx"#需要修改的excel名字
    row = 200 #需要修改格式的行数
    col = 18  ##需要修改格式的列数
    #format = get_template_format(col)
    beautiful_sheet(excel_name,row,col,format)