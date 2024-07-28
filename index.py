import pandas as pd
import streamlit as st
from dataframe import *

from st_aggrid import AgGrid, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder

st.set_page_config(page_title='Verifikasi F3',
                   layout="wide")

col = st.columns((1.5, 5), gap='medium')

with col[0]:
    st.header('Billing Management Application')
        
    set_bulan = st.columns((0.75,0.75), gap='medium')
    
    with set_bulan[0]:
        blth_lalu = st.text_input('Masukkan periode bulan lalu (YYYYMM)')

    with set_bulan[1]:
        blth_kini = st.text_input('Masukkan periode bulan kini (YYYYMM)')
    
    file_lalu = st.file_uploader("Upload Data Periode Sebelumnya")
    file_akhir = st.file_uploader("Upload Data Periode Sekarang")

if st.button("Proses"):
    lalu = pd.read_excel(file_lalu)
    akhir = pd.read_excel(file_akhir)
    
    with col[1]:
        st.markdown('#### Main')
        tabs = st.tabs(['SEMUA','KWH MAKS', 'NORMAL', 'NORMAL > 900', '0-40 JN', 'AMR'])
        for i, tab in enumerate(tabs):
            tabs[i].write()

    with tabs[0]:
        st.write("Semua")
        st.dataframe(copyDataframe(lalu, akhir, blth_lalu, blth_kini))

    with tabs[1]: 
        st.write("KWH Maks > 720 JN")
        show_image_maks(lalu, akhir, blth_lalu, blth_kini)

    with tabs[2]:
        st.write("Normal Daya 450-900 VA")
        show_image_norm1(lalu, akhir, blth_lalu, blth_kini)

    with tabs[3]:
        st.write("Normal Daya > 900")
        show_image_norm2(lalu, akhir, blth_lalu, blth_kini)

    with tabs[4]:
        st.write("KWH Nol 40 JN")
        show_image_minnol(lalu, akhir, blth_lalu, blth_kini)

    with tabs[5]:
        st.write("Hasil AMR")
        st.dataframe(amrFilter(lalu, akhir, blth_lalu, blth_kini))