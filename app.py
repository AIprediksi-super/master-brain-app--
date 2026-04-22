import streamlit as st
import numpy as np
import easyocr
from PIL import Image
import streamlit.components.v1 as components
from collections import Counter

# 1. Inisialisasi AI OCR
@st.cache_resource
def load_ocr():
    return easyocr.Reader(['en', 'id'])

reader = load_ocr()

# 2. Pengaturan Halaman
st.set_page_config(page_title="Master Brain v14: Hitam Neon", layout="wide")

if 'global_history' not in st.session_state:
    st.session_state.global_history = []

# --- SIDEBAR TEMA ---
st.sidebar.header("🎨 Tampilan & Data")
tema = st.sidebar.selectbox("Pilih Warna Tema:", 
    ["Gelap (Neon Green)", "Biru Langit Cerah", "Hijau Cerah", "Ungu Neon", "Merah Muda (Pink)"])

themes = {
    "Gelap (Neon Green)": {"bg": "#0E1117", "txt": "#00FF00", "akurat": "#006400", "mid1": "#8B8000", "mid2": "#4B5320", "kontra": "#8B0000", "btn": "#00FF00", "btn_txt": "black"},
    "Biru Langit Cerah": {"bg": "#E0F7FA", "txt": "#01579B", "akurat": "#0288D1", "mid1": "#FBC02D", "mid2": "#4FC3F7", "kontra": "#D32F2F", "btn": "#0288D1", "btn_txt": "white"},
    "Hijau Cerah": {"bg": "#F1F8E9", "txt": "#33691E", "akurat": "#388E3C", "mid1": "#FBC02D", "mid2": "#8BC34A", "kontra": "#D32F2F", "btn": "#558B2F", "btn_txt": "white"},
    "Ungu Neon": {"bg": "#2D004D", "txt": "#BF00FF", "akurat": "#7B1FA2", "mid1": "#9C27B0", "mid2": "#E040FB", "kontra": "#4A148C", "btn": "#BF00FF", "btn_txt": "black"},
    "Merah Muda (Pink)": {"bg": "#FCE4EC", "txt": "#880E4F", "akurat": "#C2185B", "mid1": "#FBC02D", "mid2": "#F06292", "kontra": "#AD1457", "btn": "#D81B60", "btn_txt": "white"}
}
t = themes[tema]

st.markdown(f"""
    <style>
    .stApp {{ background-color: {t['bg']}; color: {t['txt']}; transition: all 0.6s ease-in-out; }}
    div[data-baseweb="textarea"] {{ border: 3px solid {t['txt']} !important; background-color: white !important; border-radius: 12px; }}
    textarea {{ color: black !important; font-size: 22px !important; font-family: 'Consolas', monospace; }}
    .stButton>button {{ background-color: {t['btn']} !important; color: {t['btn_txt']} !important; font-size: 20px !important; font-weight: bold; border-radius: 12px; width: 100%; height: 3.5em; }}
    
    .predict-table {{ width: 100%; border-collapse: collapse; margin-bottom: 30px; }}
    .predict-table th {{ border: 2px solid {t['txt']}; padding: 10px; background-color: rgba(0,0,0,0.5); color: {t['txt']}; font-size: 14px; }}
    .predict-table td {{ 
        border: 1px solid rgba(255,255,255,0.2); 
        padding: 8px; 
        text-align: center; 
        font-size: 28px; 
        font-weight: 900; 
        color: white; 
        /* EFEK HITAM NEON GLOW */
        text-shadow: 0 0 5px #000, 0 0 10px #000, -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, 1px 1px 0 #000;
    }}
    .bg-akurat {{ background-color: {t['akurat']} !important; }}
    .bg-mid1 {{ background-color: {t['mid1']} !important; }}
    .bg-mid2 {{ background-color: {t['mid2']} !important; }}
    .bg-kontra {{ background-color: {t['kontra']} !important; }}
    
    h1, h2, h3 {{ color: {t['txt']} !important; text-transform: uppercase; letter-spacing: 1px; }}
    </style>
    """, unsafe_allow_html=True)

st.title("🧠 MASTER BRAIN V14: HITAM NEON")

