# -*- coding: utf-8 -*-
"""

@author: user
Created on Sat Nov 18 12:28:19 2023
"""

## 載入必要模組
import numpy as np
#import sys
import pandas as pd
import streamlit as st 
import streamlit.components.v1 as stc 


###### (1) 開始設定 ######
html_temp = """
		<div style="background-color:#3872fb;padding:10px;border-radius:10px">
		<h1 style="color:white;text-align:center;"> UCAN 八項共通職能資料查詢與比較 </h1>
		</div>
		"""
stc.html(html_temp)


###### (1) 讀取 excel or pkl檔案:    
df_ucan100To112_IndividualDepartmentCollegeSchool_original = pd.read_pickle('df_ucan100To112_IndividualDepartmentCollegeSchool.pkl')  ## [28741 rows x 44 columns]
#df_ucan100To112_IndividualDepartmentCollegeSchool_original = pd.read_excel('df_ucan100To112_IndividualDepartmentCollegeSchool.xlsx')  ## [28741 rows x 44 columns]
df_ucan100To112_IndividualDepartmentCollegeSchool = df_ucan100To112_IndividualDepartmentCollegeSchool_original.drop('姓名', axis=1)

###### (2) 挑選特定系所 各別共通職能落後名單 (低於系院校平均值) 
st.subheader("挑選特定系所 UCAN各別共通職能落後名單 (低於系院校平均值)")
##### 選擇系所
department_choice = st.selectbox('選擇系所', df_ucan100To112_IndividualDepartmentCollegeSchool['系所'].unique())

##### 選擇入學學年度
options_1 = ["100","101","102","103","104","105","106","107","108","109","110","112"]
入學年度 = st.selectbox("選擇入學學年度(111尚未調查)：", options_1)

##### 選擇特定共通職能
options_2 = ["溝通表達第1次","持續學習第1次","人際互動第1次","團隊合作第1次","問題解決第1次","創新第1次","工作責任及紀律第1次","資訊科技應用第1次"]
特定共通職能 = st.selectbox("選擇特定共通職能：", options_2)

##### 挑選某特定共通職能落後名單
cond_00 = (df_ucan100To112_IndividualDepartmentCollegeSchool['系所'] == department_choice)
cond_01 = (df_ucan100To112_IndividualDepartmentCollegeSchool['學號_first4'].str[1:] == 入學年度)
cond = ((df_ucan100To112_IndividualDepartmentCollegeSchool[特定共通職能]<df_ucan100To112_IndividualDepartmentCollegeSchool['D_'+特定共通職能]) & \
          (df_ucan100To112_IndividualDepartmentCollegeSchool[特定共通職能]<df_ucan100To112_IndividualDepartmentCollegeSchool['C_'+特定共通職能]) & \
          (df_ucan100To112_IndividualDepartmentCollegeSchool[特定共通職能]<df_ucan100To112_IndividualDepartmentCollegeSchool['S_'+特定共通職能]))          

selected_低共通職能 = df_ucan100To112_IndividualDepartmentCollegeSchool[cond_00 & cond_01 & cond].reset_index(drop=True)

st.write(selected_低共通職能)



###### (3) 挑選特定個人的 UCAN 資料並繪圖 

##### 輸入個人識別資料
st.subheader("挑選特定個人的 UCAN 資料並比較系院校平均值")
個人資料類型選擇 = st.text_input('以姓名查詢請輸入 0, 以學號查詢請輸入 1 (姓名會重複, 以學號查詢較佳): ')
某個人資料 = pd.DataFrame()
某個人資料_共通職能部分_個人= pd.DataFrame()
某個人資料_共通職能部分_系所= pd.DataFrame()
某個人資料_共通職能部分_學院= pd.DataFrame()
某個人資料_共通職能部分_學校= pd.DataFrame()
melted_某個人資料_共通職能部分_個人= pd.DataFrame()
melted_某個人資料_共通職能部分_系所= pd.DataFrame()
melted_某個人資料_共通職能部分_學院= pd.DataFrame()
melted_某個人資料_共通職能部分_學校= pd.DataFrame()
x = pd.Series()
y1 = pd.Series()
y2 = pd.Series()
y3 = pd.Series()
y4 = pd.Series()


if 個人資料類型選擇 == '0':
    name = st.text_input('請輸入姓名: ')
    if name:
        name_r = name.replace(name[1], '○')
        某個人資料 = df_ucan100To112_IndividualDepartmentCollegeSchool[df_ucan100To112_IndividualDepartmentCollegeSchool['姓名']==name_r]  
if 個人資料類型選擇 == '1':
    ID = st.text_input('請輸入學號(例子: 410635487, 499240243): ')
    if ID:
        某個人資料 = df_ucan100To112_IndividualDepartmentCollegeSchool[df_ucan100To112_IndividualDepartmentCollegeSchool['學號']==ID]  

##### 只取 '共通職能' 部分
if not 某個人資料.empty:
    某個人資料_共通職能部分_個人 = 某個人資料[['溝通表達第1次','持續學習第1次','人際互動第1次','團隊合作第1次','問題解決第1次','創新第1次','工作責任及紀律第1次','資訊科技應用第1次']]
    某個人資料_共通職能部分_系所 = 某個人資料[['D_溝通表達第1次','D_持續學習第1次','D_人際互動第1次','D_團隊合作第1次','D_問題解決第1次','D_創新第1次','D_工作責任及紀律第1次','D_資訊科技應用第1次']]
    某個人資料_共通職能部分_學院 = 某個人資料[['C_溝通表達第1次','C_持續學習第1次','C_人際互動第1次','C_團隊合作第1次','C_問題解決第1次','C_創新第1次','C_工作責任及紀律第1次','C_資訊科技應用第1次']]
    某個人資料_共通職能部分_學校 = 某個人資料[['S_溝通表達第1次','S_持續學習第1次','S_人際互動第1次','S_團隊合作第1次','S_問題解決第1次','S_創新第1次','S_工作責任及紀律第1次','S_資訊科技應用第1次']]


##### 重塑 DataFrame 以便繪圖
if not (某個人資料_共通職能部分_個人.empty or 某個人資料_共通職能部分_系所.empty or 某個人資料_共通職能部分_學院.empty or 某個人資料_共通職能部分_學校.empty):
    melted_某個人資料_共通職能部分_個人 = 某個人資料_共通職能部分_個人.melt(var_name='共通職能項目', value_name='原始分數')
    melted_某個人資料_共通職能部分_系所 = 某個人資料_共通職能部分_系所.melt(var_name='共通職能項目', value_name='原始分數')
    melted_某個人資料_共通職能部分_學院 = 某個人資料_共通職能部分_學院.melt(var_name='共通職能項目', value_name='原始分數')
    melted_某個人資料_共通職能部分_學校 = 某個人資料_共通職能部分_學校.melt(var_name='共通職能項目', value_name='原始分數')
    #type(melted_某個人的資料_共通職能部分_個人)  ## pandas.core.frame.DataFrame
    #melted_某個人的資料_共通職能部分_個人.columns  ##  Index(['共通職能項目', '原始分數'], dtype='object')
    #melted_某個人的資料_共通職能部分_個人.index  ## RangeIndex(start=0, stop=8, step=1)


