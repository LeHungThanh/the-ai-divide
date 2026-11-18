"""The AI Divide: six-page policy dashboard."""
import streamlit as st
from src.ui import inject_style

st.set_page_config(page_title="The AI Divide", page_icon="◈", layout="wide",
                   initial_sidebar_state="expanded")
navigation = st.navigation([
    st.Page("pages/1_Overview.py", title="Overview", icon="🏛️", default=True),
    st.Page("pages/2_Country_Divide.py", title="Country Divide", icon="🌍"),
    st.Page("pages/3_Company_Size.py", title="Company Size", icon="🏢"),
    st.Page("pages/4_Industry_Divide.py", title="Industry Divide", icon="📊"),
    st.Page("pages/5_Adoption_Barriers.py", title="Adoption Barriers", icon="🔎"),
    st.Page("pages/6_Conclusion_and_Sources.py", title="Conclusion & Sources", icon="📚"),
])
page_key = navigation.url_path
st.session_state["_motion_page_entry"] = st.session_state.get("_motion_last_page") != page_key
st.session_state["_motion_last_page"] = page_key
inject_style()
st.sidebar.markdown(
    '<div class="sidebar-meta"><strong>THE AI DIVIDE</strong><br>'
    'EU enterprise evidence<br><span>2021 · 2023 · 2024 · 2025</span></div>',
    unsafe_allow_html=True,
)
navigation.run()
