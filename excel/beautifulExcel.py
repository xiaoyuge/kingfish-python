import xlwings as xw

excel_path = '/Users/joyce/Desktop/excel/'

#美化表格
def beautiful_sheet(excel_name):
    # 建立excel表连接
    wb2 = xw.Book(excel_name)  

    sheets_name= [st.name for st in wb2.sheets]
    for st in  sheets_name:
        sheet2 = wb2.sheets[st]
        row = sheet2.used_range.rows.count
        col = sheet2.used_range.columns.count
        sheet2[0:row,0:col].font.name = '微软雅黑'# 设置字体格式为微软雅黑
        sheet2[0:row, 0:col].api.HorizontalAlignment = '-4108'  #设置字体居中
        sheet2[:,16].number_format = '¥#,##0_);(¥#,##0)'    #“单价”这一列单元格设置为分割格式显示
        sheet2[:,13].font.color = (0, 150, 255) #设置标签列颜色为绿色
        for i in range(row): ##行遍历
                if i==0:
                    sheet2[i, 0:col].color = (0, 150, 255) #设置标题背景颜色为蓝色
                    sheet2[i, 0:col].font.color = (255, 255, 255) #设置标题字体颜色为白色
                    sheet2[i, 0:col].font.bold = True #设置为粗体
                elif i%2 ==0:
                    sheet2[i,0:col].color = [183, 222, 232]    #设置偶数行背景颜色格式为浅蓝色
        #自适应宽度
        sheet2.autofit()
    wb2.save()#保存excel
    wb2.close()#关闭excel
    return None


if __name__ == '__main__':
    
    excel_name = excel_path  + "苏州二手房数据.xlsx"#需要修改的excel名字
   
    beautiful_sheet(excel_name)