##### 準備畫圖數據
if not (melted_某個人資料_共通職能部分_個人.empty or melted_某個人資料_共通職能部分_系所.empty or melted_某個人資料_共通職能部分_學院.empty or melted_某個人資料_共通職能部分_學校.empty):
    x = melted_某個人資料_共通職能部分_個人['共通職能項目']
    y1 = melted_某個人資料_共通職能部分_個人['原始分數']
    y2 = melted_某個人資料_共通職能部分_系所['原始分數']
    y3 = melted_某個人資料_共通職能部分_學院['原始分數']
    y4 = melted_某個人資料_共通職能部分_學校['原始分數']

##### 畫圖
import matplotlib.pyplot as plt
import matplotlib

##### 設置 matplotlib 支持中文的字體: 這裡使用的是 'SimHei' 字體，您也可以替換為任何支持中文的字體
matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
##### 畫圖
# with st.expander("UCAN 分數比較: 個人、系所、學院、學校"):
#     plt.figure(figsize=(10, 6))
#     plt.plot(x, y1, '-b', label='個人', marker='o')  
#     plt.plot(x, y2, '-r', label='系所', marker='s')
#     plt.plot(x, y3, '-g', label='學院',marker='*')
#     plt.plot(x, y4, color='pink', label='學校', marker='x')
#     plt.xlabel('共通職能項目')
#     plt.ylabel('UCAN 原始分數')
#     if 個人資料類型選擇 == '0':
#         plt.title(f'姓名_{name} UCAN 分數比較: 個人、系所、學院、學校')
#     else:
#         plt.title(f'學號_{ID} UCAN 分數比較: 個人、系所、學院、學校')
#     plt.legend()
#     plt.xticks(rotation=45)
#     plt.show()


##### 畫圖 #####
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
#from plotly.offline import plot
#import plotly.offline as pyoff
#st.subheader("UCAN 資料繪圖")

if not (x.empty or y1.empty or y2.empty or y3.empty or y4.empty):
    with st.expander("UCAN 分數比較: 個人、系所、學院、學校"):
        fig1 = make_subplots(specs=[[{"secondary_y": False}]])
           
        ##include a go.Bar trace for volumes
        #fig1.add_trace(go.Bar(x=KBar_df['Time'], y=KBar_df['Volume'], name='成交量', marker=dict(color='black')),secondary_y=False)  ## secondary_y=False 表示此圖形的y軸scale是在左邊而不是在右邊
        fig1.add_trace(go.Scatter(x=x, y=y1, mode='lines+markers',line=dict(color='red', width=2), name='個人'), secondary_y=False)
        fig1.add_trace(go.Scatter(x=x, y=y2, mode='lines+markers',line=dict(color='green', width=2), name='系所'), secondary_y=False)
        fig1.add_trace(go.Scatter(x=x, y=y3, mode='lines+markers',line=dict(color='blue', width=2), name='學院'), secondary_y=False)
        fig1.add_trace(go.Scatter(x=x, y=y4, mode='lines+markers',line=dict(color='orange', width=2), name='學校'), secondary_y=False)
        
        #fig1.layout.yaxis2.showgrid=True
        
        ## 設定圖表標題
        if 個人資料類型選擇 == '0':
            fig1.update_layout(title = f'姓名_{name} UCAN 分數比較: 個人、系所、學院、學校', xaxis_title='共通職能項目', yaxis_title='UCAN 原始分數')
        else:
            fig1.update_layout(title = f'學號_{ID} UCAN 分數比較: 個人、系所、學院、學校', xaxis_title='共通職能項目', yaxis_title='UCAN 原始分數')
            
    
    
    
        #fig.show()
        #pyoff.plot(fig)
        
        #fig2 = make_subplots(specs=[[{"secondary_y": True}]])
        #fig2.add_trace(go.Scatter(x=KBar_df['Time'][last_nan_index_RSI+1:], y=KBar_df['RSI_long'][last_nan_index_RSI+1:], mode='lines',line=dict(color='orange', width=2), name=f'{LongRSIPeriod}-根 K棒 移動 RSI'), 
                      #secondary_y=False)
        #fig2.add_trace(go.Scatter(x=KBar_df['Time'][last_nan_index_RSI+1:], y=KBar_df['RSI_short'][last_nan_index_RSI+1:], mode='lines',line=dict(color='orange', width=2), name=f'{ShortRSIPeriod}-根 K棒 移動 RSI'), 
                      #secondary_y=False)
        
        
        ## streamlit plot
        st.plotly_chart(fig1, use_container_width=True)
        #st.plotly_chart(fig2, use_container_width=True)






























# #### 讀取各入學年度 UCAN檔案並合併
# ### 105入學
# df_ucan105 = pd.read_excel(r'C:\Users\user\Dropbox\系務\校務研究IR\資料\UCan\整理後資料 (Lo)\UCAN_105-112入學\105_ucan.xls')
# df_ucan105.shape  ## (2235, 53)
# df_ucan105.columns
# df_ucan105 = df_ucan105.iloc[:,0:18]
# df_ucan105.shape  ## (2235, 18)
# #df_ucan105.isna().sum(axis=1)
# df_ucan105.isna().sum(axis=0)
# df_ucan105_NoNA = df_ucan105.dropna(subset=['學號'])
# df_ucan105_NoNA.shape  ## (2234, 18)　　##去掉一筆學號有ＮＡ值的資料
# df_ucan105_NoNA.isna().sum(axis=0)
# filtered_df = df_ucan105_NoNA[~df_ucan105_NoNA['學號'].str.startswith('4')]
# filtered_df.to_excel(r'C:\Users\user\Dropbox\系務\校務研究IR\資料\UCan\整理後資料 (Lo)\UCAN_105-112入學\105入學學號不是以4開頭.xlsx', index=False)

# ### 106入學
# df_ucan106 = pd.read_excel(r'C:\Users\user\Dropbox\系務\校務研究IR\資料\UCan\整理後資料 (Lo)\UCAN_105-112入學\106_ucan.xls')
# df_ucan106.shape  ## (2186, 53)
# df_ucan106 = df_ucan106.iloc[:,0:18]
# df_ucan106.shape  ## (2186, 18)
# #df_ucan106.isna().sum(axis=1)
# df_ucan106.isna().sum(axis=0)  ## 沒有 NA值
# df_ucan106_NoNA = df_ucan106.dropna(subset=['學號'])
# df_ucan106_NoNA.shape  ## (2186, 18)
# df_ucan106_NoNA.isna().sum(axis=0)
# filtered_df = df_ucan106_NoNA[~df_ucan106_NoNA['學號'].str.startswith('4')]
# filtered_df.to_excel(r'C:\Users\user\Dropbox\系務\校務研究IR\資料\UCan\整理後資料 (Lo)\UCAN_105-112入學\106入學學號不是以4開頭.xlsx', index=False)

