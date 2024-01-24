
import os
from pathlib import Path

#定义要整理的文件格式
FILE_FORMATS={
    "图片":[".jpg",".jpeg",".bpm",'.png','.gif'],
    "文档":[".doc",".docx",".xls",".xlsx",".ppt",".pptx",".pdf",".txt",".md"],
    "视频":[".mp4","avi","wmv",],
    "音频":[".mp3"],
    "压缩":[".rar",".zip",".tar",".gz",".7z","bz"],
    "脚本":[".ps1",".sh",".bat",".py"],
    "可执行文件":['.exe','.msi'],
    "网页文件":['.html','.xml','.mhtml','.html'],
    "快捷方式":[".lnk"],
}

#定义要整理的文件夹
orgPath='/Users/joyce/Desktop/data/'

#循环整理文件夹
for myfile in os.scandir(orgPath):    
    #跳过file
    if myfile.is_dir():        
        print('%s是文件夹'%myfile)        
        continue
    #输出要整理的文件名
    print('整理文件:%s'%myfile.name)
    file_path=Path(orgPath +'/'+ myfile.name)
    lower_file_path=file_path.suffix.lower()    

    #循环遍历我们定义的格式类型
    for format in FILE_FORMATS:        
        if lower_file_path in FILE_FORMATS[format]:
            directory_path=Path(orgPath+'/'+format)
            directory_path.mkdir(exist_ok=True)
            file_path.rename(directory_path.joinpath(myfile.name))

print('文件整理已完成！')



