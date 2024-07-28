import numpy as np
import pandas as pd

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
    
    path_foto1 = 'https://portalapp.iconpln.co.id/acmt/DisplayBlobServlet1?idpel='
    path_foto2 = '&blth='

    kroscek['LWBP_LALU'] = kroscek_temp['LWBP_LALU_y']
    kroscek['FOTO_LALU'] = path_foto1+kroscek['IDPEL']+path_foto2+blth_lalu

    kroscek['LWBP_AKHIR'] = kroscek_temp['LWBP_AKHIR_y']
    kroscek['FOTO_AKHIR'] = path_foto1+kroscek['IDPEL']+path_foto2+blth_kini

    kroscek['WBP_LALU'] = kroscek_temp['WBP_LALU_y']
    kroscek['WBP_AKHIR'] = kroscek_temp['WBP_AKHIR_y']
    kroscek['PAKAI_LALU'] = kroscek_temp['PEMKWH_REAL_x']
    kroscek['PAKAI_AKHIR'] = kroscek_temp['PEMKWH_REAL_y']
    kroscek['SELISIH'] = kroscek_temp['PEMKWH_REAL_y']-kroscek_temp['PEMKWH_REAL_x']
    kroscek['SELISIH %'] = (kroscek['SELISIH']/kroscek_temp['PEMKWH_REAL_x'])*100
    kroscek['DLPD_LALU'] = kroscek_temp['DLPD_x']
    kroscek['DLPD_KINI'] = kroscek_temp['DLPD_y']
    kroscek['TARIF'] = kroscek_temp['TARIF']
    kroscek['DAYA'] = kroscek_temp['DAYA']
    kroscek['JAM_NYALA'] = kroscek_temp['JAM_NYALA']

    conditions_50 = [(kroscek['SELISIH']>50) | (kroscek['SELISIH']<-50),
                (kroscek['SELISIH']<50) | (kroscek['SELISIH']>-50)]

    conditions_100 = [(kroscek['SELISIH']>100) | (kroscek['SELISIH']<-100),
                (kroscek['SELISIH']<100) | (kroscek['SELISIH']>-100)]

    letters = ['Selisih Besar','Normal']

    kroscek['SELISIH 50%'] = np.select(conditions_50, letters)
    kroscek['SELISIH 100%'] = np.select(conditions_100, letters)

    conditions_sub = [(kroscek['DAYA']==450) | (kroscek['DAYA']==900),
                (kroscek['DAYA']>900)]

    letters_sub = ['Subs','Nonsubs']

    kroscek['SUBS_NONSUBS'] = np.select(conditions_sub, letters_sub)

    conditions_minnol = [(kroscek['DLPD_LALU']=='K KWH NOL') | (kroscek['DLPD_LALU']=='C KWH < 40 JAM'),
                (kroscek['DLPD_LALU']=='N KWH N O R M A L') | (kroscek['DLPD_LALU']=='J REKENING PECAHAN')]

    letters_minnol = ['Yes','No']

    kroscek['MIN_NOL'] = np.select(conditions_minnol, letters_minnol)
    return kroscek

def amrFilter(lalu, akhir, blth_lalu, blth_kini):
    kroscek = copyDataframe(lalu, akhir, blth_lalu, blth_kini)
    criteria1 = ['L STAND MUNDUR', 'N KWH N O R M A L', 'K KWH NOL', 
                 'C KWH < 40 JAM', 'J REKENING PECAHAN']
    
    amr_df = kroscek[kroscek['DLPD_KINI'].isin(criteria1)]
    amr_df = amr_df[amr_df['SELISIH 50%'].isin(["Selisih Besar"])]
    del amr_df['FOTO_LALU']
    del amr_df['FOTO_AKHIR']
    return amr_df

def maksFilter(lalu, akhir, blth_lalu, blth_kini):
    kroscek = copyDataframe(lalu, akhir, blth_lalu, blth_kini)
    maks_df = kroscek[kroscek['DLPD_KINI'].isin(['L STAND METER MUNDUR'])]
    return maks_df

def norm1Filter(lalu, akhir, blth_lalu, blth_kini):
    kroscek = copyDataframe(lalu, akhir, blth_lalu, blth_kini)
    
    norm1_df = kroscek[kroscek['DLPD_KINI'].isin(['N KWH N O R M A L'])]
    norm1_df = norm1_df[norm1_df['SELISIH 50%'].isin(["Selisih Besar"])]
    norm1_df = norm1_df[norm1_df['SUBS_NONSUBS'].isin(["Subs"])]
    return norm1_df

def norm2Filter(lalu, akhir, blth_lalu, blth_kini):
    kroscek = copyDataframe(lalu, akhir, blth_lalu, blth_kini)
    
    norm2_df = kroscek[kroscek['DLPD_KINI'].isin(['N KWH N O R M A L'])]
    norm2_df = norm2_df[norm2_df['SELISIH 50%'].isin(["Selisih Besar"])]
    norm2_df = norm2_df[norm2_df['SUBS_NONSUBS'].isin(["Nonsubs"])]
    return norm2_df