# ### 107入學
# df_ucan107 = pd.read_excel(r'C:\Users\user\Dropbox\系務\校務研究IR\資料\UCan\整理後資料 (Lo)\UCAN_105-112入學\107_ucan.xls')
# df_ucan107.shape  ## (2427, 53)
# df_ucan107 = df_ucan107.iloc[:,0:18]
# df_ucan107.shape  ## (2427, 18)
# #df_ucan107.isna().sum(axis=1)
# df_ucan107.isna().sum(axis=0)  ## 
# df_ucan107_NoNA = df_ucan107.dropna(subset=['學號'])
# df_ucan107_NoNA.shape  ## (2426, 18)  ##去掉一筆學號有ＮＡ值的資料
# df_ucan107_NoNA.isna().sum(axis=0)
# filtered_df = df_ucan107_NoNA[~df_ucan107_NoNA['學號'].str.startswith('4')]
# filtered_df.to_excel(r'C:\Users\user\Dropbox\系務\校務研究IR\資料\UCan\整理後資料 (Lo)\UCAN_105-112入學\107入學學號不是以4開頭.xlsx', index=False)

# ### 108入學
# df_ucan108 = pd.read_excel(r'C:\Users\user\Dropbox\系務\校務研究IR\資料\UCan\整理後資料 (Lo)\UCAN_105-112入學\108_ucan.xls')
# df_ucan108.shape  ## (2203, 53)
# df_ucan108 = df_ucan108.iloc[:,0:18]
# df_ucan108.shape  ## (2203, 18)
# #df_ucan108.isna().sum(axis=1)
# df_ucan108.isna().sum(axis=0)  ## 沒有 NA值
# df_ucan108_NoNA = df_ucan108.dropna(subset=['學號'])
# df_ucan108_NoNA.shape  ## (2203, 18)  ##
# df_ucan108_NoNA.isna().sum(axis=0)
# filtered_df = df_ucan108_NoNA[~df_ucan108_NoNA['學號'].str.startswith('4')]
# filtered_df.to_excel(r'C:\Users\user\Dropbox\系務\校務研究IR\資料\UCan\整理後資料 (Lo)\UCAN_105-112入學\108入學學號不是以4開頭.xlsx', index=False)


# ### 109入學
# df_ucan109 = pd.read_excel(r'C:\Users\user\Dropbox\系務\校務研究IR\資料\UCan\整理後資料 (Lo)\UCAN_105-112入學\109_ucan.xls')
# df_ucan109.shape  ## (2895, 53)
# df_ucan109 = df_ucan109.iloc[:,0:18]
# df_ucan109.shape  ## (2895, 18)
# #df_ucan109.isna().sum(axis=1)
# df_ucan109.isna().sum(axis=0)  ## 沒有 NA值
# df_ucan109_NoNA = df_ucan109.dropna(subset=['學號'])
# df_ucan109_NoNA.shape  ## (2895, 18)  ##
# df_ucan109_NoNA.isna().sum(axis=0)
# filtered_df = df_ucan109_NoNA[~df_ucan109_NoNA['學號'].str.startswith('4')]
# filtered_df.to_excel(r'C:\Users\user\Dropbox\系務\校務研究IR\資料\UCan\整理後資料 (Lo)\UCAN_105-112入學\109入學學號不是以4開頭.xlsx', index=False)

# ### 110入學
# df_ucan110 = pd.read_excel(r'C:\Users\user\Dropbox\系務\校務研究IR\資料\UCan\整理後資料 (Lo)\UCAN_105-112入學\110_ucan.xls')
# df_ucan110.shape  ## (2202, 53)
# df_ucan110 = df_ucan110.iloc[:,0:18]
# df_ucan110.shape  ## (2202, 18)
# #df_ucan110.isna().sum(axis=1)
# df_ucan110.isna().sum(axis=0)  ## 沒有 NA值
# df_ucan110_NoNA = df_ucan110.dropna(subset=['學號'])
# df_ucan110_NoNA.shape  ## (2202, 18)  ##
# df_ucan110_NoNA.isna().sum(axis=0)
# filtered_df = df_ucan110_NoNA[~df_ucan110_NoNA['學號'].str.startswith('4')]
# filtered_df.to_excel(r'C:\Users\user\Dropbox\系務\校務研究IR\資料\UCan\整理後資料 (Lo)\UCAN_105-112入學\110入學學號不是以4開頭.xlsx', index=False)

# ### 112入學
# df_ucan112 = pd.read_excel(r'C:\Users\user\Dropbox\系務\校務研究IR\資料\UCan\整理後資料 (Lo)\UCAN_105-112入學\112_ucan.xls')
# df_ucan112.shape  ## (1852, 53)
# df_ucan112 = df_ucan112.iloc[:,0:18]
# df_ucan112.shape  ## (1852, 18)
# #df_ucan112.isna().sum(axis=1)
# df_ucan112.isna().sum(axis=0)  ## 沒有 NA值
# df_ucan112_NoNA = df_ucan112.dropna(subset=['學號'])
# df_ucan112_NoNA.shape  ## (1852, 18)  ##
# df_ucan112_NoNA.isna().sum(axis=0)
# filtered_df = df_ucan112_NoNA[~df_ucan112_NoNA['學號'].str.startswith('4')]
# filtered_df.to_excel(r'C:\Users\user\Dropbox\系務\校務研究IR\資料\UCan\整理後資料 (Lo)\UCAN_105-112入學\112入學學號不是以4開頭.xlsx', index=False)

# ### UCAN 合併資料 (for 105,106,107,108,109,110,112)
# df_ucan105To112 = pd.concat([df_ucan105_NoNA,df_ucan106_NoNA,df_ucan107_NoNA,df_ucan108_NoNA,df_ucan109_NoNA,df_ucan110_NoNA,df_ucan112_NoNA])
# df_ucan105To112.reset_index(drop=True, inplace=True)
# df_ucan105To112.index  ## RangeIndex(start=0, stop=15998, step=1)
# df_ucan105To112.shape  ## (15998, 18)
# #df_ucan105To112 = df_ucan105To112.iloc[:,0:18]
# #df_ucan105To112.shape  ##  (16000, 18)
# df_ucan105To112.columns
# df_ucan105To112.head()
# df_ucan105To112['學號']
# type(df_ucan105To112['學號'][0])  ## str
# df_ucan105To112[df_ucan105To112['學號']=='410635487'] ##  獲取學號為 '410635487' 的資料.

# ### 獲得UCAN資料中 (for 105,106,107,108,109,110,112), 不同入學年度的樣本數分佈(藉由學號前四碼)
# df_ucan105To112['學號_first4'] = df_ucan105To112['學號'].str[:4]
# df_ucan105To112.columns
# value_counts_UCAN_105To112 = df_ucan105To112['學號_first4'].value_counts()
# type(value_counts_UCAN_105To112)  ## pandas.core.series.Series
# #value_counts_UCAN_105To112.index   
# value_counts_UCAN_105To112[:20]  ## 學號4105開頭有2080筆, 學號4106開頭有2265筆

