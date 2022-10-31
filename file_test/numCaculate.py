"""
读取数字，统计最大、最小、总数和平均值
"""

fin = open("/Users/joyce/kingfish-python/kingfish-python/file_test/number.txt")

max = 0
min = 10000
sumv = 0
count = 0

for line in fin:
    number = int(line.strip())
    if number > max:
        max = number
    elif number < max:
        min = number
    sumv += number
    count = count + 1
avg = sumv/count

fin.close()

print("max is ",max)
print("min is ",min)
print("sum is ",sumv)
print("avg is ",avg)

fout = open("output.txt","w")
fout.write("max is "+ str(max) + "\n")
fout.write("min is "+ str(min) + "\n")
fout.write("sum is "+ str(sumv) + "\n")
fout.write("avg is "+ str(avg) + "\n")

fout.close()
