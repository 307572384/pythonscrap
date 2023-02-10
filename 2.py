import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
opt = ChromeOptions()            # 创建Chrome参数对象
opt.headless = True              # 把Chrome设置成可视化无界面模式，windows/Linux 皆可
driver = webdriver.Chrome()# Chrome浏览器
driver.get("https://hui.fang.anjuke.com/loupan/all/a1_m94-95_o8_w1_z3/")
time.sleep(5)
def scrach():
    sc = driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/div[1]/div[3]')
    fw = sc.find_elements(By.CLASS_NAME,'item-mod')
    for i in fw:
        print(i)
        url = i.find_element(By.CLASS_NAME,'pic').get_attribute('href')
        house_name = i.find_element(By.CSS_SELECTOR,'.items-name').text
        house_address = i.find_element(By.CSS_SELECTOR, '.list-map').text
        price = i.find_element(By.CSS_SELECTOR, '.price').text
        time.sleep(5)
        driver.execute_script(f'window.open("{url}","_blank");')
        time.sleep(5)
        driver.switch_to.window(driver.window_handles[-1])
        tr = driver.find_element(By.XPATH,'/html/body/div[2]/div[26]/div[3]/div[2]/ul/li[1]/a').text
        bs = driver.find_element(By.XPATH, '/html/body/div[2]/div[26]/div[3]/div[2]/ul/li[2]/a').text
        edu = driver.find_element(By.XPATH, '/html/body/div[2]/div[26]/div[3]/div[2]/ul/li[3]/a').text
        hos = driver.find_element(By.XPATH, '/html/body/div[2]/div[26]/div[3]/div[2]/ul/li[4]/a').text
        print(tr,bs,edu,hos)
        dict ={"楼盘名称": house_name,
                           "楼盘地址": house_address,
                           "楼盘均价": price,
                           "公交经过数量": tr,
                           "附近购物数量": bs,
                           "附近学校数量": edu,
                           "附近医院数量": hos}
        df = pd.DataFrame.from_dict(dict,orient='index').T
        df.to_excel("惠州楼房分析.xlsx", encoding="utf-8", index=None)
        driver.close()
        driver.switch_to.window(driver.window_handles[-1])



if __name__ == "__main__":
    scrach()