# ### 100-108入學
# df_ucan100To108 = pd.read_excel(r'C:\Users\user\Dropbox\系務\校務研究IR\資料\UCan\整理後資料 (Lo)\UCAN_100-108入學\100-108個人分數_Lo.xls')
# df_ucan100To108.shape  ##  (24284, 53)
# df_ucan100To108 = df_ucan100To108.iloc[:,0:18]
# df_ucan100To108.shape  ## (24284, 18)
# #df_ucan100To108.isna().sum(axis=1)
# df_ucan100To108.isna().sum(axis=0)  ## 學號欄位有 11個NA值
# df_ucan100To108_NoNA = df_ucan100To108.dropna(subset=['學號'])
# df_ucan100To108_NoNA.shape  ## (24273, 18), 24273=24284-11
# df_ucan100To108_NoNA.isna().sum(axis=0)  ## 沒有 NA 值了
# #type(df_ucan100To108_NoNA['學號'][0])  ## str
# filtered_df = df_ucan100To108_NoNA[~df_ucan100To108_NoNA['學號'].str.startswith('4')]
# filtered_df.to_excel(r'C:\Users\user\Dropbox\系務\校務研究IR\資料\UCan\整理後資料 (Lo)\UCAN_100-108入學\100To108入學學號不是以4開頭.xlsx', index=False)

# ### 獲得100-108入學UCAN資料中, 不同入學年度的樣本數分佈(藉由學號前四碼)
# df_ucan100To108_NoNA['學號_first4'] = df_ucan100To108_NoNA['學號'].str[:4]
# #df_ucan100To108_NoNA.loc[:,'學號_first4'] = df_ucan100To108_NoNA['學號'].str[:4]
# df_ucan100To108_NoNA.columns
# value_counts_UCAN_100To108_NoNA = df_ucan100To108_NoNA['學號_first4'].value_counts()
# #type(value_counts_UCAN_100To108_NoNA)  ## pandas.core.series.Series
# #value_counts_UCAN_100To108_NoNA.index   
# value_counts_UCAN_100To108_NoNA[:20]  ## 學號4105開頭有2201筆, 學號4106開頭有2267筆


# ### UCAN 合併資料 (for 100, 101,102,103,104,105,106,107,108,109,110,112)
# df_ucan100To112 = pd.concat([df_ucan105To112, df_ucan100To108_NoNA])   ## [40271 rows x 19 columns]
# df_ucan100To112 = df_ucan100To112.drop_duplicates(subset=['學號'])     ## [28755 rows x 19 columns]
# df_ucan100To112.reset_index(drop=True, inplace=True)
# df_ucan100To112.index  ## RangeIndex(start=0, stop=28755, step=1)
# df_ucan100To112.shape  ## (28755, 19)
# df_ucan100To112.columns
# df_ucan100To112.head()
# df_ucan100To112['學號']
# type(df_ucan100To112['學號'][0])  ## str
# df_ucan100To112[df_ucan100To112['學號']=='410635487'] ##  獲取學號為 '410635487' 的資料.

# ### 獲得100-112入學UCAN資料中, 不同入學年度的樣本數分佈(藉由學號前四碼)
# df_ucan100To112['學號_first4'] = df_ucan100To112['學號'].str[:4]
# #df_ucan100To112.loc[:,'學號_first4'] = df_ucan100To112['學號'].str[:4]
# df_ucan100To112.columns
# value_counts_UCAN_100To112 = df_ucan100To112['學號_first4'].value_counts()
# #type(value_counts_UCAN_100To112)  ## pandas.core.series.Series
# #value_counts_UCAN_100To112.index   
# value_counts_UCAN_100To112[:20]  ## 學號4105開頭有2057筆, 學號4106開頭有2067筆

# ### 檢查學號欄位是否有重複的
# df_ucan100To112['學號'].value_counts(ascending=False)

# ### 找出系名
# unique_values_department = df_ucan100To112['系所'].unique()  ## 是同一系: '資訊科學暨大數據分析與應用學系' 與 '資料科學暨大數據分析與應用學系'
# df_ucan100To112['系所'].replace('資訊科學暨大數據分析與應用學系', '資料科學暨大數據分析與應用學系', inplace=True)
# df_ucan100To112['系所'].replace('社會工作與兒童(少年)福利學系', '社會工作與兒童少年福利學系', inplace=True)
# unique_values_department = df_ucan100To112['系所'].unique()

# ### UCAN原始資料df_ucan100To112增加學院別的column 
# ## 定義系名到學院的映射
# #['Science', 'Management', 'Social','Information','Internation','Language']
# college_map =\
# {'台灣文學系':'Social', 
#  '中國文學系':'Social', 
#  '英國語文學系':'Language', 
#  '西班牙語文學系':'Language', 
#  '日本語文學系':'Language', 
#  '寰宇外語教育':'Internation',
#  '大眾傳播學系':'Social', 
#  '資訊傳播工程學系':'Information', 
#  '寰宇管理學程':'Internation', 
#  '會計學系':'Management', 
#  '企業管理學系':'Management', 
#  '國際企業學系':'Management',
#  '財務金融學系':'Management', 
#  '法律學系':'Social', 
#  '生態學系':'Social', 
#  '應用化學系':'Science', 
#  '資料科學暨大數據分析與應用學系':'Science', 
#  '財務工程學系':'Science',
#  '資訊管理學系':'Information', 
#  '資訊工程學系':'Information', 
#  '食品營養學系':'Science', 
#  '觀光事業學系':'Management',
#  '化粧品科學系':'Science', 
#  '創新與創業管理碩士學位學程':'Management', 
#  '西班牙語文學系碩士班':'Language', 
#  '法律學士學位學程原住民專班':'Social',
#  '健康照顧社會工作學士學位學程原住民專班':'Social', 
#  '寰宇外語教育學士學位學程':'Internation', 
#  '寰宇管理學士學位學程':'Internation', 
#  '生態人文學系':'Social',
#  '社會工作與兒童少年福利學系':'Social', 
#  '國際生大一博雅教育學士學位學程':'Internation', 
#  '經營管理學士班':'Management', 
#  '應用數學系':'Science', 
#  '不分系':'No_College'
# }

# ## 使用映射來創建新的 '學院別' 欄位
# df_ucan100To112.columns
# df_ucan100To112['學院別'] = df_ucan100To112['系所'].map(college_map)
# df_ucan100To112.head(700)
# df_ucan100To112.tail(20)
 

