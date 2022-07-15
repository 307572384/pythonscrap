import time
import pymysql
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from apscheduler.schedulers.blocking import BlockingScheduler
# 东方财富7x24小时
from selenium.webdriver import Chrome, ChromeOptions
# run函数
# def run():
#     print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))  # 输出当地时间
#     timer = threading.Timer(30, run)  # 设置一个定时器，循环输出时间
#     timer.start(index)  # 启动线程
#     print("爬虫再次启动")
# //连接数据库
conn = pymysql.connect(host='',  # host属性
                       port=,  # 端口号
                       user='',  # 用户名
                       password='',  # 此处填登录数据库的密码
                       db='study' , # 数据库名
                       charset='utf8'
                       )


# f = open("7x24小时新闻.csv", "w", encoding="utf-8", newline="")
# csv.writer(f).writerow(["时间", "新闻来源", "新闻内容"])
# driver = webdriver.Chrome()
opt = ChromeOptions()            # 创建Chrome参数对象
opt.headless = True              # 把Chrome设置成可视化无界面模式，windows/Linux 皆可
# Chrome浏览器
driver = webdriver.Chrome()
driver.get("https://kuaixun.eastmoney.com/")

def index():
    # 设置等待5秒，避免爬虫时被封禁
    driver.implicitly_wait(5)
    # 找到外框的获取里面所有的li标签
    lis = driver.find_elements_by_xpath("//*[@class='livenews-media']")
    for i,li  in enumerate(lis):
        # debug后发现lis里面len获取最大值是50，所以直接for循环给他控制在50次就退出操作
        if i < 50:
            # 获取url
            line = li.find_element_by_css_selector("a.media-title").get_attribute('href')
          # 获取时间，第一次获取text内容实用get_attribute发现获取的内容是空值，所以改用.text获取到值
          #   time24 = li.find_element_by_css_selector('span.time').get_attribute('text')
            time24 = li.find_element_by_css_selector('span.time').text
            # 获取本地时间
            b = time.strftime('%Y-%m-%d ', time.localtime(time.time()))
            # 与获取到的时间进行拼接获取可以进入数据库里面时间格式
            d = b + time24
            newtext = li.find_element_by_css_selector("a.media-title").get_attribute('text')
            print(d,line,newtext)
            # 获取一个光标
            cursor = conn.cursor()
            # 插入数据,insert into 表（列名，列名，列名）values(值，值，值)这个值主要就是对应的你获取到的值
            sql = 'insert into studyt(newtime,nsources,ncontent) values(%s,%s,%s);'
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
        else:
            driver.quit()
# 翻页功能，selenium模拟键盘自动翻页
for j in range(1):
        index()
        driver.implicitly_wait(5)
        # driver.switch_to.window(driver.window_handles[-1])
        #页面点击跳转下一页，因为无法识别到li里面的标签所以就用键盘右键换页的方法替代
        ActionChains(driver).key_down(Keys.CONTROL).send_keys(Keys.RIGHT).key_up(Keys.CONTROL).perform()

        time.sleep(5)


if __name__ == "__main__":
        index()
        # sched = BlockingScheduler()
        # sched.add_job(index, 'interval', seconds=30)
        # sched.start()



