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
# A股研报下载
#连接MongoDB数据库
client= MongoClient('mongodb://localhost:27017/')
db = client['Areport']

# 2.0版本使用urlib下载文件全程无需管理
# 下载的地址
save_patha='E:\\researchReport\\'

opt = ChromeOptions()            # 创建Chrome参数对象
opt.headless = True              # 把Chrome设置成可视化无界面模式，windows/Linux 皆可
# driver = Chrome(options=opt)     # 创建Chrome无界面对象
# # Chrome浏览器
driver = webdriver.Chrome()
linex= []
att= []
def index():

    # 定位到外框的table使用xpath进行完整的地址定位
    # lis = driver.find_element(By.XPATH,'/html/body/div[1]/div[8]/div[2]/div[5]/table/tbody')
    # report_list = lis.find_elements_by_tag_name("//*[@id=“industry_table”]/td[5]")
    lis = driver.find_element(By.XPATH, '//*[@id=“industry_table”]/td[5]')
    for li  in lis:
            # report_url = driver.find_element(By.XPATH, '/html/body/div[1]/div[8]/div[2]/div[5]/table/tbody/tr[1]/td[5]/a')
            line = li.get_attribute('href')
            print(line)
            # line = li.find_element(By.CLASS_NAME,'ellipsis').click()
            # 将获取到的超链接调入selenium进行点击
            driver.execute_script(f'window.open("{line}","_blank");')
            # 检测新窗口
            driver.switch_to.window(driver.window_handles[-1])
            # 获取报告标题
            # A_title = driver.find_element(By.XPATH,'/html/body/div[1]/div[8]/div[3]/div[1]/div[1]/div[1]/span')
            # A_title_text = A_title.get_attribute('text')
            A_title = driver.find_element_by_css_selector('span.title_text').text
            # A股代码
            A_code = driver.find_element(By.CSS_SELECTOR,'div.name b').text
            # 股票名称
            A_name = driver.find_element(By.CSS_SELECTOR, 'div.name span').text
            # 公告日期
            A_time = driver.find_element(By.CSS_SELECTOR,'div.ggdate span').text
            # 下载pdf的地址
            A_down_file_url = driver.find_element_by_css_selector("div.title_box a.pdf-link").get_attribute('href')
            # A_down_file_url = driver.find_element_by_css_selector("a.pdf-link")
            print(A_down_file_url)
            time.sleep(2)
            Atitlename = A_title + '.pdf'
            namechangea =  Atitlename.replace(':', ' ')
            namechangeb = namechangea.replace('*', '').replace('(','').replace('/','').replace(')','')
            time.sleep(2)
            # 下载文件将文件名字转换成urllib内可识别的名字
            save_pathb=save_patha+namechangeb
            print(save_pathb)
            # 使用urllib来下载文件,文件下载
            urllib.request.urlretrieve(A_down_file_url, save_pathb)
            time.sleep(2)
            # 直接将A股的名称转进去mongodb，自动创建储存桶
            gfs = GridFS(db, collection=A_name)
            # 下载后本地地址
            # 将文件写入Mongodb中的grid
            file = open(save_pathb, "rb")
            seargs = {"content_type":A_name, "md5": A_code}
            gfs.put(file, filename=namechangeb,**seargs)
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
        index()
