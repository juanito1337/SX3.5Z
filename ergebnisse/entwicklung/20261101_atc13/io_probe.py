import os, json, time
p=r"C:\Users\1337\Documents\ChatGPT\SX3.5Z\cad\nx\SX35Z_CNC_KONZEPT_13_SEITENMAGAZIN_PARK_20261101_195816_194619_851deb3d9dea\io_reproduction.json"
for i in range(1000):
 with open(p,'w',encoding='utf8') as f: json.dump({'iteration':i,'data':'x'*100000},f)
print('IO_STRESS_PASS 1000 rewrites')
