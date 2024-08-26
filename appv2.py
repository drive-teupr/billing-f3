import pandas as pd
import streamlit as st
import numpy as np
import webbrowser

from st_aggrid import AgGrid, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder
from streamlit.components.v1 import html

def copyDataframe(lalu, akhir, blth_lalu, blth_kini):
    # BUAT DATAFRAME JURUSJURUSAN

    juruslalu = pd.DataFrame()

    juruslalu['IDPEL'] = lalu['IDPEL']
    juruslalu['PEMKWH'] = lalu['PEMKWH']
    juruslalu['DLPD'] = lalu['DLPD']
    juruslalu['LWBP_LALU'] = lalu['SLALWBP']
    juruslalu['LWBP_CABUT'] = lalu['SAHLWBP_CABUT']
    juruslalu['LWBP_PASANG'] = lalu['SLALWBP_PASANG']
    juruslalu['LWBP_AKHIR'] = lalu['SAHLWBP']
    juruslalu['WBP_LALU'] = lalu['SLAWBP']
    juruslalu['WBP_CABUT'] = lalu['SAHWBP_CABUT']
    juruslalu['WBP_PASANG'] = lalu['SLAWBP_PASANG']
    juruslalu['WBP_AKHIR'] = lalu['SAHWBP']
    juruslalu['FAKM'] = lalu['FAKM']
    juruslalu['PEMKWH_REAL'] = (((juruslalu['LWBP_AKHIR']-juruslalu['LWBP_PASANG'])
                                +(juruslalu['LWBP_CABUT']-juruslalu['LWBP_LALU']))
                                +((juruslalu['WBP_AKHIR']-juruslalu['WBP_PASANG'])
                                +(juruslalu['WBP_CABUT']-juruslalu['WBP_LALU']))
                                )

    jurusakhir = pd.DataFrame()

    jurusakhir['IDPEL'] = akhir['IDPEL']
    jurusakhir['NAMA'] = akhir['NAMA']
    jurusakhir['PEMKWH'] = akhir['PEMKWH']
    jurusakhir['TARIF'] = akhir['TARIF']
    jurusakhir['DAYA'] = akhir['DAYA']
    jurusakhir['DLPD'] = akhir['DLPD']
    jurusakhir['LWBP_LALU'] = akhir['SLALWBP']
    jurusakhir['LWBP_CABUT'] = akhir['SAHLWBP_CABUT']
    jurusakhir['LWBP_PASANG'] = akhir['SLALWBP_PASANG']
    jurusakhir['LWBP_AKHIR'] = akhir['SAHLWBP']
    jurusakhir['WBP_LALU'] = akhir['SLAWBP']
    jurusakhir['WBP_CABUT'] = akhir['SAHWBP_CABUT']
    jurusakhir['WBP_PASANG'] = akhir['SLAWBP_PASANG']
    jurusakhir['WBP_AKHIR'] = akhir['SAHWBP']
    jurusakhir['JAM_NYALA'] = akhir['JAMNYALA']
    jurusakhir['FAKM'] = akhir['FAKM']
    jurusakhir['PEMKWH_REAL'] = (((jurusakhir['LWBP_AKHIR']-jurusakhir['LWBP_PASANG'])
                                +(jurusakhir['LWBP_CABUT']-jurusakhir['LWBP_LALU']))
                                +((jurusakhir['WBP_AKHIR']-jurusakhir['WBP_PASANG'])
                                +(jurusakhir['WBP_CABUT']-jurusakhir['WBP_LALU']))
                                )
        
    kroscek_temp = pd.DataFrame()

    kroscek_temp = pd.merge(juruslalu,jurusakhir,on='IDPEL',how='right')

    kroscek = pd.DataFrame()

    kroscek['IDPEL'] = kroscek_temp['IDPEL'].astype(str)
    kroscek['NAMA'] = kroscek_temp['NAMA']
    
    path_foto1 = 'https://portalapp.iconpln.co.id/acmt/DisplayBlobServlet1?idpel='
    path_foto2 = '&blth='

    kroscek['LWBP_LALU'] = kroscek_temp['LWBP_LALU_y']
    kroscek['LWBP_AKHIR'] = kroscek_temp['LWBP_AKHIR_y']
    
    kroscek['WBP_LALU'] = kroscek_temp['WBP_LALU_y']
    kroscek['WBP_AKHIR'] = kroscek_temp['WBP_AKHIR_y']
    kroscek['PAKAI_LALU'] = kroscek_temp['PEMKWH_REAL_x']
    kroscek['PAKAI_AKHIR'] = kroscek_temp['PEMKWH_REAL_y']
    kroscek['SELISIH'] = (kroscek_temp['PEMKWH_REAL_y']-kroscek_temp['PEMKWH_REAL_x'])
    kroscek['SELISIH %'] = (kroscek['SELISIH']/kroscek_temp['PEMKWH_REAL_x'])*100
    kroscek['DLPD_LALU'] = kroscek_temp['DLPD_x']
    kroscek['DLPD_KINI'] = kroscek_temp['DLPD_y']
    kroscek['TARIF'] = kroscek_temp['TARIF']
    kroscek['DAYA'] = kroscek_temp['DAYA']
    kroscek['JAM_NYALA'] = kroscek_temp['JAM_NYALA']

    conditions_50 = [(kroscek['SELISIH %']>50) | (kroscek['SELISIH %']<-50),
                (kroscek['SELISIH %']<50) | (kroscek['SELISIH %']>-50)]

    conditions_100 = [(kroscek['SELISIH %']>100) | (kroscek['SELISIH %']<-100),
                (kroscek['SELISIH %']<100) | (kroscek['SELISIH %']>-100)]

    letters = ['Selisih Besar','Normal']

    kroscek['SELISIH 50%'] = np.select(conditions_50, letters, default='Undefined')
    kroscek['SELISIH 100%'] = np.select(conditions_100, letters, default='Undefined')

    conditions_sub = [(kroscek['DAYA']==450) | (kroscek['DAYA']==900),
                (kroscek['DAYA']>900)]

    letters_sub = ['Subs','Nonsubs']

    kroscek['SUBS_NONSUBS'] = np.select(conditions_sub, letters_sub, default='Undefined')

    conditions_minnol = [(kroscek['DLPD_LALU']=='K KWH NOL') | (kroscek['DLPD_LALU']=='C KWH < 40 JAM'),
                (kroscek['DLPD_LALU']=='N KWH N O R M A L') | (kroscek['DLPD_LALU']=='J REKENING PECAHAN')]

    letters_minnol = ['Yes','No']

    kroscek['MIN_NOL'] = np.select(conditions_minnol, letters_minnol, default='Undefined')

    kroscek['FOTO_LALU'] = path_foto1+kroscek['IDPEL']+path_foto2+blth_lalu+'&unitup=32510'
    kroscek['FOTO_AKHIR'] = path_foto1+kroscek['IDPEL']+path_foto2+blth_kini+'&unitup=32510'

    return kroscek