# ### 以"系" 統整資料
# df_ucan100To112_departments = df_ucan100To112.groupby('系所')[['溝通表達第1次','持續學習第1次', '人際互動第1次', '團隊合作第1次', '問題解決第1次', '創新第1次', '工作責任及紀律第1次','資訊科技應用第1次']].mean()
# type(df_ucan100To112_departments)
# df_ucan100To112_departments.head()
# df_ucan100To112_departments.iloc[2,:]
# df_ucan100To112_departments.columns
# '''
# Index(['溝通表達第1次', '持續學習第1次', '人際互動第1次', '團隊合作第1次', '問題解決第1次', '創新第1次','工作責任及紀律第1次', '資訊科技應用第1次'],dtype='object')
# '''
# df_ucan100To112_departments.index
# ## 將index 轉換成一個新的column(column name 是 'index'), 並為這個新的 column 命名:
# df_ucan100To112_departments_reset = df_ucan100To112_departments.reset_index().rename(columns={'系所': '系所'})
# df_ucan100To112_departments_reset.columns
# ## 從第二個 column 到最後一個 column 的 column name 前面增加字串 'D_'
# df_ucan100To112_departments_reset.columns = [df_ucan100To112_departments_reset.columns[0]] + ['D_' + col for col in df_ucan100To112_departments_reset.columns[1:]]


# ### 以 "院" 統整資料:
# ## 选择理學院各系，並計算各columns 平均值
# df_ucan100To112_Science = df_ucan100To112_departments.loc[['應用化學系', '資料科學暨大數據分析與應用學系', '食品營養學系', '財務工程學系', '化粧品科學系','應用數學系'],:].mean()
# #type(df_ucan100To112_Science)  ## pandas.core.series.Series
# df_ucan100To112_Science.head(8)
# df_ucan100To112_Science.index
# #df_ucan100To112_Science.columns

# ## 选择管理學院各系，並計算各columns 平均值
# df_ucan100To112_Manage = df_ucan100To112_departments.loc[['會計學系', '企業管理學系', '國際企業學系', '財務金融學系', '觀光事業學系','創新與創業管理碩士學位學程','經營管理學士班'],:].mean()
# df_ucan100To112_Manage.head(8)
# df_ucan100To112_Manage.index

# ## 选择人文社會學院各系，並計算各columns 平均值
# df_ucan100To112_Social = df_ucan100To112_departments.loc[['台灣文學系', '中國文學系', '大眾傳播學系', '法律學系', '生態學系','法律學士學位學程原住民專班','健康照顧社會工作學士學位學程原住民專班','生態人文學系','社會工作與兒童少年福利學系'],:].mean()
# df_ucan100To112_Social.head(8)
# df_ucan100To112_Social.index

# ## 选择資訊學院各系，並計算各columns 平均值
# df_ucan100To112_Information = df_ucan100To112_departments.loc[['資訊傳播工程學系', '資訊管理學系', '資訊工程學系'],:].mean()
# df_ucan100To112_Information.head(8)
# df_ucan100To112_Information.index

# ## 选择國際學院各系，並計算各columns 平均值
# df_ucan100To112_Internation = df_ucan100To112_departments.loc[['寰宇管理學程', '寰宇外語教育','寰宇外語教育學士學位學程', '寰宇管理學士學位學程','國際生大一博雅教育學士學位學程'],:].mean()
# df_ucan100To112_Internation.head(8)
# df_ucan100To112_Internation.index

# ## 选择外語學院各系，並計算各columns 平均值
# df_ucan100To112_Language = df_ucan100To112_departments.loc[['英國語文學系', '西班牙語文學系','日本語文學系', '西班牙語文學系碩士班'],:].mean()
# df_ucan100To112_Language.head(8)
# df_ucan100To112_Language.index


# ## 綜合各院資料:
# df_ucan100To112_Colleges = pd.concat([df_ucan100To112_Science, df_ucan100To112_Manage, df_ucan100To112_Social,df_ucan100To112_Information,df_ucan100To112_Internation,df_ucan100To112_Language], axis=1).transpose()
# #type(df_ucan100To112_Colleges)  ## pandas.core.frame.DataFrame
# df_ucan100To112_Colleges.index
# df_ucan100To112_Colleges.columns
# df_ucan100To112_Colleges.index = ['Science', 'Management', 'Social','Information','Internation','Language']
# df_ucan100To112_Colleges.head(6)

# ## 將index 轉換成一個新的column(column name 是 'index'), 並為這個新的 column 命名:
# df_ucan100To112_Colleges_reset = df_ucan100To112_Colleges.reset_index().rename(columns={'index': '學院別'})
# df_ucan100To112_Colleges_reset.columns
# ## 從第二個 column 到最後一個 column 的 column name 前面增加字串 'C_'
# df_ucan100To112_Colleges_reset.columns = [df_ucan100To112_Colleges_reset.columns[0]] + ['C_' + col for col in df_ucan100To112_Colleges_reset.columns[1:]]


# ###  統整: 個人,系所,學院,學校 資料: df_ucan100To112, df_ucan100To112_departments_reset, df_ucan100To112_Colleges_reset
# ## 合併 個人, 系所:
# df_ucan100To112_IndividualDepartment = pd.merge(df_ucan100To112, df_ucan100To112_departments_reset, how="inner", on='系所')  ## [28755 rows x 28 columns]
# df_ucan100To112_IndividualDepartment.columns
# '''
# Index(['學校', '學制', '系所', '年級', '班級', '學號', '姓名', '性別', '診斷次數', '溝通表達第1次',
#        '持續學習第1次', '人際互動第1次', '團隊合作第1次', '問題解決第1次', '創新第1次', '工作責任及紀律第1次',
#        '資訊科技應用第1次', '第1次診斷完成時間', '學號_first4', '學院別', 'D_溝通表達第1次', 'D_持續學習第1次',
#        'D_人際互動第1次', 'D_團隊合作第1次', 'D_問題解決第1次', 'D_創新第1次', 'D_工作責任及紀律第1次',
#        'D_資訊科技應用第1次'],
#       dtype='object')
# '''
# df_ucan100To112_IndividualDepartment.head(2000)

# ## 合併 個人, 系所, 學院:
# df_ucan100To112_IndividualDepartmentCollege = pd.merge(df_ucan100To112_IndividualDepartment, df_ucan100To112_Colleges_reset, how="inner", on='學院別')  ## [28755 rows x 28 columns]
# df_ucan100To112_IndividualDepartmentCollege.columns  
# '''
# Index(['學校', '學制', '系所', '年級', '班級', '學號', '姓名', '性別', '診斷次數', '溝通表達第1次',
#        '持續學習第1次', '人際互動第1次', '團隊合作第1次', '問題解決第1次', '創新第1次', '工作責任及紀律第1次',
#        '資訊科技應用第1次', '第1次診斷完成時間', '學號_first4', '學院別', 'D_溝通表達第1次', 'D_持續學習第1次',
#        'D_人際互動第1次', 'D_團隊合作第1次', 'D_問題解決第1次', 'D_創新第1次', 'D_工作責任及紀律第1次',
#        'D_資訊科技應用第1次', 'C_溝通表達第1次', 'C_持續學習第1次', 'C_人際互動第1次', 'C_團隊合作第1次',
#        'C_問題解決第1次', 'C_創新第1次', 'C_工作責任及紀律第1次', 'C_資訊科技應用第1次'],
#       dtype='object')
# ''' 
# df_ucan100To112_IndividualDepartmentCollege.index 
# df_ucan100To112_IndividualDepartmentCollege.head(5000)
# df_ucan100To112_IndividualDepartmentCollege.tail(5000)


