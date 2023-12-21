import json
import subprocess
import sys
import base64
sys.stdout.reconfigure(encoding="utf-8")
# 定义字典
data = {
    "group": "job",
    "speedtestMode": "all",
    "pingMethod": "googleping",
    "sortMethod": "rspeed",
    "concurrency": 200,
    "testMode": 2,
    "subscription": "https://raw.githubusercontent.com/Leon406/SubCrawler/main/sub/share/all3",
    "timeout": 16,
    "language": "en",
    "fontSize": 24,
    "theme": "rainbow",
    "outputMode": 3,
    "unique": True,
}

# 将字典转换为JSON格式
json_data = json.dumps(data, indent=4)
output_data = "config.json"
# 将JSON数据写入文件
with open(output_data, "w", encoding="utf-8") as json_file:
    json_file.write(json_data)
print("JSONOK")
cmd = f"lite.exe --config {output_data} --test {data['subscription']}"

process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
process.communicate()

with open("output.json", "r", encoding="utf-8") as file:
    data = json.load(file)

proxy = ""
values = data[list(data.keys())[0]]
for value in values:
    out_proxy = ""
    if value["avg_speed"] > 1024 * 100:
        out_proxy = proxy
        proxy = out_proxy + value["link"] + "\n"
import base64

def url_to_base64(url):
    # 将链接转换为字节串
    url_bytes = url.encode('utf-8')
    
    # 使用base64编码
    base64_encoded = base64.b64encode(url_bytes)
    
    return base64_encoded.decode('utf-8')  # 将字节串转换为字符串并返回
base64_encoded_url = url_to_base64(proxy)
with open("proxy.txt", "w", encoding="utf-8") as a:
    a.write(base64_encoded_url)
