# 'name': 'A股上市公司季报、年报、半年报',
# https://data.eastmoney.com/notices/hsa/1.html
# 这个功能可以存着就做月度调研的时候使用就行
import os
import os
import urllib.request
import socket
import sys
import logging
import re,string
import os
import os
import urllib.request
import socket
import sys
import logging
import re,string
import time
import pymysql
import requests
import win32gui
import ast
import xlrd
import win32api
import win32con
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome, ChromeOptions
from gridfs import GridFS
from pymongo import MongoClient
import sys
# A股年报下载器
#连接MongoDB数据库
client= MongoClient('mongodb://localhost:27017/')
db = client['Areport']
# 输入你要爬取的行业
f_industry ='证券'
f_a = '.xls'
f_b = 'D:/A股所有行业数据/'
f_c = f_b+f_industry+f_a

# 获取xlxs里面的股票代码
data = xlrd.open_workbook(f_c,formatting_info=True)
# 获取到表
sheet2 =data.sheet_by_name(f_industry)
path1 = r'E:\Areport\\'
patha = path1+f_industry+'\\'

# patha=r'E:\Areport\医药商业\\'
# 下载的地址
sava_path1 = 'E:\Areport\\'
sava_path2 = '\\'
save_patha=sava_path1 + f_industry+sava_path2
# 打印print到指定文件地址txt中
# 获取列数据
cell0 = sheet2.cell(0,0)
# 获取第一行第一列的数据
lie = [str(sheet2.cell_value(i, 0)) for i in range(1, sheet2.nrows)]
# 去除列中的英文
reportlist = re.sub('[a-zA-Z]','',str(lie))
reportlist1 = ast.literal_eval(reportlist)
# 2.0版本使用urlib下载文件全程无需管理

opt = ChromeOptions()            # 创建Chrome参数对象
opt.headless = True              # 把Chrome设置成可视化无界面模式，windows/Linux 皆可
# driver = Chrome(options=opt)     # 创建Chrome无界面对象
# # Chrome浏览器
driver = webdriver.Chrome()
linex= []
att= []
def index():
        # #按回车继续
    driver.find_element(By.XPATH, "/html/body/div[1]/div[8]/div[2]/div[2]/div[2]/div/form/input[2]").click()
    time.sleep(3)
        # 跳转新的窗口否则无法找到新的标签
    driver.switch_to.window(driver.window_handles[-1])
    driver.find_element(By.XPATH, "/html/body/div[1]/div[8]/div[5]/div[2]/div/div[1]/ul/li[3]").click()
    time.sleep(3)
    driver.find_element(By.XPATH, " // *[ @ id = 'filter_s_node'] / li[5]").click()
    time.sleep(3)
    # 定位到外框的table使用xpath进行完整的地址定位
    report_list=driver.find_elements(By.CSS_SELECTOR, "table tbody tr  td:nth-child(1) div.ellipsis a")
    for li  in report_list:
            line = li.get_attribute('href')
            # line = li.find_element(By.CLASS_NAME,'ellipsis').click()
            # 将获取到的超链接调入selenium进行点击
            driver.execute_script(f'window.open("{line}","_blank");')
            # 检测新窗口
            driver.switch_to.window(driver.window_handles[-1])
            # 获取报告标题
            # A_title = driver.find_element(By.XPATH,'/html/body/div[1]/div[8]/div[3]/div[1]/div[1]/div[1]/span')
            # A_title_text = A_title.get_attribute('text')
            A_title = driver.find_element(By.CSS_SELECTOR,'span.title_text').text
            # A股代码
            A_code = driver.find_element(By.CSS_SELECTOR,'div.name b').text
            # 股票名称
            A_name = driver.find_element(By.CSS_SELECTOR, 'div.name span').text
            # 公告日期
            A_time = driver.find_element(By.CSS_SELECTOR,'div.ggdate span').text
            # 下载pdf的地址
            A_down_file_url = driver.find_element(By.CSS_SELECTOR,"div.title_box a.pdf-link").get_attribute('href')
            # A_down_file_url = driver.find_element_by_css_selector("a.pdf-link")
            time.sleep(2)
            Atitlename = A_title + '.pdf'
            namechangea =  Atitlename.replace(':', ' ').replace('*ST','')
            namechangeb = namechangea.replace('*', '').replace('(','').replace('/','').replace(')','').replace('>','').replace('【','').replace('】','').replace('、','').replace('《','').replace('》','').replace('"','').replace('，','').replace('：','').replace('|','').replace('\\','').replace('<','')
            A_name_ch = A_name.replace('*', '').replace('(','').replace('/','').replace(')','').replace('>','').replace('【','').replace('】','').replace('、','').replace('《','').replace('》','').replace('"','').replace('，','').replace('：','').replace('|','').replace('\\','').replace('<','').replace('*ST','')
            pathc = patha + A_name_ch
            if not os.path.exists(pathc):
                os.makedirs(pathc)
            A_nameb = A_name_ch+'\\'
            time.sleep(2)
            # 下载文件将文件名字转换成urllib内可识别的名字
            save_pathb=save_patha+A_nameb+namechangeb
            requests.DEFAULT_RETRIES = 5
            requests.packages.urllib3.disable_warnings()
            r = requests.get(A_down_file_url, verify=False)
            with open(save_pathb, 'wb') as f:
                f.write(r.content)
            # 直接将A股的名称转进去mongodb，自动创建储存桶
            gfs = GridFS(db, collection=A_name)
            # 下载后本地地址
            # 将文件写入Mongodb中的grid
            file = open(save_pathb, "rb")
            seargs = {"content_type":A_name, "md5": A_code}
            if seargs == []:
                continue
            else:
                gfs.put(file, filename=namechangeb, **seargs)
            file.close()
            driver.close()
            driver.switch_to.window(driver.window_handles[-1])
    driver.close()
# 翻页功能，selenium模拟键盘自动翻页
# for j in range(1):
#         index()
#         driver.implicitly_wait(5)
#         # driver.switch_to.window(driver.window_handles[-1])
#         #页面点击跳转下一页，因为无法识别到li里面的标签所以就用键盘右键换页的方法替代
#         ActionChains(driver).key_down(Keys.CONTROL).send_keys(Keys.RIGHT).key_up(Keys.CONTROL).perform()
#
#         time.sleep(5)


if __name__ == "__main__":

    # 使用for循环去重复输入表内的股票代码并下载
    for adown in reportlist1:
            driver.get("https://data.eastmoney.com/notices/hsa/1.html")
            print(adown)
            # 输入A股的上市公司的代码
            driver.find_element(By.XPATH, "/html/body/div[1]/div[8]/div[2]/div[2]/div[2]/div/form/input[1]").send_keys(adown)
            time.sleep(3)
            index()
            driver.switch_to.window(driver.window_handles[-1])
    driver.refresh()
    driver.quit()


