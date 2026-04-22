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

# 2. Pengaturan Halaman & Tema
st.set_page_config(page_title="Master Brain v12.1: Table Edition", layout="wide")

if 'global_history' not in st.session_state:
    st.session_state.global_history = []

# --- SIDEBAR TEMA ---
st.sidebar.header("🎨 Tampilan & Data")
tema = st.sidebar.selectbox("Pilih Warna Tema:", 
    ["Gelap (Neon Green)", "Biru Langit Cerah", "Hijau Cerah", "Ungu Neon", "Merah Muda (Pink)"])

themes = {
    "Gelap (Neon Green)": {"bg": "#0E1117", "txt": "#00FF00", "akurat": "#004400", "mid": "#444400", "kontra": "#440000", "btn": "#00FF00", "btn_txt": "black"},
    "Biru Langit Cerah": {"bg": "#E0F7FA", "txt": "#01579B", "akurat": "#B3E5FC", "mid": "#FFF9C4", "kontra": "#FFEBEE", "btn": "#0288D1", "btn_txt": "white"},
    "Hijau Cerah": {"bg": "#F1F8E9", "txt": "#33691E", "akurat": "#C8E6C9", "mid": "#FFF9C4", "kontra": "#FFCCBC", "btn": "#558B2F", "btn_txt": "white"},
    "Ungu Neon": {"bg": "#2D004D", "txt": "#BF00FF", "akurat": "#4B0082", "mid": "#6A1B9A", "kontra": "#311B92", "btn": "#BF00FF", "btn_txt": "black"},
    "Merah Muda (Pink)": {"bg": "#FCE4EC", "txt": "#880E4F", "akurat": "#F8BBD0", "mid": "#FFF9C4", "kontra": "#FFCCBC", "btn": "#D81B60", "btn_txt": "white"}
}
t = themes[tema]

st.markdown(f"""
    <style>
    .stApp {{ background-color: {t['bg']}; color: {t['txt']}; transition: all 0.6s ease-in-out; }}
    div[data-baseweb="textarea"] {{ border: 3px solid {t['txt']} !important; background-color: white !important; border-radius: 12px; }}
    textarea {{ color: black !important; font-size: 22px !important; font-family: 'Consolas', monospace; }}
    .stButton>button {{ background-color: {t['btn']} !important; color: {t['btn_txt']} !important; font-size: 20px !important; font-weight: bold; border-radius: 12px; width: 100%; height: 3.5em; }}
    
    /* Style Tabel Prediksi */
    .predict-table {{
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 20px;
        color: {t['txt']};
        font-family: Arial, sans-serif;
    }}
    .predict-table th {{
        border: 2px solid {t['txt']};
        padding: 10px;
        background-color: rgba(255,255,255,0.1);
        font-size: 18px;
    }}
    .predict-table td {{
        border: 1px solid {t['txt']};
        padding: 12px;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
    }}
    .bg-akurat {{ background-color: {t['akurat']} !important; color: white !important; }}
    .bg-mid {{ background-color: {t['mid']} !important; color: white !important; }}
    .bg-kontra {{ background-color: {t['kontra']} !important; color: white !important; }}
    
    h1, h2, h3, p {{ color: {t['txt']} !important; }}
    </style>
    """, unsafe_allow_html=True)

st.title("🧠 Master Brain v12.1: Table Prediction Mode")

# --- PANEL INPUT ---
st.sidebar.markdown("---")
input_mode = st.sidebar.selectbox("Metode Input:", ["Input Manual / Paste", "Upload Screenshot"])
if st.sidebar.button("🗑️ HAPUS DATA"):
    st.session_state.global_history = []
    st.rerun()

if input_mode == "Input Manual / Paste":
    manual_input = st.text_area("Tempel Data (0-9, A, B):", height=200)
    if st.button("🚀 JALANKAN ANALISA TABEL"):
        if manual_input:
            data = manual_input.replace(',', ' ').replace('\n', ' ').upper().split()
            st.session_state.global_history.extend(data)
