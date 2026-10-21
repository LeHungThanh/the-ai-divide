"""The AI Divide: six-page policy dashboard."""
import streamlit as st
from src.ui import inject_style

st.set_page_config(page_title="The AI Divide", page_icon="◈", layout="wide",
                   initial_sidebar_state="expanded")
inject_style()
st.sidebar.markdown("### The AI Divide")
st.sidebar.caption("Evidence for EU policymakers · 2021–2025")
navigation = st.navigation([
    st.Page("pages/1_Overview.py", title="Overview", icon="🏛️", default=True),
    st.Page("pages/2_Country_Divide.py", title="Country Divide", icon="🌍"),
    st.Page("pages/3_Company_Size.py", title="Company Size", icon="🏢"),
    st.Page("pages/4_Industry_Divide.py", title="Industry Divide", icon="📊"),
    st.Page("pages/5_Adoption_Barriers.py", title="Adoption Barriers", icon="🔎"),
    st.Page("pages/6_Conclusion_and_Sources.py", title="Conclusion & Sources", icon="📚"),
])
navigation.run()
