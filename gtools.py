import streamlit as st
import pandas as pd
import openpyxl
from streamlit_extras.stoggle import stoggle
import datetime






st.title("Assistant Tool")
col1,col2 = st.columns(2)
with col1:
  with st.expander("**OR**"):
    input_ea = st.text_area("OR Function")
    st.write("**Total = {}**".format(len(input_ea.split())))
    OR_func = ""

    for i in input_ea.split():
      OR_func += " OR {}".format(i)
    st.code(OR_func, language='sql')
    stoggle("EXCEL function",""" =textjoin(" OR ",TURE,CellRange)""")
with col2:
  with st.expander("**البحث بالعمر**"):
    start_age, end_age = st.select_slider("AGE",options=range(15,101,1), value=[15,55])
    st.code(">={} AND <={}".format(start_age,end_age), language='sql')
st.info("")

with st.expander("Dates",expanded=True):
  col1,col2,col3 = st.columns(3)
  with col1:
    d = st.date_input("إختر التاريخ",)
  with col2:
    d_days = st.number_input("عدد الأيام",value=90)
  with col3:
    st.text_input("تاريخ النهاية",value=d+datetime.timedelta(days=d_days-1))










st.info("")


st.subheader("EXTRA")

if st.checkbox("رفع ملف العينة"):
  "---"
  col1,col2 = st.columns(2)
  with col1:
    uploaded_file = st.file_uploader("xlsx اختر ملف , الصيغة المدعومة " , accept_multiple_files=False , type=['xlsx'])
  if uploaded_file is not None:
  
    df = pd.read_excel(uploaded_file, None)
    with col2:
      sheets = st.selectbox('Choose cheet - إختر الورقة',list(df.keys()))
      df = pd.read_excel(uploaded_file, sheets)
      with st.expander("sheet preview"):
        st.write(df.head(5))
    col1, col2,col3 = st.columns(3)
    "---"
    with col1:
      if 'REFERENCE_MONTH' in df.columns:
          month = st.selectbox('الشهر', sorted(df['REFERENCE_MONTH'].unique()))
          df = df[df['REFERENCE_MONTH'] == month]
    with col2:
      admin = st.selectbox('المنطقة', df['CENSUS_ADMIN_NAME'].unique())
      df = df[df['CENSUS_ADMIN_NAME'] == admin]
    
  
    filter_main = []
    for i in df['CENSUS_REGION_NAME'].unique():
      df_filter_main = df[df['CENSUS_REGION_NAME'] == i]
      filter_main.append({
          "المنطقة": df_filter_main["CENSUS_REGION_NAME"].unique(),
          "العدد": len(df_filter_main),
          "الشهر": df_filter_main['REFERENCE_MONTH'].unique()
      })
    main_data = pd.DataFrame(filter_main) ## SHEET 1
 
    with col3:
      region = st.selectbox("المدينة",df['CENSUS_REGION_NAME'].unique())
      if st.checkbox("Active"):
        df = df[df['CENSUS_REGION_NAME'] == region]
    filter_center = []
    for i in df['CENSUS_CENTER_NAME'].unique():
      df_filter_center = df[df['CENSUS_CENTER_NAME'] == i]
      filter_center.append({
          "المركز": df_filter_center['CENSUS_CENTER_NAME'].unique(),
          "عدد الأسر":len(df_filter_center)
      })
    center_data = pd.DataFrame(filter_center)
    #center_data.loc[len(center_data.index)] = ['الإجمالي',center_data['عدد الأسر'].sum()]
    
  
    with st.expander("**الإضافات**"):
      col1,col2, col3 = st.columns(3, gap='large')
      with col1:
          text = st.text_area("EA")
          st.write(len(text.split()))
          df['EA'] = df['EA'].astype(int)
          ea_text = [int(i) for i in text.split()]
          ea_list = []
          ea_list2 = []
          for week in sorted(df['REFERENCE_WEEK'].unique()):
              df_week = df[df['REFERENCE_WEEK'] == week]
              temp = df_week[df_week['EA'].isin(ea_text)]
              for i in temp['CENSUS_REGION_NAME'].unique():
                if i != 'المدينة المنورة (مقر الامارة)':
                  st.subheader(":red[duplicated]")
                  duplicated_ea = temp[temp['CENSUS_REGION_NAME'] == i]
                  st.dataframe(duplicated_ea[['EA','CENSUS_REGION_NAME']])
             
              #st.write(temp[['EA','CENSUS_REGION_NAME']])
              ea_list.append({
         
              'الأسبوع': week,
              "عدد الأسر":len(temp),
              #"الحي": temp['CENSUS_HARA_NAME'].unique()
          
          
              })
              ea_list2.append({
         
              'الأسبوع': week,
           "عدد الأسر":len(temp),
           "الحي": temp['CENSUS_REGION_NAME'].unique(),
           "EA":temp['EA'].unique()
          
          
              })
          ddd = pd.DataFrame(ea_list)
          #ddd2 = pd.DataFrame(ea_list2)
          #st.write(ddd2)
      OR_func = ""
      for i in text.split():
           OR_func += " OR {}".format(i)
      
      
      with col2:
          st.write("**كود الإسناد**")
          st.code(OR_func, language='sql')
          
      with col3:
          ddd.loc[len(ddd.index)] = ['الإجمالي',ddd['عدد الأسر'].sum()]
          ddd.loc[len(ddd.index)] = ['كود الإسناد',OR_func]
          st.dataframe(ddd,hide_index=True)
          if st.button("نسخ"):
              ddd.to_clipboard(index=False)
              st.stop()
          if st.button("Copy transpose()"):
              ddd.transpose().to_clipboard(index=False)