# ## 合併 個人,系所,學院,學校: 增加8項學校整體平均共通職能分數
# means = df_ucan100To112[['溝通表達第1次','持續學習第1次', '人際互動第1次', '團隊合作第1次', '問題解決第1次', '創新第1次', '工作責任及紀律第1次','資訊科技應用第1次']].mean()
# df_ucan100To112_IndividualDepartmentCollegeSchool = df_ucan100To112_IndividualDepartmentCollege
# df_ucan100To112_IndividualDepartmentCollegeSchool['S_溝通表達第1次'] = means[0]
# df_ucan100To112_IndividualDepartmentCollegeSchool['S_持續學習第1次'] = means[1]
# df_ucan100To112_IndividualDepartmentCollegeSchool['S_人際互動第1次'] = means[2]
# df_ucan100To112_IndividualDepartmentCollegeSchool['S_團隊合作第1次'] = means[3]
# df_ucan100To112_IndividualDepartmentCollegeSchool['S_問題解決第1次'] = means[4]
# df_ucan100To112_IndividualDepartmentCollegeSchool['S_創新第1次'] = means[5]
# df_ucan100To112_IndividualDepartmentCollegeSchool['S_工作責任及紀律第1次'] = means[6]
# df_ucan100To112_IndividualDepartmentCollegeSchool['S_資訊科技應用第1次'] = means[7]
# df_ucan100To112_IndividualDepartmentCollegeSchool.shape  ## (28741, 44)
# df_ucan100To112_IndividualDepartmentCollegeSchool.columns
# '''
# Index(['學校', '學制', '系所', '年級', '班級', '學號', '姓名', '性別', '診斷次數', '溝通表達第1次',
#        '持續學習第1次', '人際互動第1次', '團隊合作第1次', '問題解決第1次', '創新第1次', '工作責任及紀律第1次',
#        '資訊科技應用第1次', '第1次診斷完成時間', '學號_first4', '學院別', 'D_溝通表達第1次', 'D_持續學習第1次',
#        'D_人際互動第1次', 'D_團隊合作第1次', 'D_問題解決第1次', 'D_創新第1次', 'D_工作責任及紀律第1次',
#        'D_資訊科技應用第1次', 'C_溝通表達第1次', 'C_持續學習第1次', 'C_人際互動第1次', 'C_團隊合作第1次',
#        'C_問題解決第1次', 'C_創新第1次', 'C_工作責任及紀律第1次', 'C_資訊科技應用第1次', 'S_溝通表達第1次',
#        'S_持續學習第1次', 'S_人際互動第1次', 'S_團隊合作第1次', 'S_問題解決第1次', 'S_創新第1次',
#        'S_工作責任及紀律第1次', 'S_資訊科技應用第1次'],
#       dtype='object')
# '''
# df_ucan100To112_IndividualDepartmentCollegeSchool.index
# df_ucan100To112_IndividualDepartmentCollegeSchool.head()
# df_ucan100To112_IndividualDepartmentCollegeSchool['學號']  ## 410635487, 499240243...

# ## 存成外部 excel 檔:
# df_ucan100To112_IndividualDepartmentCollegeSchool.to_excel(r'df_ucan100To112_IndividualDepartmentCollegeSchool.xlsx', index=False)
# ## 存成外部 pickle 檔:
# df_ucan100To112_IndividualDepartmentCollegeSchool.to_pickle(r'df_ucan100To112_IndividualDepartmentCollegeSchool.pkl')
# # ## 讀取pkl檔案: df_ucan100To112_IndividualDepartmentCollegeSchool.pkl 
# # df_ucan100To112_IndividualDepartmentCollegeSchool = pd.read_pickle('df_ucan100To112_IndividualDepartmentCollegeSchool.pkl')  ## [28741 rows x 44 columns]

# ### 畫圖 
# ## 輸入學號
# #學號 = input('請輸入想查詢UCAN資料之學號: ')  ## 410635487
# 個人資料類型選擇 = input('以姓名查詢請輸入 0, 以學號查詢請輸入 1 (姓名會重複, 以學號查詢較佳): ')
# if 個人資料類型選擇 == '0':
#     name = input('請輸入姓名(姓名中間以圈圈替代, 例如 陳○涵): ')
#     name_r = name.replace(name[1], '○')
#     某個人資料 = df_ucan100To112_IndividualDepartmentCollegeSchool[df_ucan100To112_IndividualDepartmentCollegeSchool['姓名']==name_r]  
# if 個人資料類型選擇 == '1':
#     ID = input('請輸入學號: ')
#     某個人資料 = df_ucan100To112_IndividualDepartmentCollegeSchool[df_ucan100To112_IndividualDepartmentCollegeSchool['學號']==ID]  


# #個人資料 = '499240243'  ## '410635487'
# ## 只取 '共通職能' 部分
# 某個人資料_共通職能部分_個人 = 某個人資料[['溝通表達第1次','持續學習第1次','人際互動第1次','團隊合作第1次','問題解決第1次','創新第1次','工作責任及紀律第1次','資訊科技應用第1次']]
# 某個人資料_共通職能部分_系所 = 某個人資料[['D_溝通表達第1次','D_持續學習第1次','D_人際互動第1次','D_團隊合作第1次','D_問題解決第1次','D_創新第1次','D_工作責任及紀律第1次','D_資訊科技應用第1次']]
# 某個人資料_共通職能部分_學院 = 某個人資料[['C_溝通表達第1次','C_持續學習第1次','C_人際互動第1次','C_團隊合作第1次','C_問題解決第1次','C_創新第1次','C_工作責任及紀律第1次','C_資訊科技應用第1次']]
# 某個人資料_共通職能部分_學校 = 某個人資料[['S_溝通表達第1次','S_持續學習第1次','S_人際互動第1次','S_團隊合作第1次','S_問題解決第1次','S_創新第1次','S_工作責任及紀律第1次','S_資訊科技應用第1次']]
    
# '''    
#     '溝通表達第1次','持續學習第1次','人際互動第1次',
#     '團隊合作第1次','問題解決第1次','創新第1次',
#     '工作責任及紀律第1次','資訊科技應用第1次',
#     'D_溝通表達第1次','D_持續學習第1次','D_人際互動第1次',
#     'D_團隊合作第1次','D_問題解決第1次','D_創新第1次',
#     'D_工作責任及紀律第1次','D_資訊科技應用第1次',
#     'C_溝通表達第1次','C_持續學習第1次','C_人際互動第1次',
#     'C_團隊合作第1次','C_問題解決第1次','C_創新第1次',
#     'C_工作責任及紀律第1次','C_資訊科技應用第1次',
#     'S_溝通表達第1次','S_持續學習第1次','S_人際互動第1次',
#     'S_團隊合作第1次','S_問題解決第1次','S_創新第1次',
#     'S_工作責任及紀律第1次','S_資訊科技應用第1次'
#     ]]  ## [28741 rows x 32 columns]
# '''
# #df_ucan100To112_IndividualDepartmentCollegeSchool_共通職能部分.columns
# #df_ucan100To112_IndividualDepartmentCollegeSchool_共通職能部分.iloc[0,:]

