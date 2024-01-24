import PyPDF2,os

#调用os.listdir()，找到当前工作目录中的所有文件，并去除非PDF 文档
pdfFiles = []
pdf_path = '/Users/joyce/Desktop/pdf/'
for filename in os.listdir(pdf_path):
    if filename.endswith('.pdf'):
        pdfFiles.append(filename)
        
#调用Python的sort()列表方法，将文档名按字母排序
pdfFiles.sort(key=str.lower)

#为输出的PDF文档创建PdfFileWriter 对象
pdfWriter = PyPDF2.PdfFileWriter()

#循环遍历每个PDF 文档，为它创建PdfFileReader 对象
for filename in pdfFiles:
    pdfFileObj = open(pdf_path + filename, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    
    #针对每个PDF 文档，循环遍历每一页
    #将页面添加到输出的PDF
    for pageNum in range(pdfReader.numPages):
        pageObj = pdfReader.getPage(pageNum)
        pdfWriter.addPage(pageObj)

#将输出的PDF写入一个文档，名为combinePdfs.pdf
pdfOutput = open(pdf_path+'面试宝典汇总.pdf', 'wb')
pdfWriter.write(pdfOutput)
pdfOutput.close()

