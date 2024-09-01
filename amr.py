import pandas as pd
import streamlit as st
import numpy as np

from st_aggrid import AgGrid, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder

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
    kroscek['PAKAI_LALU'] = kroscek_temp['PEMKWH_REAL_x']
    kroscek['PAKAI_AKHIR'] = kroscek_temp['PEMKWH_REAL_y']
    kroscek['SELISIH'] = (kroscek_temp['PEMKWH_REAL_y']-kroscek_temp['PEMKWH_REAL_x'])
    kroscek['SELISIH %'] = (kroscek['SELISIH']/kroscek_temp['PEMKWH_REAL_x'])*100
    kroscek['LWBP_LALU'] = kroscek_temp['LWBP_LALU_y']
    kroscek['LWBP_AKHIR'] = kroscek_temp['LWBP_AKHIR_y']
    kroscek['WBP_LALU'] = kroscek_temp['WBP_LALU_y']
    kroscek['WBP_AKHIR'] = kroscek_temp['WBP_AKHIR_y']
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

    return kroscek

def amrFilter(lalu, akhir, blth_lalu, blth_kini):
    amr_df = copyDataframe(lalu, akhir, blth_lalu, blth_kini)
    criteria1 = ["N KWH N O R M A L", "J REKENING PECAHAN", "L STAND METER MUNDUR", "M KWH MAXIMUM"]

    amr_df_1 = amr_df[amr_df['DLPD_KINI'].isin(criteria1)]
    amr_df_1 = amr_df_1[amr_df_1['SELISIH 50%'].isin(["Selisih Besar"])]

    # amr_df = kroscek[kroscek['DLPD_KINI'].isin(criteria1)]
    # amr_df = amr_df[amr_df['SELISIH 50%'].isin(["Selisih Besar"])]
    return amr_df_1

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
        tabs = st.tabs(['SEMUA','AMR'])
        for i, tab in enumerate(tabs):
            tabs[i].write()

        with tabs[0]:
            st.write("Semua")
            st.dataframe(copyDataframe(lalu, akhir, blth_lalu, blth_kini))
            
        with tabs[1]:
            st.write("Hasil AMR")
            st.dataframe(amrFilter(lalu, akhir, blth_lalu, blth_kini))