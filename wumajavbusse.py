import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from selenium.webdriver import Chrome, ChromeOptions
# 无码女优
f = open("javbussemg.csv", "w", encoding="utf-8", newline="")
csv.writer(f).writerow(["磁力"])
# driver = webdriver.Chrome()
opt = ChromeOptions()            # 创建Chrome参数对象
# opt.headless = True              # 把Chrome设置成可视化无界面模式，windows/Linux 皆可
driver = Chrome(options=opt)     # 创建Chrome无界面对象




driver.get("https://www.javbus.com/")

driver.find_element(By.XPATH,'//*[@id="navbar"]/ul[1]/li[2]/a').click()
#输入无码女优名字
driver.find_element(By.XPATH,"/html/body/nav/div/div[2]/div/div/input").send_keys("源みいな")
#按回车继续
driver.find_element(By.XPATH,"/html/body/nav/div/div[2]/div/div/input").send_keys(Keys.ENTER)
driver.implicitly_wait(5)
# 第一次搜索的页面一定要关掉不然selenium会默认把第一次搜索的页面数据给拿下来
driver.close()

#waterfall > div:nth-child(1)
def index():
    driver.implicitly_wait(5)
    #跳转新的窗口否则无法找到新的标签
    driver.switch_to.window(driver.window_handles[-1])
    sreach_windows3 = driver.current_window_handle
    lis = driver.find_element(By.CSS_SELECTOR,"#waterfall div item masonry-brick")
    for i,lis1  in enumerate(lis):
        # 获取页面框里面的url
        line = lis1.find_element_by_css_selector("a.movie-box").get_attribute('href')

        print(line)
        # 将获取到的超链接调入selenium进行点击
        driver.execute_script(f'window.open("{line}","_blank");')
        driver.implicitly_wait(5)
        # 检测新窗口
        driver.switch_to.window(driver.window_handles[-1])
        # 获取磁力链接
        link = driver.find_element_by_xpath("//*[@id='magnet-table']/tr[1]/td[1]/a[1]")
        a = link.get_attribute('href')
        # 将获取到的磁力链接写入进csv中
        csv.writer(f).writerow([a])
        # 新的窗口关闭
        driver.close()
        time.sleep(5)
        # 之前开启用来获取磁力链接的窗口已经关闭，返回原来的窗口需要重新失败为新窗口，这是个很奇怪的设置大概是因为原先的窗口已经关闭老的窗口因为还存在跳回原来的窗口时就是代表着是新的窗口
        driver.switch_to.window(driver.window_handles[-1])
#        range是需要手动设置因为暂时无法判断究竟最大页面是多少容易导入重复数据。
for j in range(4):
        index()
        driver.implicitly_wait(5)
        # driver.switch_to.window(driver.window_handles[-1])
        #页面点击跳转下一页，因为无法识别到li里面的标签所以就用键盘右键换页的方法替代
        ActionChains(driver).key_down(Keys.CONTROL).send_keys(Keys.RIGHT).key_up(Keys.CONTROL).perform()

        time.sleep(5)
        # print('第'+j+'页')







