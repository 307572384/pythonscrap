import pandas as pd

# 将列表转为df
table_df = pd.DataFrame(table_2[1:],columns=table_2[0])

# 保存excel
table_df.to_excel('test.xlsx')

table_df