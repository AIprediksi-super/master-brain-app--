import streamlit as st
import numpy as np
import easyocr
from PIL import Image
import streamlit.components.v1 as components
from collections import Counter

@st.cache_resource
def load_ocr():
    return easyocr.Reader(['en', 'id'])

reader = load_ocr()

st.set_page_config(page_title="Master Brain v13.1: Adaptive Logic", layout="wide")

if 'global_history' not in st.session_state:
    st.session_state.global_history = []

# --- SIDEBAR TEMA ---
st.sidebar.header("🎨 Tampilan & Data")
tema = st.sidebar.selectbox("Pilih Warna Tema:", 
    ["Gelap (Neon Green)", "Biru Langit Cerah", "Hijau Cerah", "Ungu Neon", "Merah Muda (Pink)"])

themes = {
    "Gelap (Neon Green)": {"bg": "#0E1117", "txt": "#00FF00", "akurat": "#006400", "mid": "#8B8000", "kontra": "#8B0000", "btn": "#00FF00", "btn_txt": "black"},
    "Biru Langit Cerah": {"bg": "#E0F7FA", "txt": "#01579B", "akurat": "#0288D1", "mid": "#FBC02D", "kontra": "#D32F2F", "btn": "#0288D1", "btn_txt": "white"},
    "Hijau Cerah": {"bg": "#F1F8E9", "txt": "#33691E", "akurat": "#388E3C", "mid": "#FBC02D", "kontra": "#D32F2F", "btn": "#558B2F", "btn_txt": "white"},
    "Ungu Neon": {"bg": "#2D004D", "txt": "#BF00FF", "akurat": "#7B1FA2", "mid": "#9C27B0", "kontra": "#4A148C", "btn": "#BF00FF", "btn_txt": "black"},
    "Merah Muda (Pink)": {"bg": "#FCE4EC", "txt": "#880E4F", "akurat": "#C2185B", "mid": "#FBC02D", "kontra": "#AD1457", "btn": "#D81B60", "btn_txt": "white"}
}
t = themes[tema]

st.markdown(f"""
    <style>
    .stApp {{ background-color: {t['bg']}; color: {t['txt']}; transition: all 0.6s ease-in-out; }}
    div[data-baseweb="textarea"] {{ border: 3px solid {t['txt']} !important; background-color: white !important; border-radius: 12px; }}
    textarea {{ color: black !important; font-size: 22px !important; font-family: 'Consolas', monospace; }}
    .stButton>button {{ background-color: {t['btn']} !important; color: {t['btn_txt']} !important; font-size: 20px !important; font-weight: bold; border-radius: 12px; width: 100%; height: 3.5em; }}
    .predict-table {{ width: 100%; border-collapse: collapse; margin-bottom: 30px; }}
    .predict-table th {{ border: 2px solid {t['txt']}; padding: 10px; background-color: rgba(0,0,0,0.4); color: {t['txt']}; }}
    .predict-table td {{ border: 1px solid rgba(255,255,255,0.2); padding: 8px; text-align: center; font-size: 28px; font-weight: 900; color: white; text-shadow: -1.5px -1.5px 0 #000, 1.5px -1.5px 0 #000, -1.5px 1.5px 0 #000, 1.5px 1.5px 0 #000; }}
    .bg-akurat {{ background-color: {t['akurat']} !important; }}
    .bg-mid {{ background-color: {t['mid']} !important; }}
    .bg-kontra {{ background-color: {t['kontra']} !important; }}
    </style>
    """, unsafe_allow_html=True)

st.title("🧠 MASTER BRAIN V13.1: ADAPTIVE LOGIC")

# --- INPUT ---
st.sidebar.markdown("---")
input_mode = st.sidebar.selectbox("Metode Input:", ["Input Manual / Paste", "Upload Screenshot"])
if st.sidebar.button("🗑️ RESET DATA"):
    st.session_state.global_history = []
    st.rerun()

if input_mode == "Input Manual / Paste":
    manual_input = st.text_area("Paste Data Histori:", height=200)
    if st.button("🚀 ANALISA ADAPTIF"):
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

# --- MESIN ANALISA ADAPTIF ---
def analyze_adaptive(data):
    col_data = [[], [], [], []]
    for item in data:
        chars = [c for c in item if c.isalnum()]
        for i in range(min(4, len(chars))):
            col_data[i].append(chars[i])
    
    final_results = {}
    
    for i in range(4):
        curr = col_data[i]
        if not curr: continue
        
        # DETEKSI SUMBER: Hanya karakter yang pernah muncul di data yang akan diprediksi
        possible_chars = sorted(list(set(curr))) 
        
        last_c = curr[-1]
        freq = Counter(curr)
        trans = Counter(zip(curr, curr[1:]))
        
        scores = {}
        for c in possible_chars:
            # Skor Markov + Tren + Momentum
            s_markov = (trans.get((last_c, c), 0) / (curr.count(last_c) or 1)) * 0.50
            s_freq = (freq.get(c, 0) / len(curr)) * 0.30
            recent = curr[-10:]
            s_moment = (recent.count(c) / 10) * 0.20
            
            scores[c] = s_markov + s_freq + s_moment
            
        sorted_all = [x for x in sorted(scores.items(), key=lambda x: x, reverse=True)]
        
        # Menyesuaikan hasil agar tidak error jika jumlah karakter unik sedikit
        def pad_results(res_list, target):
            while len(res_list) < target:
                res_list.append(("-", 0))
            return res_list

        final_results[f"KOLOM {i+1}"] = {
            "akurat": pad_results(sorted_all[:7], 7),
            "tengah": pad_results(sorted_all[2:9], 7),
            "kontra": pad_results(sorted_all[-8:][::-1], 8)
        }
    return final_results

# --- OUTPUT ---
history = st.session_state.global_history
if history:
    res = analyze_adaptive(history)
    if res:
        def draw_table(title, zone_key, css_class, rows):
            html = f"<h3>{title}</h3><table class='predict-table'><tr><th>RANK</th>"
            for k in range(1, 5): html += f"<th>KOL {k}</th>"
            html += "</tr>"
            for row in range(rows):
                html += f"<tr><td style='font-size:12px; background:rgba(0,0,0,0.5);'>#{row+1}</td>"
                for col in range(1, 5):
                    k_name = f"KOLOM {col}"
                    val = res[k_name][zone_key][row][0] if k_name in res else "-"
                    html += f"<td class='{css_class}'>{val}</td>"
                html += "</tr>"
            html += "</table>"
            return html

        st.markdown(draw_table("🟢 AKURAT (1-7)", "akurat", "bg-akurat", 7), unsafe_allow_html=True)
        st.markdown(draw_table("🟡 TENGAH (1-7)", "tengah", "bg-mid", 7), unsafe_allow_html=True)
        st.markdown(draw_table("🔴 KONTRA (1-8)", "kontra", "bg-kontra", 8), unsafe_allow_html=True)

        st.markdown("---")
        sh_txt = f"Master Brain v13.1 Result: {history[-1]}"
        share_btn = f"""<button onclick="navigator.share({{title:'Master Brain v13.1', text:'{sh_txt}'}})" style="width:100%; background-color:{t['btn']}; color:{t['btn_txt']}; padding:15px; border:none; border-radius:12px; font-size:20px; font-weight:bold; cursor:pointer;">📲 BAGIKAN HASIL</button>"""
        components.html(share_btn, height=100)
else:
    st.info("💡 Sistem Adaptif Aktif. Prediksi akan menyesuaikan otomatis dengan jenis data yang Anda masukkan.")
