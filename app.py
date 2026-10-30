import streamlit as st
import pandas as pd
import numpy as np

# 1. إعدادات الصفحة الأساسية
st.set_page_config(
    page_title="تطبيق همم - تحليل مواقع الآبار",
    page_icon="🚰",
    layout="wide"
)

# 2. تحسينات CSS لتكون الأزرار والواجهات واسعة ومريحة جداً للهواتف
st.markdown("""
    <style>
    .main-header {
        background-color: #d9534f;
        color: white;
        padding: 15px;
        text-align: center;
        font-weight: bold;
        border-radius: 8px;
        font-size: 20px;
        margin-bottom: 20px;
    }
    .stSelectbox label, .stTextInput label, .stNumberInput label {
        font-weight: bold;
        color: #333;
    }
    </style>
""", unsafe_allow_html=True)

# عنوان التطبيق
st.markdown('<div class="main-header">Well drilling location determination</div>', unsafe_allow_html=True)

# 3. القائمة الرئيسية أصبحت في الأعلى (أسهل بكثير وأفضل للهواتف)
page = st.selectbox(
    "📌 اختر القسم المطلوب:",
    [
        "New Well Position (موقع بئر جديد)",
        "Entery Data (إدخال البيانات)",
        "Org Database (قاعدة البيانات)",
        "Input Editing (تعديل البيانات)",
        "Search (البحث)",
        "Setup (الإعدادات)"
    ]
)

st.markdown("---")

# 4. محتوى الصفحات بناءً على الاختيار
if page == "New Well Position (موقع بئر جديد)":
    st.subheader("📍 تحديد موقع بئر جديد")
    
    well_name = st.text_input("اسم البئر / الرقم التعريفي:", "Borehole-01")
    lat = st.number_input("خط العرض (Latitude):", value=15.3694, format="%.6f")
    lon = st.number_input("خط الطول (Longitude):", value=44.1910, format="%.6f")
    
    utm_zone = st.selectbox("زون UTM:", ["Zone 38N", "Zone 39N", "Zone 12N"])
    easting = st.number_input("الاحداثي الشرقي (Easting X):", value=413000.0)
    northing = st.number_input("الاحداثي الشمالي (Northing Y):", value=1700000.0)
    elevation = st.number_input("ارتفاع السطح عن مستوى البحر (m):", value=2200.0)

    if st.button("حفظ الموقع", use_container_width=True):
        st.success(f"تم تسجيل موقع البئر ({well_name}) بنجاح!")

elif page == "Entery Data (إدخال البيانات)":
    st.subheader("📝 إدخال البيانات الجيولوجية والطبقات")
    depth = st.number_input("العمق الكلي المستهدف (متر):", value=150.0)
    lithology = st.selectbox("نوع الصخور / الطبقة الجيولوجية:", ["الحجر الجيري (Limestone)", "الحجر الرملي (Sandstone)", "البازلت (Basalt)", "التربة Alluvium"])
    water_table = st.number_input("منسوب المياه الساكن (SWL):", value=45.0)
    
    if st.button("حفظ البيانات الجيولوجية", use_container_width=True):
        st.success("تم إضافات البيانات بنجاح إلى السجل.")

elif page == "Org Database (قاعدة البيانات)":
    st.subheader("🗄️ قاعدة البيانات المرفوقة")
    sample_data = pd.DataFrame({
        "Well Name": ["BH-01", "BH-02", "BH-03"],
        "Easting": [413000, 414200, 412800],
        "Depth (m)": [180, 210, 150],
        "SWL (m)": [42.5, 55.0, 38.0]
    })
    st.dataframe(sample_data, use_container_width=True)

elif page == "Setup (الإعدادات)":
    st.subheader("⚙️ إعدادات البرنامج والشبكات")
    unit = st.radio("وحدات القياس:", ["متر (Meters)", "قدم (Feet)"])
    grid_method = st.selectbox("خوارزمية الاستكمال المكانية (Interpolation):", ["Kriging", "Inverse Distance Weighting (IDW)", "Nearest Neighbor"])
    st.write("حالة خوارزمية الشبكة الحالية:", grid_method)

else:
    st.subheader(f"قسم {page}")
    st.info("جاري العمل على استكمال خصائص هذا القسم.")
