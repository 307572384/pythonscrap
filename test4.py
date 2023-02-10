# 'name': '财经要闻',
#                     # 同花顺财经要闻http://news.10jqka.com.cn/today_list/

import time
import pymysql
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from apscheduler.schedulers.blocking import BlockingScheduler
# 同花顺-财经要闻

                    # https://kuaixun.eastmoney.com/dq_zg.html
from selenium.webdriver import Chrome, ChromeOptions

conn = pymysql.connect(host='localhost',  # host属性
                       port=3306,  # 端口号
                       user='root',  # 用户名
                       password='123456Aa',  # 此处填登录数据库的密码
                       db='rollbacksystem', # 数据库名
                       charset='utf8'
                       )


opt = ChromeOptions()            # 创建Chrome参数对象
opt.headless = True              # 把Chrome设置成可视化无界面模式，windows/Linux 皆可
# Chrome浏览器
driver = webdriver.Chrome()
driver.get("http://news.10jqka.com.cn/today_list/")
def index():
    # 设置等待5秒，避免爬虫时被封禁
    driver.implicitly_wait(5)
    # 找到外框的获取里面所有的li标签
    lis = driver.find_elements_by_css_selector(".list-con ul li")
    for i,li  in enumerate(lis):

            # 获取url
            line = li.find_element_by_css_selector("a.arc-cont").get_attribute('href')
            b = time.strftime('%Y', time.localtime(time.time()))
            f = '年'
            time24 = li.find_element_by_css_selector('.arc-title span').text
            d = b + f + time24
            newtext = li.find_element_by_css_selector(".arc-cont").text
            print(d,line,newtext)
            # 获取一个光标
            cursor = conn.cursor()
            # 插入数据,insert into 表（列名，列名，列名）values(值，值，值)这个值主要就是对应的你获取到的值
            sql = 'insert into quantizationsystem_new_finace(new_f_time,new_f_sources,new_f_content) values(%s,%s,%s);'
            # 对获取到的数据进行排序如果有重复的则进行筛除
            data_list=[d,line,newtext]

            list2 = sorted(list(set(data_list)), key=data_list.index)

            try:
             # 插入数据
             cursor.execute(sql,list2)
            # 连接数据
             conn.commit()
             print('插入数据成功')
            except Exception as e:
                     print('插入数据失败')
                     conn.rollback()
            time.sleep(5)
    conn.close()
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
