import pandas as pd

# 设置当前绝对路径绝对路径（注意：最后是两个斜线！）
PATH = r'C:\Users\tianyunchuan\iCloudDrive\_spyder_\survey\Correspondense\ca_prince_sample\\'
RAWDATA_FILENAME = 'data_ca_sample'

df = pd.read_excel('{}{}.xlsx'.format(PATH,RAWDATA_FILENAME), index_col=0)
# df = pd.read_excel(r'C:\Users\tianyunchuan\iCloudDrive\Desktop\_pyCodeSpyder_\survey\Correspondense\ca_prince_sample\data_ca_sample.xlsx', index_col=0)
# df = pd.read_excel('./data_ca_sample.xlsx', index_col=0)


import prince
ca = prince.CA(n_components=2,n_iter=3,copy=True,check_input=True,     engine='auto',random_state=42)
# df.columns.rename('Hair color', inplace=True)
# df.index.rename('Eye color', inplace=True)
ca = ca.fit(df)

ca.row_coordinates(df)
ca.column_coordinates(df)    

import matplotlib
import matplotlib.pyplot as plt
font = {'size': 10,'family': 'SimHei'}
matplotlib.rc('font', **font)
plt.rcParams['axes.unicode_minus'] = False 

ax = ca.plot_coordinates(df=df,ax=None,figsize=(6, 6),x_component=0,y_component=1,show_row_labels=True,show_col_labels=True)
# ax.get_figure().savefig('./ca_coordinates.svg')
# ax.get_figure().savefig('./ca_coordinates.png')
ax.get_figure().savefig('{}{}'.format(PATH,'ca_coordinates.png'))


def save_to_excel():
    with pd.ExcelWriter('{}{}'.format(PATH,'factor_weight.xlsx')) as _writer:
        # list_sheet_name = ['result_code_list.xlsx','result_data.xlsx']
        ca.row_coordinates(df).to_excel(_writer, sheet_name= 'row')
        ca.column_coordinates(df).to_excel(_writer, sheet_name= 'column')
    _writer.save()
    _writer.close()
save_to_excel()




## delete columns （如需删除列）
print(df.columns)
def del_column(*args):
    for s in args:    
        try:        
            del df[s]
        except Exception:
            print('没有「{}」这个选项'.format(s))
# 输入需删除的列名的list
del_column(*['有品位的','美味的'])



