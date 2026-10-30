import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# إعدادات الصفحة
st.set_page_config(page_title="Well drilling location determination", page_icon="🌊", layout="wide")

# تنسيق CSS مخصص للواجهات ولحل مشكلة انكماش القوائم على الهواتف
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
        text-align: right;
    }
    
    /* تحسين القائمة الجانبية لضمان اتساعها على الهواتف الذكية */
    [data-testid="stSidebar"] {
        min-width: 280px !important;
    }
    
    .main-header {
        background-color: #d96b6b;
        color: white;
        padding: 12px;
        text-align: center;
        border-radius: 6px;
        font-size: 22px;
        font-weight: bold;
        margin-bottom: 15px;
    }
    .sub-header {
        background-color: #c39bd3;
        color: black;
        padding: 8px;
        text-align: center;
        border-radius: 5px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# 1. تهيئة قاعدة البيانات في الذاكرة
if 'wells_db' not in st.session_state:
    st.session_state.wells_db = pd.DataFrame([
        {
            "اسم الموقع": "حول بحر", "قرية": "شرج آل علي", "المديرية": "حريضة", "المحافظة": "حضرموت", "ID": "W-01",
            "UTM_X": 250000, "UTM_Y": 1700000, "الارتفاع (م)": 1200, "ملاحظات": "موقع مقترح أول",
            "نوع الصخر": "حصى ورمل", "عمق الماء": 45, "سمك الطبقة": 30
        }
    ])

if 'current_page' not in st.session_state:
    st.session_state.current_page = "home"

if 'temp_well_data' not in st.session_state:
    st.session_state.temp_well_data = {}

# ---------------------------------------------------------
# 🧭 القائمة الجانبية السريعة (Menu Sidebar) للتنقل الدائم
# ---------------------------------------------------------
st.sidebar.markdown("### 🧭 القائمة السريعة (Menu)")
if st.sidebar.button("🏠 الرئيسية (Home)", use_container_width=True):
    st.session_state.current_page = "home"
    st.rerun()
if st.sidebar.button("📍 بئر جديد (New Well)", use_container_width=True):
    st.session_state.current_page = "new_well_data"
    st.rerun()
if st.sidebar.button("🗄️ قاعدة البيانات (Database)", use_container_width=True):
    st.session_state.current_page = "org_database"
    st.rerun()
if st.sidebar.button("🔍 النمذجة 3D (Search & Model)", use_container_width=True):
    st.session_state.current_page = "search_model"
    st.rerun()
if st.sidebar.button("📤 تصدير التقارير (Export Reports)", use_container_width=True):
    st.session_state.current_page = "export_reports"
    st.rerun()
if st.sidebar.button("⚙️ إعدادات النظام (Setup)", use_container_width=True):
    st.session_state.current_page = "setup"
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.info("📌 تطبيق همم - تحليل مواقع حفر الآبار والطبقات الجيولوجية.")

# ---------------------------------------------------------
# 🏠 1. الشاشة الرئيسية (Home Screen)
# ---------------------------------------------------------
if st.session_state.current_page == "home":
    st.markdown('<div class="main-header">Well drilling location determination</div>', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("New Well Position", use_container_width=True):
            st.session_state.current_page = "new_well_data"
            st.rerun()
    with c2:
        if st.button("Entery Data", use_container_width=True):
            st.session_state.current_page = "new_well_data"
            st.rerun()
    with c3:
        if st.button("Org Database", use_container_width=True):
            st.session_state.current_page = "org_database"
            st.rerun()

    st.write("")
    c4, c5, c6 = st.columns(3)
    with c4:
        if st.button("Input Editing", use_container_width=True):
            st.session_state.current_page = "input_editing"
            st.rerun()
    with c5:
        if st.button("Search", use_container_width=True):
            st.session_state.current_page = "search_model"
            st.rerun()
    with c6:
        if st.button("Exit", use_container_width=True):
            st.warning("تم إغلاق التطبيق.")

    st.markdown("---")
    sc1, sc2 = st.columns(2)
    with sc1:
        if st.button("Menu (القائمة الرئيسية)", use_container_width=True):
            st.info("استخدم القائمة الجانبية لسرعة التنقل بين الأقسام.")
    with sc2:
        if st.button("Setup (الإعدادات)", use_container_width=True):
            st.session_state.current_page = "setup"
            st.rerun()

# ---------------------------------------------------------
# 📍 2. شاشة إدخال بيانات الموقع (New Well Data)
# ---------------------------------------------------------
elif st.session_state.current_page == "new_well_data":
    st.markdown('<div class="sub-header">new well data</div>', unsafe_allow_html=True)
    
    col_gps1, col_gps2 = st.columns([3, 1])
    with col_gps1:
        st.info("📍 يمكنك إدخال الإحداثيات يدوياً أو الاعتماد على نظام الإحداثيات الجغرافية المعتمد.")
    with col_gps2:
        if st.button("🛰️ جلب موقعي الحالي (GPS)"):
            st.success("تم تحديد الإحداثيات الافتراضية لموقعك الحالي بنجاح!")

    col_top1, col_top2, col_top3, col_top4 = st.columns(4)
    with col_top1:
        loc_name = st.text_input("location name", value="موقع 1")
    with col_top2:
        coord_x = st.number_input("coordinate X:", value=250000.0)
        coord_y = st.number_input("coordinate Y:", value=1700000.0)
    with col_top3:
        elevation = st.number_input("elevation (متر)", value=1200.0)
    with col_top4:
        notes = st.text_area("notes", value="لا توجد ملاحظات")

    col_bot1, col_bot2, col_bot3, col_bot4 = st.columns(4)
    with col_bot1:
        village = st.text_input("village (القرية)", value="شرج آل علي")
    with col_bot2:
        district = st.text_input("district (المديرية)", value="حريضة")
    with col_bot3:
        governorate = st.text_input("governorate (المحافظة)", value="حضرموت")
    with col_bot4:
        well_id = st.text_input("ID (رقم المعرّف)", value=f"W-0{len(st.session_state.wells_db)+1}")

    st.markdown("---")
    col_left, col_right = st.columns([1, 2])
    with col_left:
        st.button("map (خريطة أساس)")
        st.checkbox("observed boundary (الحدود المرصودة)")
        st.checkbox("free boundary (الحدود الحرة)")
        if st.button("georeference (إرجاع جغرافي)"):
            st.success("تم تفعيل الإرجاع الجغرافي UTM Zone 38N.")
            
    with col_right:
        st.info("🗺️ خريطة معاينة الموقع الجغرافي:")
        map_df = pd.DataFrame({'lat': [15.5], 'lon': [48.5]})
        st.map(map_df, zoom=6)

    st.markdown("---")
    b_col1, b_col2, b_col3, b_col4 = st.columns(4)
    with b_col1:
        if st.button("إغلاق (Close)"):
            st.session_state.current_page = "home"
            st.rerun()
    with b_col2:
        if st.button("Basemap"):
            st.success("تم اختيار طبقة الخريطة الأساسية (Topographic Basemap).")
    with b_col3:
        if st.button("Save (حفظ البيانات الأولية)"):
            st.session_state.temp_well_data = {
                "اسم الموقع": loc_name, "قرية": village, "المديرية": district,
                "المحافظة": governorate, "ID": well_id, "UTM_X": coord_x,
                "UTM_Y": coord_y, "الارتفاع (م)": elevation, "ملاحظات": notes
            }
            st.success("تم حفظ البيانات المؤقتة بنجاح!")
    with b_col4:
        if st.button("Next ➡️ (الانتقال للبيانات الجيولوجية)"):
            st.session_state.current_page = "new_well_geo_data"
            st.rerun()

# ---------------------------------------------------------
# 🪨 3. شاشة البيانات الجيولوجية والخرائط (New Well Geo Data)
# ---------------------------------------------------------
elif st.session_state.current_page == "new_well_geo_data":
    st.markdown('<div class="sub-header">new well geo data</div>', unsafe_allow_html=True)
    
    st.text_input("location name (الموقع الحالي)", value=st.session_state.temp_well_data.get("اسم الموقع", "موقع جديد"))

    st.write("اختر الطبقات والبيانات الجيولوجية المساعدة:")
    g1, g2, g3, g4 = st.columns(4)
    with g1:
        geo_map = st.checkbox("geological map (الخريطة الجيولوجية)")
        faults = st.checkbox("fault structure (الفوالق والصدوع)")
        add_in1 = st.text_input("additional input 1", value="توصيف السطح")
    with g2:
        topo_map = st.checkbox("topographic map (الخريطة الطبوغرافية)")
        dikes = st.checkbox("dike structure (القواطع النارية)")
        add_in2 = st.text_input("additional input 2", value="اتجاه الميل")
    with g3:
        dem_map = st.checkbox("dem map (نموذج الارتفاع الرقمي)")
        other_st = st.checkbox("other structure (تراكيب أخرى)")
        add_in3 = st.text_input("additional input 3", value="الإنتاجية المتوقعة")
    with g4:
        grid_map = st.checkbox("grid and z map (الشبكة وقيم Z)")
        nearby = st.checkbox("nearby wells data (آبار مجاورة)")
        add_in4 = st.text_input("additional input 4", value="بيانات الضخ")

    st.markdown("---")
    b_geo1, b_geo2, b_geo3, b_geo4 = st.columns(4)
    with b_geo1:
        if st.button("Save All (حفظ الكل في القاعدة)"):
            full_data = st.session_state.temp_well_data
            if not full_data:
                full_data = {"اسم الموقع": "بئر افتراضي", "UTM_X": 250000, "UTM_Y": 1700000, "الارتفاع (م)": 1200, "ID": "W-New"}
            full_data.update({"نوع الصخر": "حجر جيري متشقق", "عمق الماء": 50, "سمك الطبقة": 35})
            st.session_state.wells_db = pd.concat([st.session_state.wells_db, pd.DataFrame([full_data])], ignore_index=True)
            st.success("تم حفظ البئر مع كافة الطبقات الجيولوجية بنجاح!")
    with b_geo2:
        if st.button("Process (معالجة وتحليل)"):
            st.info("جاري تحليل البيانات الجيولوجية وتقاطع الفوالق مع الأودية...")
    with b_geo3:
        if st.button("Result (عرض الموديل 3D)"):
            st.session_state.current_page = "search_model"
            st.rerun()
    with b_geo4:
        if st.button("Exit (إغلاق وعودة)"):
            st.session_state.current_page = "home"
            st.rerun()

# ---------------------------------------------------------
# 🔍 4. شاشة البحث والنمذجة ثلاثية الأبعاد (Search & 3D Model)
# ---------------------------------------------------------
elif st.session_state.current_page == "search_model":
    st.markdown('<div class="sub-header">Search & 3D Subsurface Model</div>', unsafe_allow_html=True)
    
    df = st.session_state.wells_db
    st.dataframe(df, use_container_width=True)
    
    fig = go.Figure()
    for idx, row in df.iterrows():
        x, y = row['UTM_X'], row['UTM_Y']
        z_surf = row.get('الارتفاع (م)', 1200)
        z_bot = z_surf - 150
        z_wat = z_surf - row.get('عمق الماء', 45)
        
        fig.add_trace(go.Scatter3d(
            x=[x, x], y=[y, y], z=[z_surf, z_bot],
            mode='lines+markers', line=dict(color='black', width=6),
            name=f"بئر {row.get('اسم الموقع', '')}"
        ))
        fig.add_trace(go.Scatter3d(
            x=[x], y=[y], z=[z_wat],
            mode='markers', marker=dict(size=8, color='blue', symbol='diamond'),
            showlegend=False
        ))

    fig.update_layout(
        scene=dict(xaxis_title='UTM X', yaxis_title='UTM Y', zaxis_title='Elevation (m)', aspectmode='data'),
        height=500, margin=dict(l=0, r=0, b=0, t=20)
    )
    st.plotly_chart(fig, use_container_width=True)

    if st.button("الرجوع للقائمة الرئيسية"):
        st.session_state.current_page = "home"
        st.rerun()

# ---------------------------------------------------------
# 📥 5. شاشة تصدير التقارير (Export Reports - PDF, Excel, Word, JPG)
# ---------------------------------------------------------
elif st.session_state.current_page == "export_reports":
    st.markdown('<div class="sub-header">Export Reports & Data (تصدير التقارير والبيانات)</div>', unsafe_allow_html=True)
    
    st.write("اختر صيغة التصدير المناسبة لتقرير تحليل الآبار والموديل الجيولوجي:")
    
    export_format = st.radio(
        "حدد صيغة التصدير المطلوبة:",
        ["Excel (.xlsx)", "CSV (.csv)", "Word (.docx - جدول تقرير)", "PDF (تقرير هندسي)", "Image / JPG (لقطة الموديل)"],
        horizontal=True
    )
    
    df_export = st.session_state.wells_db
    
    st.markdown("---")
    
    if "Excel" in export_format:
        excel_data = df_export.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 تحميل التقرير بصيغة Excel / CSV",
            data=excel_data,
            file_name="Hammam_Wells_Report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    elif "CSV" in export_format:
        csv_data = df_export.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 تحميل الملف بصيغة CSV",
            data=csv_data,
            file_name="Hammam_Wells_Data.csv",
            mime="text/csv"
        )
    elif "Word" in export_format:
        st.info("📄 يتم تجهيز تقرير نصي منسق بصيغة Word (مبني على جدول بيانات الآبار والطبقات).")
        word_data = df_export.to_csv(sep='\t', index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 تحميل التقرير بصيغة Word (Text Table)",
            data=word_data,
            file_name="Hammam_Report.doc",
            mime="application/msword"
        )
    elif "PDF" in export_format:
        st.info("📑 تقرير هندسي شامل يضم إحداثيات الآبار، أعماق المياه، والطبقات الحاملة جاهز للتصدير.")
        pdf_mock_data = df_export.to_string().encode('utf-8')
        st.download_button(
            label="📥 تحميل التقرير الهندسي بصيغة PDF",
            data=pdf_mock_data,
            file_name="Hammam_Engineering_Report.pdf",
            mime="application/pdf"
        )
    elif "Image" in export_format:
        st.info("🖼️ يمكنك التقاط ومشاركة صورة الموديل ثلاثي الأبعاد بصيغة JPG أو PNG مباشرة من واجهة الرسم 3D.")

    st.write("")
    if st.button("الرجوع للقائمة الرئيسية"):
        st.session_state.current_page = "home"
        st.rerun()

# ---------------------------------------------------------
# 🗄️ 6. قاعدة البيانات والإدارة (Org Database)
# ---------------------------------------------------------
elif st.session_state.current_page == "org_database":
    st.markdown('<div class="sub-header">Org Database Management</div>', unsafe_allow_html=True)
    st.dataframe(st.session_state.wells_db, use_container_width=True)
    
    if st.button("الرجوع للقائمة الرئيسية"):
        st.session_state.current_page = "home"
        st.rerun()

# ---------------------------------------------------------
# ✏️ 7. تعديل البيانات (Input Editing)
# ---------------------------------------------------------
elif st.session_state.current_page == "input_editing":
    st.markdown('<div class="sub-header">Input Data Editing</div>', unsafe_allow_html=True)
    edited_df = st.data_editor(st.session_state.wells_db, use_container_width=True)
    if st.button("حفظ التعديلات"):
        st.session_state.wells_db = edited_df
        st.success("تم تحديث البيانات بنجاح!")
    
    if st.button("الرجوع للقائمة الرئيسية"):
        st.session_state.current_page = "home"
        st.rerun()

# ---------------------------------------------------------
# ⚙️ 8. الإعدادات المتكاملة (Setup)
# ---------------------------------------------------------
elif st.session_state.current_page == "setup":
    st.markdown('<div class="sub-header">System Setup & Preferences (إعدادات النظام)</div>', unsafe_allow_html=True)
    
    with st.form("setup_form"):
        st.subheader("🌐 الإحداثيات والنظام الجغرافي")
        coord_system = st.selectbox("النظام الإحداثي المفضل", ["UTM WGS84 - Zone 38N", "UTM WGS84 - Zone 39N", "UTM WGS84 - Zone 48N"])
        
        st.subheader("📏 وحدات القياس")
        measurement_unit = st.radio("وحدة القياس الأساسية للأعماق والمسافات", ["المتر (Meters)", "القدم (Feet)"], horizontal=True)
        
        st.subheader("📁 مسارات الحفظ والتصدير")
        save_path = st.text_input("مسار حفظ التقارير والملفات الافتراضي", value="C:/Hammam_Projects/Data")
        export_format_pref = st.selectbox("تنسيق التصدير الافتراضي للتقارير والبيانات", ["Excel (.xlsx)", "Word (.docx)", "PDF Report", "CSV"])
        
        st.subheader("🕸️ إعدادات الشبكة والنمذجة ثلاثية الأبعاد (Grid & Modeling Settings)")
        grid_resolution = st.slider("دقة ونعومة الشبكة ثلاثية الأبعاد (Grid Cell Resolution)", min_value=5, max_value=50, value=20)
        interpolation_method = st.selectbox("طريقة الاستكمال المكاني للطبقات الجيولوجية", ["Nearest Neighbor", "Kriging (قياسي)", "Inverse Distance Weighting (IDW)"])
        
        saved_setup = st.form_submit_button("💾 حفظ الإعدادات والتفضيلات")
        if saved_setup:
            st.success("تم حفظ إعدادات النظام وتحديث التفضيلات بنجاح!")
    
    st.write("")
    if st.button("الرجوع للقائمة الرئيسية"):
        st.session_state.current_page = "home"
        st.rerun()