# ## 重塑 DataFrame 以便繪圖
# melted_某個人資料_共通職能部分_個人 = 某個人資料_共通職能部分_個人.melt(var_name='共通職能項目', value_name='原始分數')
# melted_某個人資料_共通職能部分_系所 = 某個人資料_共通職能部分_系所.melt(var_name='共通職能項目', value_name='原始分數')
# melted_某個人資料_共通職能部分_學院 = 某個人資料_共通職能部分_學院.melt(var_name='共通職能項目', value_name='原始分數')
# melted_某個人資料_共通職能部分_學校 = 某個人資料_共通職能部分_學校.melt(var_name='共通職能項目', value_name='原始分數')
# #type(melted_某學號的資料_共通職能部分_個人)  ## pandas.core.frame.DataFrame
# #melted_某學號的資料_共通職能部分_個人.columns  ##  Index(['共通職能項目', '原始分數'], dtype='object')
# #melted_某學號的資料_共通職能部分_個人.index  ## RangeIndex(start=0, stop=8, step=1)


# ## 準備畫圖數據
# x = melted_某個人資料_共通職能部分_個人['共通職能項目']
# y1 = melted_某個人資料_共通職能部分_個人['原始分數']
# y2 = melted_某個人資料_共通職能部分_系所['原始分數']
# y3 = melted_某個人資料_共通職能部分_學院['原始分數']
# y4 = melted_某個人資料_共通職能部分_學校['原始分數']

# import matplotlib.pyplot as plt
# import matplotlib

# ## 設置 matplotlib 支持中文的字體: 這裡使用的是 'SimHei' 字體，您也可以替換為任何支持中文的字體
# matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
# matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
# matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題

# ## 畫圖
# plt.figure(figsize=(10, 6))
# plt.plot(x, y1, '-b', label='個人', marker='o')  
# plt.plot(x, y2, '-r', label='系所', marker='s')
# plt.plot(x, y3, '-g', label='學院',marker='*')
# plt.plot(x, y4, color='pink', label='學校', marker='x')
# plt.xlabel('共通職能項目')
# plt.ylabel('UCAN 原始分數')
# if 個人資料類型選擇 == '0':
#     plt.title(f'姓名_{name} UCAN 分數比較: 個人、系所、學院、學校')
# else:
#     plt.title(f'學號_{ID} UCAN 分數比較: 個人、系所、學院、學校')
# plt.legend()
# plt.xticks(rotation=45)
# plt.show()




# #### 畢業生流向整合資料
# df_graduation_total = pd.read_excel(r'C:\Users\user\Dropbox\系務\校務研究IR\資料\UCan\整理後資料 (Lo)\畢業生流向資料\A10_Lo2.xlsx')
# df_graduation_total.head()
# df_graduation_total.shape  ## (24799, 11)
# #df_graduation_total.index  ## RangeIndex(start=0, stop=24799, step=1)
# df_graduation_total.columns  ## Index(['A', 'B', 'C', '學號', 'job', 'F', 'G', 'H', 'I', 'J', 'K'], dtype='object')
# df_graduation_total.isna().sum(axis=0)  ##
# df_graduation_total_NoNA = df_graduation_total.dropna(subset=['學號','job'])
# #df_graduation_total_NoNA = df_graduation_total.dropna(subset=['job'])
# #df_graduation_total_NoNA = df_ucan110.dropna(subset=['job'])
# df_graduation_total_NoNA.shape  ## (23971, 11)
# df_graduation_total_NoNA.isna().sum(axis=0)  ## "學號" 與 "job" 欄位沒有NA值了
# #type(df_graduation_total_NoNA['學號'][0])  ## int
# df_graduation_total_NoNA['學號'] = df_graduation_total_NoNA['學號'].astype(str) ## 資料型態從 int 變成 str
# #type(df_graduation_total_NoNA['學號'][0])  ## str
# df_graduation_total_NoNA['學號_first4'] = df_graduation_total_NoNA['學號'].str[:4]
# df_graduation_total_NoNA.columns
# #df_graduation_total_NoNA[df_graduation_total_NoNA['學號']=='410635487']

# ### 畢業生流向學號資料不是以4開頭
# filtered_df = df_graduation_total_NoNA[~df_graduation_total_NoNA['學號'].str.startswith('4')]
# filtered_df.to_excel(r'C:\Users\user\Dropbox\系務\校務研究IR\資料\UCan\整理後資料 (Lo)\畢業生流向資料\畢業生流向學號資料不是以4開頭\畢業生流向學號資料不是以4開頭.xlsx', index=False)

# ### 獲得畢業生流向資料中, 不同入學年度的樣本數分佈(藉由學號前四碼)
# value_counts_graduation = df_graduation_total_NoNA['學號_first4'].value_counts()
# #type(value_counts_graduation)  ## pandas.core.series.Series
# #value_counts.index   
# value_counts_graduation[:20]  ## 學號4105開頭有1968筆, 學號4106開頭有1593筆
# ''' 
# Index(['4103', '4104', '4102', '4101', '4105', '4100', '4106', '4993', '6105',
#        '6104', '6103', '6102', '4995', '6106', '4992', '4994', '6101', '4997',
#        '6107', '6100', '6108', '4983', '4984', '4987', '4982', '6109', '4985',
#        '6995', 'D101', '4977', '4973', '6993', '6994', '4975', '6992', '6985',
#        '4972', 'D100', '4974', '6997', '6975', '6987', '6942', '4967', '6982',
#        '6983', '6962', '6972', '6977', '4965', '4963', '4962', '6974', '6952',
#        '6984', '4952', '6921', '4942', '4964', '6957', '6973', '4957', '4953',
#        '6967', '6954', '4955', '6965'],
#       dtype='object')
# '''
# #print(value_counts_graduation[4])  ## 學號4105有1968筆
# #print(value_counts_graduation[6])  ## 學號4106有1593筆

# ### 檢查學號欄位是否有重複的
# df_graduation_total_NoNA['學號'].value_counts(ascending=False)
# '''
# 410307814    5
# 410402957    4
# 410305757    4
# 410109402    4
# 410214362    4
# ...
# '''
# #df_graduation_total_NoNA[f_graduation_total_NoNA['學號'] == '410307814']
# df_graduation_total_NoNA[df_graduation_total_NoNA['學號']=='410307814']

