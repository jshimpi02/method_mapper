# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
from generator import extract_methods_table, extract_methods_from_pdf

st.set_page_config(page_title="Experimental Methods Mapper", page_icon="🧬", layout="wide")

# Sidebar with example prompts
st.sidebar.title("🧪 Example Prompts")
st.sidebar.markdown("""
- Alzheimer's detection using MRI scans
- Lung cancer diagnosis with CT imaging
- Diabetic retinopathy detection using fundus images
- COVID-19 variant classification using PCR
- Skin lesion detection with deep learning
""")

st.markdown("<h1 style='font-family: cursive;'>🧬 Experimental Methods Mapper</h1>", unsafe_allow_html=True)
st.markdown("""
Enter your research goal or topic below, or upload a research paper PDF. The tool will extract experimental methods, tools, datasets, and metrics using a local LLM (LLaMA 3 via Ollama).
""")

# Tabs: Search by text or PDF upload
tab1, tab2 = st.tabs(["🔍 Search by Topic", "📄 Upload PDF"])

with tab1:
    goal = st.text_input(
        "🎯 Research Goal",
        placeholder="e.g., Alzheimer's progression using MRI",
        key="research_goal",
        autocomplete="on"
    )
    search_clicked = st.button("🔍 Search")

    if search_clicked and goal:
        with st.spinner("Searching Semantic Scholar and extracting methods via LLaMA 3..."):
            methods_df = extract_methods_table(goal)

with tab2:
    uploaded_file = st.file_uploader("📄 Upload a Research Paper (PDF)", type=["pdf"])
    if uploaded_file:
        with st.spinner("Extracting methods from uploaded PDF using LLaMA 3..."):
            methods_df = extract_methods_from_pdf(uploaded_file)

if 'methods_df' in locals() and not methods_df.empty:
    st.success("✅ Extracted Methods")

    with st.expander("📊 View Extracted Table", expanded=True):
        st.dataframe(methods_df, use_container_width=True)
        csv = methods_df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download CSV", csv, "methods_table.csv")

    with st.expander("📈 Visualize Extracted Insights", expanded=False):
        col1, col2 = st.columns(2)

        with col1:
            if 'Method' in methods_df.columns:
                method_counts = methods_df['Method'].value_counts().reset_index()
                method_counts.columns = ['Method', 'Count']
                fig1 = px.bar(method_counts, x='Method', y='Count', title='Top Methods')
                st.plotly_chart(fig1, use_container_width=True)
            else:
                st.info("No 'Method' column found in the extracted data.")

        with col2:
            if 'Tools' in methods_df.columns:
                tool_counts = methods_df['Tools'].value_counts().reset_index()
                tool_counts.columns = ['Tool', 'Count']
                fig2 = px.pie(tool_counts, names='Tool', values='Count', title='Tool Distribution')
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.info("No 'Tools' column found in the extracted data.")

        if 'Domain' in methods_df.columns:
            domain_counts = methods_df['Domain'].value_counts().reset_index()
            domain_counts.columns = ['Domain', 'Count']
            fig3 = px.bar(domain_counts, x='Domain', y='Count', title='Domain Breakdown')
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.info("No 'Domain' column found in the extracted data.")

elif 'methods_df' in locals():
    st.warning("No methods found or extraction failed.")
