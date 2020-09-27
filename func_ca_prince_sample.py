# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 10:57:18 2020
@author: tianyunchuan
"""

import pandas as pd
import prince
import matplotlib
import matplotlib.pyplot as plt


""" 定义路径、文件名 """
# 设置当前绝对路径绝对路径（注意：最后是两个斜线！）
PATH = r'C:\Users\tianyunchuan\iCloudDrive\_spyder_\survey\Correspondense\ca_prince_sample\\'
# 定义 excel 文件名
RAWDATA_FILENAME = 'data_ca_sample'


""" 数据导入 """
df = pd.read_excel('{}{}.xlsx'.format(PATH,RAWDATA_FILENAME), index_col=0)

# 绝对路径导入
#df = pd.read_excel(r'C:\Users\tianyunchuan\iCloudDrive\Desktop\_pyCodeSpyder_\survey\Correspondense\ca_prince_sample\data_ca_sample.xlsx', index_col=0)


""" Correpon过程函数 """
def proc_correpon(data):
    ##  实例化、fit
    ca = prince.CA(n_components=2,n_iter=3,copy=True,check_input=True,engine='auto',random_state=42)
    ## 非必须，定义行列名称
    data.columns.rename('Image', inplace=True)
    data.index.rename('Brand', inplace=True)
    ca = ca.fit(data)
    
    ## 获取 dim 1-2 数值
    result_rows = ca.row_coordinates(data)
    result_columns = ca.column_coordinates(data)    
    
    ##  生成图像
    font = {'size': 10,'family': 'SimHei'}
    matplotlib.rc('font', **font)
    plt.rcParams['axes.unicode_minus'] = False 
    
    ax = ca.plot_coordinates(X=data,ax=None,figsize=(6, 6),x_component=0,y_component=1,show_row_labels=True,show_col_labels=True)
    ax.get_figure().savefig('{}{}'.format(PATH,'ca_coordinates.png'))
    ax.get_figure().savefig('{}{}'.format(PATH,'ca_coordinates.svg'))
    
    
    ## 导出 dim 1-2 数值
    with pd.ExcelWriter('{}{}'.format(PATH,'factor_weight.xlsx')) as _writer:
        # list_sheet_name = ['result_code_list.xlsx','result_data.xlsx']
        ca.row_coordinates(data).to_excel(_writer, sheet_name= 'row')
        ca.column_coordinates(data).to_excel(_writer, sheet_name= 'column')
    _writer.save()
    _writer.close()
    
    return result_rows, result_columns

""" 调用 correspon 函数， 生成结果 """
result_rows, result_columns = proc_correpon(df)


#####################################################

""" delete columns （如需删除列、或行，如：品牌或选项） """
## 定义删除列函数
def del_column(list_args):
    df_del = df.copy()
    # 删除行
    df_del.drop(list_args[0],inplace=True)
    # 删除列
    df_del.drop(list_args[1], axis=1, inplace=True)
    return df_del


## 打印列内容，在右侧Console控制台有内容输出，方便复制粘贴选项内容
print(df.index)
print(df.columns)      
 
            
## 输入需删除的列名的list
# 需删除的行List
_list_del_rowName = ['品牌-A','品牌-C']
# 需要删除的列List
_list_del_colName = ['甜蜜的', '开心的', '温馨的', '注重健康的', '材料放心的', '亲切的', '有趣的/好玩的',]
# 待删除行列再生成列表
list_args = [_list_del_rowName,_list_del_colName]

## 执行函数，删除行列
df_del = del_column(list_args)

## 再次运行 correpon 过程函数，获取图片
result_rows_update, result_columns_update = proc_correpon(df_del)