def maksFilter(lalu, akhir, blth_lalu, blth_kini):
    kroscek = copyDataframe(lalu, akhir, blth_lalu, blth_kini)
    maks_df = kroscek[kroscek['DLPD_KINI'].isin(['L STAND METER MUNDUR'])]
    return maks_df

def norm1Filter(lalu, akhir, blth_lalu, blth_kini):
    kroscek = copyDataframe(lalu, akhir, blth_lalu, blth_kini)
    
    temp = kroscek[kroscek['DLPD_KINI'].isin(['N KWH N O R M A L', 'J REKENING PECAHAN'])]
    temp_1 = temp[temp['SELISIH 50%'].isin(["Selisih Besar"])]
    temp_2 = temp_1[temp_1['SUBS_NONSUBS'].isin(["Subs"])]
    norm1_df = temp_2[temp_2['SELISIH 100%'].isin(["Selisih Besar"])]
    return norm1_df

def norm2Filter(lalu, akhir, blth_lalu, blth_kini):
    kroscek = copyDataframe(lalu, akhir, blth_lalu, blth_kini)
    
    temp = kroscek[kroscek['DLPD_KINI'].isin(['N KWH N O R M A L', 'J REKENING PECAHAN'])]
    temp_1 = temp[temp['SELISIH 50%'].isin(["Selisih Besar"])]
    norm2_df = temp_1[temp_1['SUBS_NONSUBS'].isin(["Nonsubs"])]
    return norm2_df

