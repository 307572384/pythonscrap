# 'name': 'A股上市公司季报、年报、半年报',
# https://data.eastmoney.com/notices/hsa/1.html
# 这个功能可以存着就做月度调研的时候使用就行
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
#连接MongoDB数据库
client= MongoClient('mongodb://localhost:27017/')
db = client['yourmongodb data']
# 获取xlxs里面的股票代码
data = xlrd.open_workbook("D:/A股所有行业数据/白色家电.xls",formatting_info=True)
# 获取到表
sheet2 =data.sheet_by_name('白色家电')
# 获取列数据
cell0 = sheet2.cell(0,0)
# 获取第一行第一列的数据
lie = [str(sheet2.cell_value(i, 0)) for i in range(1, sheet2.nrows)]
# 去除列中的英文
reportlist = re.sub('[a-zA-Z]','',str(lie))
reportlist1 = ast.literal_eval(reportlist)
# 1.0版本模拟人工智能点击下载连接


VK_CODE ={'enter':0x0D, 'down_arrow':0x28}
#键盘键按下
def keyDown(keyName):
    win32api.keybd_event(VK_CODE[keyName], 0, 0, 0)
#键盘键抬起
def keyUp(keyName):
    win32api.keybd_event(VK_CODE[keyName], 0, win32con.KEYEVENTF_KEYUP, 0)

opt = ChromeOptions()            # 创建Chrome参数对象
opt.headless = True              # 把Chrome设置成可视化无界面模式，windows/Linux 皆可
# Chrome浏览器
driver = webdriver.Chrome()
linex= []
att= []


def index():
        # #按回车继续
    driver.find_element(By.XPATH, "/html/body/div[1]/div[8]/div[2]/div[2]/div[2]/div/form/input[2]").click()
    time.sleep(5)
        # 跳转新的窗口否则无法找到新的标签
    driver.switch_to.window(driver.window_handles[-1])
    driver.find_element(By.XPATH, "/html/body/div[1]/div[8]/div[5]/div[2]/div/div[1]/ul/li[3]").click()
    time.sleep(5)

        # driver.find_element(By.XPATH, "/html/body/div[1]/div[8]/div[5]/div[2]/div/div[2]/ul/li[5]").click()
    driver.find_element(By.XPATH, " // *[ @ id = 'filter_s_node'] / li[5]").click()
    time.sleep(5)
    # 获取报告的url
    # line =driver.find_element(By.XPATH, '//*[@id="dataview"]/div[2]/div[2]/table/tbody/tr[1]/td[1]/div/a')
    # b = line.get_attribute('href')

    # 找到外框的获取里面所有的li标签
    # lis = driver.find_elements(By.CSS_SELECTOR,"div.dataview-body table tbody tr")
    # 定位到外框的table使用xpath进行完整的地址定位
    lis = driver.find_element(By.XPATH,'/html/body/div[1]/div[8]/div[5]/div[2]/div/div[3]/div[2]/div[2]/table/tbody')
    # 定位tag标签，因为href的超链接是在a标签里面
    report_list = lis.find_elements_by_tag_name("a")
    for li  in report_list:
            line = li.get_attribute('href')
            print(line)
            # line = li.find_element(By.CLASS_NAME,'ellipsis').click()
            # 将获取到的超链接调入selenium进行点击
            driver.execute_script(f'window.open("{line}","_blank");')
            driver.implicitly_wait(5)

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
            # A_down_file_url = driver.find_element_by_css_selector("a.pdf-link").get_attribute('href')
            A_down_file_url = driver.find_element_by_css_selector("a.pdf-link")
            time.sleep(2)
            # 将鼠标移动到文件并右键
            action = ActionChains(driver).move_to_element(A_down_file_url)
            action.context_click(A_down_file_url).perform()
            # 谷歌浏览器按k保存文件
            win32api.keybd_event(75, 0, 0, 0)
            win32api.keybd_event(75, 0, win32con.KEYEVENTF_KEYUP, 0)
            time.sleep(2)
            # 使用win32gui.FindWindow找到目标程序
            win = win32gui.FindWindow('#32770',u'另存为')
            # 激活前端窗口
            win32gui.SetForegroundWindow(win)
            # 找到句柄窗口
            a1 = win32gui.FindWindowEx(win, None, "DUIViewWndClassName", None)
            a2 = win32gui.FindWindowEx(a1, None, "DirectUIHWND", None)
            a3 = win32gui.FindWindowEx(a2, None, "FloatNotifySink", None)
            a4 = win32gui.FindWindowEx(a3, None, "ComboBox", None)
            time.sleep(5)
            # 找到搜索框
            tid = win32gui.FindWindowEx(a4, None, 'Edit', None)
            # 将pdf名字保存下来,因为存入名字中的:在Google Chrome里面无法识别：所以需要把：字符改成空格
            Atitlename = A_title+'.pdf'
            namechange =Atitlename.replace(':',' ')
            # 将pdf名字传输进入框中
            win32gui.SendMessage(tid, win32con.WM_SETTEXT, None, namechange)
            time.sleep(5)
            # 按enter保存
            keyDown("enter")
            keyUp("enter")
            # 直接将A股的名称转进去，自动创建储存桶
            gfs = GridFS(db, collection=A_name)
            # 下载后本地地址
            in_url = 'C:/Users/MyPc/Downloads/'
            down = in_url+namechange
            time.sleep(5)
            # 将文件写入Mongodb中的grid
            file = open(down, "rb")
            seargs = {"content_type":A_name, "md5": A_code}
            gfs.put(file, filename=namechange,**seargs)
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
            time.sleep(5)
            index()
            driver.switch_to.window(driver.window_handles[-1])
        driver.close()


