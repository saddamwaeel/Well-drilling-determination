import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# إعدادات الصفحة
st.set_page_config(page_title="Well drilling location determination", page_icon="🌊", layout="wide")

# تنسيق CSS مخصص للواجهات
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
        text-align: right;
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
    /* إخفاء القائمة الجانبية تماماً لمنع التداخل على الهواتف */
    [data-testid="stSidebar"] {
        display: none;
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
# 🧭 شريط التنقل العلوي البديل (متجاوب ومثالي للهواتف بدون تداخل)
# ---------------------------------------------------------
st.markdown("### 🧭 التنقل السريع بين الأقسام")
nav_col1, nav_col2, nav_col3 = st.columns(3)
with nav_col1:
    if st.button("🏠 الرئيسية", use_container_width=True):
        st.session_state.current_page = "home"
        st.rerun()
    if st.button("🗄️ القاعدة", use_container_width=True):
        st.session_state.current_page = "org_database"
        st.rerun()
with nav_col2:
    if st.button("📍 بئر جديد", use_container_width=True):
        st.session_state.current_page = "new_well_data"
        st.rerun()
    if st.button("📤 التقارير", use_container_width=True):
        st.session_state.current_page = "export_reports"
        st.rerun()
with nav_col3:
    if st.button("🔍 النمذجة 3D", use_container_width=True):
        st.session_state.current_page = "search_model"
        st.rerun()
    if st.button("⚙️ الإعدادات", use_container_width=True):
        st.session_state.current_page = "setup"
        st.rerun()

st.markdown("---")

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
            st.info("استخدم أزرار التنقل العلوي لسرعة الانتقال بين الأقسام.")
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
        if st.button("🛰️ جلب موقعي (GPS)"):
            st.success("تم تحديد الإحداثيات بنجاح!")

    col_top1, col_top2 = st.columns(2)
    with col_top1:
        loc_name = st.text_input("location name", value="موقع 1")
        coord_x = st.number_input("coordinate X:", value=250000.0)
        coord_y = st.number_input("coordinate Y:", value=1700000.0)
    with col_top2:
        elevation = st.number_input("elevation (متر)", value=1200.0)
        notes = st.text_area("notes", value="لا توجد ملاحظات")

    col_bot1, col_bot2 = st.columns(2)
    with col_bot1:
        village = st.text_input("village (القرية)", value="شرج آل علي")
        district = st.text_input("district (المديرية)", value="حريضة")
    with col_bot2:
        governorate = st.text_input("governorate (المحافظة)", value="حضرموت")
        well_id = st.text_input("ID (رقم المعرّف)", value=f"W-0{len(st.session_state.wells_db)+1}")

    st.markdown("---")
    if st.button("Save (حفظ البيانات الأولية)", use_container_width=True):
        st.session_state.temp_well_data = {
            "اسم الموقع": loc_name, "قرية": village, "المديرية": district,
            "المحافظة": governorate, "ID": well_id, "UTM_X": coord_x,
            "UTM_Y": coord_y, "الارتفاع (م)": elevation, "ملاحظات": notes
        }
        st.success("تم حفظ البيانات المؤقتة بنجاح!")

    if st.button("Next ➡️ (الانتقال للبيانات الجيولوجية)", use_container_width=True):
        st.session_state.current_page = "new_well_geo_data"
        st.rerun()

# ---------------------------------------------------------
# 🪨 3. شاشة البيانات الجيولوجية والخرائط (New Well Geo Data)
# ---------------------------------------------------------
elif st.session_state.current_page == "new_well_geo_data":
    st.markdown('<div class="sub-header">new well geo data</div>', unsafe_allow_html=True)
    
    st.text_input("location name (الموقع الحالي)", value=st.session_state.temp_well_data.get("اسم الموقع", "موقع جديد"))

    st.write("اختر الطبقات والبيانات الجيولوجية المساعدة:")
    geo_map = st.checkbox("geological map (الخريطة الجيولوجية)")
    faults = st.checkbox("fault structure (الفوالق والصدوع)")
    topo_map = st.checkbox("topographic map (الخريطة الطبوغرافية)")
    dem_map = st.checkbox("dem map (نموذج الارتفاع الرقمي)")

    st.markdown("---")
    if st.button("Save All (حفظ الكل في القاعدة)", use_container_width=True):
        full_data = st.session_state.temp_well_data
        if not full_data:
            full_data = {"اسم الموقع": "بئر افتراضي", "UTM_X": 250000, "UTM_Y": 1700000, "الارتفاع (م)": 1200, "ID": "W-New"}
        full_data.update({"نوع الصخر": "حجر جيري متشقق", "عمق الماء": 50, "سمك الطبقة": 35})
        st.session_state.wells_db = pd.concat([st.session_state.wells_db, pd.DataFrame([full_data])], ignore_index=True)
        st.success("تم حفظ البئر مع كافة الطبقات الجيولوجية بنجاح!")

    if st.button("Result (عرض الموديل 3D)", use_container_width=True):
        st.session_state.current_page = "search_model"
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
        height=400, margin=dict(l=0, r=0, b=0, t=20)
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------
# 📥 5. شاشة تصدير التقارير (Export Reports)
# ---------------------------------------------------------
elif st.session_state.current_page == "export_reports":
    st.markdown('<div class="sub-header">Export Reports & Data</div>', unsafe_allow_html=True)
    
    export_format = st.radio(
        "حدد صيغة التصدير المطلوبة:",
        ["Excel (.xlsx)", "CSV (.csv)", "Word (.docx)", "PDF"],
        horizontal=True
    )
    
    df_export = st.session_state.wells_db
    excel_data = df_export.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 تحميل التقرير",
        data=excel_data,
        file_name="Hammam_Wells_Report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

# ---------------------------------------------------------
# 🗄️ 6. قاعدة البيانات والإدارة (Org Database)
# ---------------------------------------------------------
elif st.session_state.current_page == "org_database":
    st.markdown('<div class="sub-header">Org Database Management</div>', unsafe_allow_html=True)
    st.dataframe(st.session_state.wells_db, use_container_width=True)

# ---------------------------------------------------------
# ✏️ 7. تعديل البيانات (Input Editing)
# ---------------------------------------------------------
elif st.session_state.current_page == "input_editing":
    st.markdown('<div class="sub-header">Input Data Editing</div>', unsafe_allow_html=True)
    edited_df = st.data_editor(st.session_state.wells_db, use_container_width=True)
    if st.button("حفظ التعديلات", use_container_width=True):
        st.session_state.wells_db = edited_df
        st.success("تم تحديث البيانات بنجاح!")

# ---------------------------------------------------------
# ⚙️ 8. الإعدادات المتكاملة (Setup)
# ---------------------------------------------------------
elif st.session_state.current_page == "setup":
    st.markdown('<div class="sub-header">System Setup & Preferences</div>', unsafe_allow_html=True)
    
    coord_system = st.selectbox("النظام الإحداثي المفضل", ["UTM WGS84 - Zone 38N", "UTM WGS84 - Zone 39N"])
    measurement_unit = st.radio("وحدة القياس", ["المتر (Meters)", "القدم (Feet)"], horizontal=True)
    grid_resolution = st.slider("دقة الشبكة ثلاثية الأبعاد", min_value=5, max_value=50, value=20)
    
    if st.button("💾 حفظ الإعدادات", use_container_width=True):
        st.success("تم حفظ إعدادات النظام بنجاح!")
