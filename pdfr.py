# 导入pdfplumber
import pdfplumber

# 读取pdf文件，保存为pdf实例
pdf =  pdfplumber.open("E:\三位一体计划\三位\升级\创业开公司\营养师配餐系统\营养师各种表\\脂溶性维生素和水溶性维生素的RNIs.pdf")

# 访问第二页
first_page = pdf.pages[0]

# 自动读取表格信息，返回列表
table = first_page.extract_table()
text = first_page.extract_text()
print(table)
print(text)
# import pandas as pd
#
# # 将列表转为df
# table_df = pd.DataFrame(table_2[1:],columns=table_2[0])
#
# # 保存excel
# table_df.to_excel('test.xlsx')
#
# table_df