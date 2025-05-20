# 🧬 Experimental Methods Mapper

This Streamlit-based app helps researchers and students extract experimental methods, tools, datasets, and evaluation metrics from scientific literature. It supports both topic-based search via Semantic Scholar and PDF uploads. Outputs are visualized as tables, charts, and a dynamic knowledge graph.

---

## 🚀 Features

- 🔍 **Search by Research Topic** (via Semantic Scholar API)
- 📄 **Upload PDFs** to extract methods from full-text
- 🤖 **Auto-generated literature summary**
- 📊 **Visualize top methods, tools, domains**
- 🧠 **Interactive Knowledge Graph** (PyVis + NetworkX)
- 💾 **Save and Load** query results (with history)
- ⏪ **Search history sidebar** (like ChatGPT)

---

## 📸 Screenshots

| Search Input | Table + Graph | Summary View |
|--------------|---------------|---------------|
| ![search](docs/search.png) | ![graph](docs/graph.png) | ![summary](docs/summary.png) |

---

## 🧱 Tech Stack

- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [Plotly](https://plotly.com/python/)
- [NetworkX](https://networkx.org/)
- [PyVis](https://pyvis.readthedocs.io/)
- [PyMuPDF](https://pymupdf.readthedocs.io/) for PDF parsing
- [Ollama](https://ollama.com/) + LLaMA 3 for local LLM extraction
- [Semantic Scholar API](https://api.semanticscholar.org/)

---

## 📂 Project Structure

```
method_mapper/
│
├── app.py                   # Streamlit app
├── generator.py             # LLaMA prompt logic + PDF/Semantic Scholar
├── saved_runs/              # JSONs of saved queries
├── requirements.txt
└── README.md
```

---

## 🛠 Installation

### 1. Clone the repository
```bash
git clone https://github.com/your-username/method_mapper.git
cd method_mapper
```

### 2. Set up environment
```bash
pip install -r requirements.txt
```

### 3. Run Streamlit app
```bash
streamlit run app.py
```

---

## 🔧 Requirements

Your `requirements.txt`:

```txt
streamlit
pandas
plotly
networkx
pyvis
PyMuPDF
```

---

## 📤 Usage

### Option 1: Search by Topic
- Enter a research goal (e.g. *"diabetic retinopathy detection using deep learning"*)
- App fetches abstracts via Semantic Scholar
- LLaMA 3 parses and outputs a structured table

### Option 2: Upload PDF
- Upload a research paper in PDF
- App extracts text and runs prompt on LLaMA 3
- Outputs methods, tools, datasets, and metrics

---

## 💾 Save & Load

- Save extracted data with a custom name
- Reload anytime from the sidebar
- Auto-keeps search history in session like ChatGPT

---

## 🧠 Example Prompts

- *Alzheimer’s detection using MRI*
- *Lung cancer diagnosis with CT*
- *Skin lesion classification with CNN*
- *COVID-19 PCR classification*
- *Retinal image segmentation using U-Net*

---

## 📈 Visual Output

- Top methods bar chart
- Tool distribution pie chart
- Domain breakdown
- Auto-generated natural language summary
- PyVis-powered interactive knowledge graph

---

## 🧠 Future Enhancements

- GPT-powered summary via OpenAI or Ollama API
- Export as PDF report
- Add citations + source tracing
- Expand dataset extraction
- Add bulk PDF support

---

## 👤 Author

Built by [Jaimin Shimpi](https://github.com/jshimpi02)

---

## 📜 License

MIT License – feel free to use and adapt.