def minNolFilter(lalu, akhir, blth_lalu, blth_kini):
    kroscek = copyDataframe(lalu, akhir, blth_lalu, blth_kini)
    
    minNol_df = kroscek[kroscek['DLPD_KINI'].isin(['K KWH NOL'])]
    minNol_df = minNol_df[minNol_df['MIN_NOL'].isin(['No'])]
    return minNol_df

def show_image_maks(lalu, akhir, blth_lalu, blth_kini):
    df = pd.DataFrame(maksFilter(lalu, akhir, blth_lalu, blth_kini))
    thumbnail_renderer = JsCode("""
        class ThumbnailRenderer {
            init(params) {

            this.eGui = document.createElement('img');
            this.eGui.setAttribute('src', params.value);
            this.eGui.setAttribute('width', '250');
            this.eGui.setAttribute('height', '250');
            }
                getGui() {
                console.log(this.eGui);

                return this.eGui;
            }
        }
        """)
    
    options_builder = GridOptionsBuilder.from_dataframe(df)
    options_builder.configure_column("FOTO_LALU", cellRenderer=thumbnail_renderer)
    options_builder.configure_column("FOTO_AKHIR", cellRenderer=thumbnail_renderer)
    options_builder.configure_selection(selection_mode="single", use_checkbox=True)
    options_builder.configure_grid_options(rowHeight=250)
    grid_options = options_builder.build()

    # Create AgGrid component
    grid = AgGrid(df, 
                    gridOptions = grid_options,
                    allow_unsafe_jscode=True,
                    height=500, width=200, theme='streamlit')
    return grid

def show_image_norm1(lalu, akhir, blth_lalu, blth_kini):
    df = pd.DataFrame(norm1Filter(lalu, akhir, blth_lalu, blth_kini))
    thumbnail_renderer = JsCode("""
        class ThumbnailRenderer {
            init(params) {

            this.eGui = document.createElement('img');
            this.eGui.setAttribute('src', params.value);
            this.eGui.setAttribute('width', '250');
            this.eGui.setAttribute('height', '250');
            }
                getGui() {
                console.log(this.eGui);

                return this.eGui;
            }
        }
        """)

    options_builder = GridOptionsBuilder.from_dataframe(df)
    options_builder.configure_column("FOTO_LALU", cellRenderer=thumbnail_renderer)
    options_builder.configure_column("FOTO_AKHIR", cellRenderer=thumbnail_renderer)
    options_builder.configure_selection(selection_mode="single", use_checkbox=True)
    options_builder.configure_grid_options(rowHeight=250)
    grid_options = options_builder.build()

    # Create AgGrid component
    grid = AgGrid(df, 
                    gridOptions = grid_options,
                    allow_unsafe_jscode=True,
                    height=500, width=200, theme='streamlit')
    return grid

def show_image_norm2(lalu, akhir, blth_lalu, blth_kini):
    df = pd.DataFrame(norm2Filter(lalu, akhir, blth_lalu, blth_kini))
    thumbnail_renderer = JsCode("""
        class ThumbnailRenderer {
            init(params) {

            this.eGui = document.createElement('img');
            this.eGui.setAttribute('src', params.value);
            this.eGui.setAttribute('width', '250');
            this.eGui.setAttribute('height', '250');
            }
                getGui() {
                console.log(this.eGui);

                return this.eGui;
            }
        }
        """)
    
    options_builder = GridOptionsBuilder.from_dataframe(df)
    options_builder.configure_column("FOTO_LALU", cellRenderer=thumbnail_renderer)
    options_builder.configure_column("FOTO_AKHIR", cellRenderer=thumbnail_renderer)
    options_builder.configure_selection(selection_mode="single", use_checkbox=True)
    options_builder.configure_grid_options(rowHeight=250)
    grid_options = options_builder.build()

    # Create AgGrid component
    grid = AgGrid(df, 
                    gridOptions = grid_options,
                    allow_unsafe_jscode=True,
                    height=500, width=200, theme='streamlit')
    return grid

def show_image_minnol(lalu, akhir, blth_lalu, blth_kini):
    df = pd.DataFrame(minNolFilter(lalu, akhir, blth_lalu, blth_kini))
    thumbnail_renderer = JsCode("""
        class ThumbnailRenderer {
            init(params) {

            this.eGui = document.createElement('img');
            this.eGui.setAttribute('src', params.value);
            this.eGui.setAttribute('width', '250');
            this.eGui.setAttribute('height', '250');
            }
                getGui() {
                console.log(this.eGui);

                return this.eGui;
            }
        }
        """)
    
    options_builder = GridOptionsBuilder.from_dataframe(df)
    options_builder.configure_column("FOTO_LALU", cellRenderer=thumbnail_renderer)
    options_builder.configure_column("FOTO_AKHIR", cellRenderer=thumbnail_renderer)
    options_builder.configure_selection(selection_mode="single", use_checkbox=True)
    options_builder.configure_grid_options(rowHeight=250)
    grid_options = options_builder.build()

    # Create AgGrid component
    grid = AgGrid(df, 
                    gridOptions = grid_options,
                    allow_unsafe_jscode=True,
                    height=500, width=200, theme='streamlit')
    return grid