else:
    up_file = st.file_uploader("Upload Foto:", type=["png", "jpg", "jpeg"])
    if up_file and st.button("🚀 SCAN & ANALISA"):
        img = Image.open(up_file)
        results = reader.readtext(np.array(img), detail=0)
        data = [str(x).upper() for x in results if len(x) >= 2]
        st.session_state.global_history.extend(data)

# --- MESIN ANALISA ---
def analyze_v12_table(data):
    col_data = [[], [], [], []]
    for item in data:
        chars = [c for c in item if c.isdigit() or c in ['A', 'B']]
        for i in range(min(4, len(chars))):
            col_data[i].append(chars[i])
    
    final_results = {}
    valid_chars = [str(d) for d in range(10)] + ['A', 'B']
    
    for i in range(4):
        curr = col_data[i]
        if not curr: continue
        last_c = curr[-1]
        trans = Counter(zip(curr, curr[1:]))
        freq = Counter(curr)
        
        scores = {}
        for c in valid_chars:
            s_pola = (trans.get((last_c, c), 0) / (curr.count(last_c) or 1)) * 0.65
            s_freq = (freq.get(c, 0) / len(curr)) * 0.35
            scores[c] = s_pola + s_freq
            
        sorted_all = [x[0] for x in sorted(scores.items(), key=lambda x: x[1], reverse=True)]
        
        final_results[f"KOLOM {i+1}"] = {
            "akurat": sorted_all[:5],
            "tengah": sorted_all[len(sorted_all)//2-2 : len(sorted_all)//2+3],
            "kontra": sorted_all[-8:] # Lawan arus 1-8 sesuai permintaan sebelumnya
        }
    return final_results

# --- TAMPILAN OUTPUT TABEL ---
history = st.session_state.global_history
if history:
    st.write(f"📊 Menampilkan Tabel Prediksi dari {len(history)} data histori.")
    res = analyze_v12_table(history)
    
    if res:
        # FUNGSI MEMBUAT TABEL HTML
        def create_table_html(title, zone_key, css_class):
            html = f"<h3>{title}</h3><table class='predict-table'><tr>"
            for k in range(1, 5): html += f"<th>KOLOM {k}</th>"
            html += "</tr>"
            
            # Mendapatkan jumlah baris (5 untuk akurat/mid, 8 untuk kontra)
            num_rows = len(res["KOLOM 1"][zone_key])
            
            for row in range(num_rows):
                html += "<tr>"
                for col in range(1, 5):
                    val = res[f"KOLOM {col}"][zone_key][row] if f"KOLOM {col}" in res else "-"
                    html += f"<td class='{css_class}'>{val}</td>"
                html += "</tr>"
            html += "</table>"
            return html

        st.markdown(create_table_html("🟢 TABEL PREDIKSI AKURAT (1-5)", "akurat", "bg-akurat"), unsafe_allow_html=True)
        st.markdown(create_table_html("🟡 TABEL PREDIKSI TENGAH (1-5)", "tengah", "bg-mid"), unsafe_allow_html=True)
        st.markdown(create_table_html("🔴 TABEL KONTRA PREDIKSI (1-8)", "kontra", "bg-kontra"), unsafe_allow_html=True)

        # Share
        st.markdown("---")
        share_btn = f"""<button onclick="navigator.share({{title:'Tabel Master Brain', text:'Hasil Prediksi Tabel Master Brain Aktif'}})" style="width:100%; background-color:{t['btn']}; color:{t['btn_txt']}; padding:15px; border:none; border-radius:12px; font-size:20px; font-weight:bold; cursor:pointer;">📲 BAGIKAN TABEL HASIL</button>"""
        components.html(share_btn, height=100)
else:
    st.info("💡 Masukkan data untuk melihat tampilan Tabel Prediksi Warna.")