# --- INPUT ---
st.sidebar.markdown("---")
input_mode = st.sidebar.selectbox("Metode Input:", ["Input Manual / Paste", "Upload Screenshot"])
if st.sidebar.button("🗑️ RESET DATA"):
    st.session_state.global_history = []
    st.rerun()

if input_mode == "Input Manual / Paste":
    manual_input = st.text_area("Tempel Histori:", height=200)
    if st.button("🚀 ANALISA HITAM NEON"):
        if manual_input:
            data = manual_input.replace(',', ' ').replace('\n', ' ').upper().split()
            st.session_state.global_history.extend(data)
else:
    up_file = st.file_uploader("Upload Gambar:", type=["png", "jpg", "jpeg"])
    if up_file and st.button("🚀 SCAN FOTO"):
        img = Image.open(up_file)
        results = reader.readtext(np.array(img), detail=0)
        data = [str(x).upper() for x in results if len(x) >= 2]
        st.session_state.global_history.extend(data)

# --- MESIN ANALISA V14 ---
def analyze_v14(data):
    col_data = [[], [], [], []]
    for item in data:
        chars = [c for c in item if c.isalnum()]
        for i in range(min(4, len(chars))):
            col_data[i].append(chars[i])
    
    final_results = {}
    for i in range(4):
        curr = col_data[i]
        if not curr: continue
        possible_chars = sorted(list(set(curr)))
        last_c = curr[-1]
        freq = Counter(curr)
        trans = Counter(zip(curr, curr[1:]))
        
        scores = {}
        for c in possible_chars:
            s_markov = (trans.get((last_c, c), 0) / (curr.count(last_c) or 1)) * 0.50
            s_freq = (freq.get(c, 0) / len(curr)) * 0.30
            s_moment = (curr[-10:].count(c) / 10) * 0.20
            scores[c] = s_markov + s_freq + s_moment
            
        sorted_all = [x[0] for x in sorted(scores.items(), key=lambda x: x[1], reverse=True)]
        
        def get_p(res_list, start, end):
            extracted = res_list[start:end]
            while len(extracted) < (end-start): extracted.append("-")
            return extracted

        final_results[f"KOLOM {i+1}"] = {
            "akurat": get_p(sorted_all, 0, 7),
            "mid1": get_p(sorted_all, 1, 8),
            "mid2": get_p(sorted_all, 2, 9),
            "kontra": get_p(sorted_all[::-1], 0, 8)
        }
    return final_results

# --- OUTPUT ---
history = st.session_state.global_history
if history:
    res = analyze_v14(history)
    if res:
        def draw_table(title, key, css):
            rows = 8 if key == "kontra" else 7
            html = f"<h3>{title}</h3><table class='predict-table'><tr><th>RANK</th>"
            for k in range(1, 5): html += f"<th>KOL {k}</th>"
            html += "</tr>"
            for r in range(rows):
                html += f"<tr><td style='font-size:12px; background:rgba(0,0,0,0.5);'>#{r+1}</td>"
                for c in range(1, 5):
                    val = res[f"KOLOM {c}"][key][r] if f"KOLOM {c}" in res else "-"
                    html += f"<td class='{css}'>{val}</td>"
                html += "</tr>"
            html += "</table>"
            return html

        st.markdown(draw_table("🟢 AKURAT (1-7)", "akurat", "bg-akurat"), unsafe_allow_html=True)
        st.markdown(draw_table("🟡 TENGAH (01) (1-7)", "mid1", "bg-mid1"), unsafe_allow_html=True)
        st.markdown(draw_table("🟠 TENGAH (02) (1-7)", "mid2", "bg-mid2"), unsafe_allow_html=True)
        st.markdown(draw_table("🔴 KONTRA PREDIKSI (1-8)", "kontra", "bg-kontra"), unsafe_allow_html=True)

        st.markdown("---")
        components.html(f"""<button onclick="navigator.share({{title:'Master Brain v14', text:'Result: {history[-1]}'}})" style="width:100%; background-color:{t['btn']}; color:{t['btn_txt']}; padding:15px; border:none; border-radius:12px; font-size:20px; font-weight:bold; cursor:pointer;">📲 BAGIKAN HASIL</button>""", height=100)
else:
    st.info("💡 Masukkan histori untuk menjalankan Analisa Hitam Neon 1-7 & 1-8.")
