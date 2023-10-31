import os
import requests
import configparser

def download_web_pages(config):
    web_pages = config['web_pages']
    if not os.path.exists('py'):
        os.makedirs('py')
    for page_name, url in web_pages.items():
        try:
            # 发送HTTP请求获取网页内容
            response = requests.get(url)
            if response.status_code == 200:
                # 保存网页内容到以页面名命名的文件中
                with open(f'py/{page_name}', 'w', encoding='utf-8') as file:
                    file.write(response.text)
                print(f'{page_name} 下载成功')
            else:
                print(f'{page_name} 下载失败，HTTP 状态码：{response.status_code}')
        except Exception as e:
            print(f'{page_name} 下载失败，错误：{str(e)}')

def generate_config_file():
    config = configparser.ConfigParser()
    config.add_section('test')
    
    # 设置 [test] 部分的选项
    config.set('test', 'path', '原始.conf')
    config.set('test', 'target', 'clash')
    config.set('test', 'sort', 'true')
    
    # 获取下载的文件路径
    downloaded_files = os.listdir('py')
    downloaded_files = [f'py/{file}' for file in downloaded_files]
    url = '|'.join(downloaded_files)
    config.set('test', 'url', url)
    
    # 保存配置文件
    with open('generate.ini', 'w') as configfile:
        config.write(configfile)
    
    print('generate.ini 文件已生成')

# 读取配置文件
Url = configparser.ConfigParser()
Url.read('Url.conf')

# 下载网页内容
download_web_pages(Url)

# 生成配置文件
generate_config_file()

import subprocess
subconverter_path = r'.\subconverter.exe'
subprocess.run([subconverter_path, '-g'], check=True)
print("subconverter.exe 已成功运行并生成配置文件。")

def process_config_file(input_file, output_file):
    try:
        # 创建一个名为 my_list 的空列表
        my_list = []

        # 打开输入文件进行读取
        with open(input_file, 'r', encoding='utf-8') as file:
            # 逐行读取文件并将每一行的内容添加到 my_list 中
            for line in file:
                my_list.append(line.strip())  # 使用 strip() 去除行末的换行符

        # 删除第一行
        del my_list[0]

        # 删除最后两行
        del my_list[-1]
        del my_list[-1]

        # 遍历列表中的每一项并删除前两个字符
        for i in range(len(my_list)):
            my_list[i] = my_list[i][2:]

        # 创建一个名为输出文件的文件，并将处理后的 my_list 写入文件中
        with open(output_file, 'w', encoding='utf-8') as debug_file:
            # 在第一行写入 "Proxy:" 并换行
            debug_file.write("Proxy:\n")

            # 将处理后的 my_list 写入文件中，每行加上 "-"
            for line in my_list:
                debug_file.write(f"  - {line}\n")

            # 在最后两行写入 "Proxy Group: ~" 和 "Rule:"
            debug_file.write("Proxy Group: ~\n")
            debug_file.write("Rule:\n")

        print(f"{output_file} 文件已生成")
    except Exception as e:
        print(f"处理配置文件时出错：{e}")

# 调用函数处理配置文件
#process_config_file('原始.conf', '调试.conf')
#import re
def extract_and_remove_duplicates(input_file, output_file):
    try:
        # 创建一个集合来存储唯一的 UUID
        unique_uuids = set()

        # 打开输入文件进行读取
        with open(input_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # 创建一个列表来存储去重后的行
        deduplicated_lines = []

        # 使用正则表达式识别 UUID，并将不重复的行添加到 deduplicated_lines 列表中
        uuid_pattern = r'uuid:\s*([0-9a-fA-F-]+)'
        for line in lines:
            match = re.search(uuid_pattern, line)
            if match:
                uuid = match.group(1)
                if uuid not in unique_uuids:
                    deduplicated_lines.append(line)
                    unique_uuids.add(uuid)

        # 创建一个名为输出文件的文件，并将去重后的行写入文件中
        with open(output_file, 'w', encoding='utf-8') as debug_file:
            for line in deduplicated_lines:
                debug_file.write(line)

        print(f"{output_file} 文件已生成")
    except Exception as e:
        print(f"处理文件时出错：{e}")
# 调用函数提取 UUID 并去重
#extract_and_remove_duplicates('原始.conf', '去重后的.conf')
