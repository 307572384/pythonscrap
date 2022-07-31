import os
import sys
import time
import pandas as pd
from struct import unpack
# 获取当前目录
proj_path = os.path.dirname(os.path.abspath(sys.argv[0])) + ''

def transform_data():
    # 保存csv文件的目录
    target = proj_path + '/day'
    if not os.path.exists(target):
        os.makedirs(target)
    code_list = []
    source_list = ['D:/twx/vipdoc/sh/lday','D:/twx/vipdoc/sz/lday']
    for source in source_list:
        file_list = os.listdir(source)
        # 逐个文件进行解析
        for f in file_list:
            day2csv(source, f, target)
        # 获取所有股票/指数代码
        code_list.extend(list(map(lambda x: x[:x.rindex('.')], file_list)))
    # 保存所有代码列表
    pd.DataFrame(data=code_list, columns=['code']).to_csv(proj_path + 'data/all_codes.csv', index=False)
# 将通达信的日线文件转换成CSV格式
def day2csv(source_dir, file_name, target_dir):
    # 以二进制方式打开源文件
    source_file = open(source_dir + os.sep + file_name, 'rb')
    # print(source_file)
    buf = source_file.read()
    source_file.close()

    # 打开目标文件，后缀名为CSV
    target_file = open(target_dir + os.sep + file_name[: file_name.rindex('.')] + '.csv', 'w')
    buf_size = len(buf)
    rec_count = int(buf_size / 32)
    begin = 0
    end = 32
    header = str('date') + ',' + str('open') + ',' + str('high') + ',' + str('low') + ',' \
             + str('close') + ',' + str('amount') + ',' + str('volume') + '\n'
    target_file.write(header)
    for i in range(rec_count):
        # 将字节流转换成Python数据格式
        # I: unsigned int
        # f: float
        a = unpack('IIIIIfII', buf[begin:end])
        # 处理date数据
        year = a[0] // 10000
        month = (a[0] % 10000) // 100
        day = (a[0] % 10000) % 100
        date = '{}-{:02d}-{:02d}'.format(year, month, day)

        line = date + ',' + str(a[1] / 100.0) + ',' + str(a[2] / 100.0) + ',' \
               + str(a[3] / 100.0) + ',' + str(a[4] / 100.0) + ',' + str(a[5]) + ',' \
               + str(a[6]) + '\n'
        target_file.write(line)
        begin += 32
        end += 32
    target_file.close()
def re_code():
    gswo_path = r'D:/PythonProjec/pythonscrap/day'
    save_path = r'D:/PythonProjec/pythonscrap/save'
    list = []
    for i in os.listdir(gswo_path):
        list.append(i)
    name = ['A股代码文件名']
    df = pd.DataFrame(columns=name, data=list)
    df.to_csv(save_path + 'A_code.csv')
    print('已完成全部转换并将文件保存到'+save_path)

if __name__ == '__main__':
    # 程序开始时的时间
    time_start = time.time()

    # 获取所有股票代码
    # get_all_stock_codes()

    # 转换所有数据
    transform_data()
    re_code()

    # 更新数据
    # update_data()

    # 程序结束时系统时间
    time_end = time.time()

    print('程序所耗时间：', time_end - time_start)