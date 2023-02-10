import time
from selenium import webdriver
# from selenium.webdriver import Chrome, ChromeOptions
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# opt = ChromeOptions()            # 创建Chrome参数对象
# opt.headless = False            # 把Chrome设置成可视化无界面模式，windows/Linux 皆可
# driver = Chrome(options=opt)
# driver.get('https://www.pexels.com/zh-cn/photo/931177/')
# ab = driver.find_element(By.XPATH,'//*[@id="__next"]/main/div/div[2]/div/div/img').get_attribute('src')
# print(ab)
# import requests
# # dowlimg = requests.get(ab)
# # open('imgtest.jpeg','wb').write(dowlimg.content)
# # driver.close()
# url = 'https://pdf.dfcfw.com/pdf/H2_AN202302051582783380_1.pdf?1675614279000.pdf'
# dowlimg = requests.get(url)
# open('PDF.pdf','wb').write(dowlimg.content)
url = "https://img-blog.csdnimg.cn/f6c50979184e417babde47d8f8fbd58e.png#pic_center"
# driver.close()
import random
import wget
url = "https://pdf.dfcfw.com/pdf/H2_AN202302051582783380_1.pdf?1675614279000.pdf"
wget.download(url,'pdf1.pdf')
import urllib
url = "https://pdf.dfcfw.com/pdf/H2_AN202302051582783380_1.pdf?1675614279000.pdf"
urllib.request.urlretrieve(url, 'img1.jpeg')