def minNolFilter(lalu, akhir, blth_lalu, blth_kini):
    kroscek = copyDataframe(lalu, akhir, blth_lalu, blth_kini)
    
    temp = kroscek[kroscek['DLPD_KINI'].isin(["C KWH < 40 JAM", "K KWH NOL"])]
    minNol_df = temp[temp['MIN_NOL'].isin(['No'])]
    minNol_df = minNol_df.reset_index()
    return minNol_df

def open_page(url):
    open_script = """
        <script type="text/javascript">
            window.open('%s', '_blank').focus();
        </script>
    """ % (url)
    html(open_script)

st.set_page_config(page_title='Verifikasi F3 2.0',
                   layout="wide")

st.header('Billing Management Application 2.0')

# Layout dengan dua kolom
col1, col2 = st.columns((1.5, 5), gap='medium')

with col1:
    set_bulan = st.columns((0.75,0.75), gap='medium')
    
    with set_bulan[0]:
        blth_lalu = st.text_input('Masukkan periode bulan lalu (YYYYMM)')

    with set_bulan[1]:
        blth_kini = st.text_input('Masukkan periode bulan kini (YYYYMM)')
    
    file_lalu = st.file_uploader("Upload Data Periode Sebelumnya")
    file_akhir = st.file_uploader("Upload Data Periode Sekarang")

    if st.button("Proses"):
        st.write("DataFrame ditampilkan di kolom kedua.")
        # Update status untuk tombol-tombol tambahan di kolom kedua
        st.session_state['show_df'] = True

with col2:
    if 'show_df' in st.session_state and st.session_state['show_df']:
        lalu = pd.read_excel(file_lalu)
        akhir = pd.read_excel(file_akhir)

        # Menampilkan DataFrame dan tombol di kolom kedua
        # Tabs untuk tombol-tombol tambahan
        st.markdown('#### Main')
        tabs = st.tabs(['SEMUA','KWH MAKS', 'NORMAL', 'NORMAL > 900', '0-40 JN'])
        for i, tab in enumerate(tabs):
            tabs[i].write()
        
        with tabs[0]:
            st.write("Semua")
            st.dataframe(copyDataframe(lalu, akhir, blth_lalu, blth_kini))

        with tabs[1]:
            st.write("KWH Maks > 720 JN")
            df_maks = maksFilter(lalu, akhir, blth_lalu, blth_kini)
            st.dataframe(df_maks)
            st.write(len(df_maks))
            if st.button("Lihat Foto KWh Maks"):
                for url in df_maks['FOTO_AKHIR']:
                    open_page(url)
        
        with tabs[2]:
            st.write("Normal Daya 450-900 VA")
            df_norm1 = norm1Filter(lalu, akhir, blth_lalu, blth_kini)
            st.dataframe(df_norm1)
            st.write(len(df_norm1))
            if st.button("Lihat Foto Normal Subsidi"):
                for url in df_norm1['FOTO_AKHIR']:
                    open_page(url)
                
        with tabs[3]:
            st.write("Normal Daya > 900")
            df_norm2 = norm2Filter(lalu, akhir, blth_lalu, blth_kini)
            st.dataframe(df_norm2)
            st.write(len(df_norm2))
            if st.button("Lihat Foto Normal Non Subsidi"):
                for url in df_norm2['FOTO_AKHIR']:
                    open_page(url)
        
        with tabs[4]:
            st.write("KWH Nol 40 JN")
            df_minNol = minNolFilter(lalu, akhir, blth_lalu, blth_kini)
            st.dataframe(df_minNol)
            st.write(len(df_minNol))
            if st.button("Lihat Foto 0-40 JN"):
                for url in df_minNol['FOTO_AKHIR']:
                    open_page(url)

    else:
        st.write("Tekan 'Proses' untuk menampilkan DataFrame dan tombol tambahan.")
