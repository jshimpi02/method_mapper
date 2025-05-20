# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
from generator import extract_methods_table, extract_methods_from_pdf
import tempfile
import os
import json

SAVE_DIR = "saved_runs"
os.makedirs(SAVE_DIR, exist_ok=True)

st.set_page_config(page_title="Experimental Methods Mapper", page_icon="🧬", layout="wide")

st.markdown("<h1 style='font-family: cursive;'>🧬 Experimental Methods Mapper</h1>", unsafe_allow_html=True)

with st.expander("ℹ️ Example Prompts (Click to hide)", expanded=False):
    st.markdown("""
    - Alzheimer's detection using MRI scans  
    - Lung cancer diagnosis with CT imaging  
    - Diabetic retinopathy detection using fundus images  
    - COVID-19 variant classification using PCR  
    - Skin lesion detection with deep learning
    """)

st.markdown("""
Enter your research goal or upload a PDF to extract experimental methods, tools, datasets, and metrics using LLaMA 3.
""")

# Utility functions
def add_node_with_type(net, node, node_type):
    color_map = {
        'Method': 'lightblue',
        'Tool': 'lightgreen',
        'Dataset': 'orange'
    }
    net.add_node(node, label=node, title=node_type, color=color_map.get(node_type, 'gray'))

def list_saved_runs():
    return [f[:-5] for f in os.listdir(SAVE_DIR) if f.endswith(".json")]

def load_saved_run(name):
    with open(os.path.join(SAVE_DIR, name + ".json"), 'r') as f:
        return pd.DataFrame(json.load(f))

def save_current_run(name, df):
    with open(os.path.join(SAVE_DIR, name + ".json"), 'w') as f:
        json.dump(df.to_dict(orient="records"), f)

# Inputs
col_input, col_saved = st.columns([3, 1])
with col_input:
    tab1, tab2 = st.tabs(["🔍 Search by Topic", "📄 Upload PDF"])
    methods_df = pd.DataFrame()
    st.session_state.setdefault("history", [])
    with tab1:
        goal = st.text_input("🎯 Research Goal", placeholder="e.g., Alzheimer's progression using MRI", key="research_goal", autocomplete="on")
        if st.button("🔍 Search") and goal:
            st.session_state.history.append(goal)
            with st.spinner("Searching Semantic Scholar and extracting methods..."):
                methods_df = extract_methods_table(goal)
    with tab2:
        uploaded_file = st.file_uploader("📄 Upload a Research Paper (PDF)", type=["pdf"])
        if uploaded_file:
            with st.spinner("Extracting methods from uploaded PDF..."):
                methods_df = extract_methods_from_pdf(uploaded_file)

with col_saved:
    st.markdown("### 💾 Load Previous Run")
    saved_files = list_saved_runs()
    selected_file = st.selectbox("Select a saved run:", [""] + saved_files, key="load_run")
    if selected_file:
        try:
            methods_df = load_saved_run(selected_file)
            st.success(f"Loaded run: {selected_file}")
        except FileNotFoundError:
            st.error(f"Saved run '{selected_file}' not found. Please refresh or save again.")

    st.markdown("### 🧠 Search History")
    for idx, past_query in enumerate(reversed(st.session_state.get("history", []))):
        if st.button(past_query, key=f"history_{idx}"):
            with st.spinner("Reloading query and extracting methods..."):
                methods_df = extract_methods_table(past_query)
                st.success(f"Re-ran search: {past_query}")


if not methods_df.empty:
    st.success("✅ Extracted Methods")

    st.markdown("---")
    save_name = st.text_input("💾 Save this run as:", placeholder="e.g., alzheimers_mri", key="save_name")
    if st.button("Save Run") and save_name:
        save_current_run(save_name, methods_df)
        st.success(f"Saved run as '{save_name}'")

    col_left, col_right = st.columns([3, 2])

    with col_left:
        with st.expander("📝 Auto-Generated Literature Summary", expanded=True):
            if 'Method' in methods_df.columns:
                summary = "This study explores the following methods: "
                methods = methods_df['Method'].dropna().unique().tolist()
                datasets = methods_df['Dataset'].dropna().unique().tolist()
                tools = methods_df['Tools'].dropna().unique().tolist() if 'Tools' in methods_df.columns else []

                if methods:
                    summary += ", ".join(methods) + ". "
                if datasets:
                    summary += f"Datasets include: {', '.join(datasets)}. "
                if tools:
                    summary += f"Tools and software mentioned: {', '.join(tools)}. "
                else:
                    summary += "No specific tools were mentioned."

                st.markdown(summary)

                if st.button("🧠 Regenerate Summary using GPT", key="regen_summary"):
                    prompt = f"Generate a concise research summary using the following methods: {methods}. Datasets: {datasets}. Tools: {tools}."
                    st.info("(Simulated GPT Response)")
                    st.markdown(f"🧠 *{prompt}*")
            else:
                st.info("Not enough method information to generate summary.")

        with st.expander("📊 View Extracted Table", expanded=True):
            st.dataframe(methods_df, use_container_width=True)
            csv = methods_df.to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ Download CSV", csv, "methods_table.csv")

    with col_right:
        with st.expander("🧠 Knowledge Graph View", expanded=True):
            G = nx.Graph()
            for _, row in methods_df.iterrows():
                method = row.get('Method')
                tool = row.get('Tools')
                dataset = row.get('Dataset')
                if method and tool:
                    G.add_edge(method, tool, label="uses")
                if method and dataset:
                    G.add_edge(method, dataset, label="applied on")

            net = Network(height='400px', width='100%', notebook=False)
            net.show_buttons(filter_=[])
            net.set_options("""
            var options = {
              "physics": {
                "enabled": false
              }
            }
            """)

            for _, row in methods_df.iterrows():
                method = row.get('Method')
                tool = row.get('Tools')
                dataset = row.get('Dataset')
                if method:
                    add_node_with_type(net, method, "Method")
                if tool:
                    add_node_with_type(net, tool, "Tool")
                if dataset:
                    add_node_with_type(net, dataset, "Dataset")
                if method and tool:
                    net.add_edge(method, tool)
                if method and dataset:
                    net.add_edge(method, dataset)

            tmp_dir = tempfile.mkdtemp()
            html_path = os.path.join(tmp_dir, "graph.html")
            net.save_graph(html_path)
            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            components.html(html_content, height=400, width=500, scrolling=True)

            with open(html_path, 'rb') as f:
                st.download_button("⬇️ Download Graph as HTML", f.read(), file_name="knowledge_graph.html")