# ### 去掉下列欄位資料相同的樣本: '調查學年','畢業學年','畢業後滿幾年','學號','job' 
# #df_graduation_total_NoNA.drop_duplicates(subset=['A','B','C','學號','job'], inplace=True)
# temp5 = df_graduation_total_NoNA.drop_duplicates(subset=['調查學年','畢業學年','畢業後滿幾年','學號','job'])
# temp5['學號'].value_counts(ascending=False)
# #df_graduation_total_NoNA['學號'].value_counts(ascending=False)
# '''
# 610600167    2
# 410316669    2
# 410314992    2
# 410315419    2
# 410315469    2
# '''
# #df_graduation_total_NoNA[df_graduation_total_NoNA['學號']=='410316669']
# temp5[temp5['學號']=='410316669']
# '''
# 此位同學107學年畢業, 有 2 筆資料: 畢業滿 1, 3 年:
#         調查學年   畢業學年  畢業後滿幾年  ...        J    K 學號_first4
# 9093   110.0  107.0     3.0  ...  34000.0  NaN      4103
# 13103  108.0  107.0     1.0  ...  28000.0  NaN      4103
# '''

# ### 去掉下列欄位資料相同的樣本: '學號'
# temp1 = df_graduation_total_NoNA.drop_duplicates(subset=['學號'])
# temp1['學號'].value_counts(ascending=False)  ## 沒有重複資料了

# ### 去掉下列欄位資料相同的樣本: '畢業後滿幾年','學號'
# #temp2 = df_graduation_total_NoNA.drop_duplicates(subset=['畢業後滿幾年','學號'])
# #temp2['學號'].value_counts(ascending=False)  ## 
# df_graduation_total_NoNA.drop_duplicates(subset=['畢業後滿幾年','學號'],inplace=True)
# df_graduation_total_NoNA['學號'].value_counts(ascending=False)  ## 
# '''
# 610600167    2
# 410316669    2
# 410314992    2
# 410315419    2
# 410315469    2
# '''

# # ### 繪製長條圖
# # import matplotlib.pyplot as plt
# # value_counts_graduation.plot(kind='bar')
# # plt.xlabel('Unique Values')
# # plt.ylabel('Frequency')
# # plt.title('Frequency of Unique Values in column_name')
# # plt.show()




# #### UCAN 與 畢業生流向資料整合:
# ###
# df_total_ucan105To112 = pd.merge(df_ucan105To112, df_graduation_total_NoNA, how="inner", on='學號')
# df_total_ucan105To112.drop('學號_first4_y', axis=1, inplace=True)
# df_total_ucan105To112.rename(columns={'學號_first4_x': '學號_first4'}, inplace=True)

# df_total_ucan105To112.head()
# df_total_ucan105To112.shape  ## (3169, 29), 29 = 19 + 12 - 1 -1
# df_total_ucan105To112.columns
# df_total_ucan105To112.to_excel(r'C:\Users\user\Dropbox\系務\校務研究IR\資料\UCan\整理後資料 (Lo)\UCAN畢業生流向合併資料\UCAN畢業生流向合併資料_ucan105To112.xlsx', index=False)

# ###
# df_total_ucan100To112 = pd.merge(df_ucan100To112, df_graduation_total_NoNA, how="inner", on='學號')
# df_total_ucan100To112.drop('學號_first4_y', axis=1, inplace=True)
# df_total_ucan100To112.rename(columns={'學號_first4_x': '學號_first4'}, inplace=True)
# df_total_ucan100To112.head()
# df_total_ucan100To112.shape  ## (17154, 29), 29 = 19 + 12 - 1 -1
# df_total_ucan100To112.columns
# df_total_ucan100To112.to_excel(r'C:\Users\user\Dropbox\系務\校務研究IR\資料\UCan\整理後資料 (Lo)\UCAN畢業生流向合併資料\UCAN畢業生流向合併資料_ucan100To112.xlsx', index=False)
# df_total_ucan100To112.iloc[0,:]

# ### UCAN 與 畢業生流向 整合資料中學號資料不是以4開頭
# filtered_df = df_total_ucan100To112[~df_total_ucan100To112['學號'].str.startswith('4')]
# filtered_df.to_excel(r'C:\Users\user\Dropbox\系務\校務研究IR\資料\UCan\整理後資料 (Lo)\UCAN畢業生流向合併資料\UCAN畢業生流向合併資料學號資料不是以4開頭.xlsx', index=False)

# ### 獲得UCAN 與 畢業生流向 整合資料中, 不同入學年度的樣本數分佈(藉由學號前四碼)
# value_counts_UCANgraduation = df_total_ucan100To112['學號_first4'].value_counts()
# #type(value_counts_UCANgraduation)  ## pandas.core.series.Series
# #value_counts_UCANgraduation.index   
# value_counts_UCANgraduation[:20]  ## 學號4105開頭有1517筆, 學號4106開頭有1311筆

# ### 檢查學號欄位是否有重複的 (重複的原因是有不同的 "畢業後滿幾年" 值)
# df_total_ucan100To112['學號'].value_counts(ascending=False) 
# '''
# 410422135    2
# 410214150    2
# 410307987    2
# 410307953    2
# 410307929    2
# '''
# df_total_ucan100To112.head()
# df_total_ucan100To112.columns


# ####
# ### 挑選 '畢業後滿幾年' = 1
# #type(df_total_ucan100To112['畢業後滿幾年'][0])  ## numpy.float64
# #df_total_ucan100To112['畢業後滿幾年'] = df_total_ucan100To112['畢業後滿幾年'].astype(str) ## 資料型態從 numpy.float64 變成 str
# df_total_ucan100To112_after1 = df_total_ucan100To112[df_total_ucan100To112['畢業後滿幾年']==1]  ## [6664 rows x 29 columns]
# df_total_ucan100To112_after1.shape  ## (6664, 29)
# df_total_ucan100To112_after1['畢業後滿幾年']

# ### 挑選 '畢業後滿幾年' = 3
# df_total_ucan100To112_after3 = df_total_ucan100To112[df_total_ucan100To112['畢業後滿幾年']==3]  ## 
# df_total_ucan100To112_after3.shape  ## (6418, 29)
# df_total_ucan100To112_after3['畢業後滿幾年']

# ### 挑選 '畢業後滿幾年' = 5
# df_total_ucan100To112_after5 = df_total_ucan100To112[df_total_ucan100To112['畢業後滿幾年']==5]  ## 
# df_total_ucan100To112_after5.shape  ## (4072, 29)
# df_total_ucan100To112_after5['畢業後滿幾年']

# ### 挑選 '畢業後滿幾年' = 2
# df_total_ucan100To112_after2 = df_total_ucan100To112[df_total_ucan100To112['畢業後滿幾年']==2]  ## 
# df_total_ucan100To112_after2.shape  ## (0, 29)

# ### 挑選 '畢業後滿幾年' = 4
# df_total_ucan100To112_after4 = df_total_ucan100To112[df_total_ucan100To112['畢業後滿幾年']==4]  ## 
# df_total_ucan100To112_after4.shape  ## (0, 29)
