import streamlit as st
from collections import Counter
import random

# --- CONFIG UI ---
st.set_page_config(page_title="Master Brain v15: Nature Glow", layout="wide")

if 'history' not in st.session_state:
    st.session_state.history = []

# --- DAFTAR TEMA & GRADASI ---
app_themes = {
    "Pelangi & Cosmic 🌈": {"bg": "linear-gradient(135deg, #1a2a6c, #b21f1f, #fdbb2d)", "txt": "#FFFFFF", "btn": "#FFFFFF", "btn_txt": "black"},
    "Biru Laut & Nature": {"bg": "linear-gradient(to bottom, #000428, #004e92)", "txt": "#E0F7FA", "btn": "#00E5FF", "btn_txt": "black"},
    "Gelap Neon (Leaf)": {"bg": "#0E1117", "txt": "#00FF00", "btn": "#00FF00", "btn_txt": "black"},
}

gradien_options = {
    "Hijau Emerald": "linear-gradient(135deg, #56ab2f 0%, #a8e063 100%)",
    "Biru Cyan": "linear-gradient(135deg, #00d2ff 0%, #3a7bd5 100%)",
    "Merah Muda Magma": "linear-gradient(135deg, #f80759 0%, #bc4e9c 100%)",
    "Emas Mewah": "linear-gradient(135deg, #f2994a 0%, #f2c94c 100%)"
}

# --- CSS ANIMASI: BINTANG & DAUN ---
p_app = st.sidebar.selectbox("Tema Aplikasi:", list(app_themes.keys()))
t_app = app_themes[p_app]

st.markdown(f"""
    <style>
    /* LATAR BELAKANG BINTANG JATUH */
    .stApp {{ 
        background: {t_app['bg']}; 
        color: {t_app['txt']}; 
        overflow-x: hidden;
    }}
    
    /* ANIMASI BINGKAI DAUN BERGERAK */
    .leaf-frame {{
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        pointer-events: none;
        border: 20px solid transparent;
        border-image: url('https://transparentpng.com') 30 stretch;
        z-index: 9999;
        animation: leafMove 5s infinite alternate ease-in-out;
    }}
    
    @keyframes leafMove {{
        0% {{ transform: scale(1); filter: hue-rotate(0deg); }}
        100% {{ transform: scale(1.02); filter: hue-rotate(20deg); }}
    }}

    /* EFEK BINTANG JATUH (STARS) */
    .star {{
        position: absolute; background: white; border-radius: 50%; opacity: 0.5;
        animation: fall linear infinite;
    }}
    @keyframes fall {{
        from {{ transform: translateY(-10vh) translateX(0); }}
        to {{ transform: translateY(110vh) translateX(20vw); }}
    }}

    /* TABEL PREMIUM */
    .predict-table {{ width: 100%; border-collapse: separate; border-spacing: 5px; }}
    .predict-table td {{ 
        border-radius: 12px; padding: 15px; text-align: center; font-size: 32px; font-weight: 900; 
        color: white !important; -webkit-text-stroke: 1.5px black;
        text-shadow: 0 0 15px rgba(255,255,255,0.7), 3px 3px 5px #000;
        box-shadow: inset 0 0 10px rgba(0,0,0,0.5);
    }}
    
    textarea {{ color: #FFFFFF !important; font-weight: bold !important; font-size: 20px !important; background: rgba(0,0,0,0.4) !important; }}
    </style>
    
    <div class="leaf-frame"></div>
    """, unsafe_allow_html=True)

# Memasukkan elemen bintang secara acak
for _ in range(20):
    size = random.randint(2, 5)
    left = random.randint(0, 100)
    dur = random.randint(3, 8)
    st.markdown(f'<div class="star" style="width:{size}px; height:{size}px; left:{left}%; animation-duration:{dur}s;"></div>', unsafe_allow_html=True)

st.title("🧠 MASTER BRAIN V15: COSMIC LEAF")

# --- KONTROL GRADASI ---
c_t1, c_t2, c_t3 = st.columns(3)
with c_t1: p_t1 = st.selectbox("Gradasi Tabel 1:", list(gradien_options.keys()), index=0)
with c_t2: p_t2 = st.selectbox("Gradasi Tabel 2:", list(gradien_options.keys()), index=1)
with c_t3: p_t3 = st.selectbox("Gradasi Tabel 3:", list(gradien_options.keys()), index=2)

g1, g2, g3 = gradien_options[p_t1], gradien_options[p_t2], gradien_options[p_t3]

# --- INPUT UTAMA ---
manual_input = st.text_area("Tempel Data 4-Digit:", height=150, key="input_area", placeholder="Tempel histori di sini...")

def reset_paste(): st.session_state["input_area"] = ""
def reset_all(): 
    st.session_state["input_area"] = ""
    st.session_state.history = []

c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🚀 JALANKAN ANALISA"):
        if manual_input: st.session_state.history = manual_input.replace(',', ' ').split()
with c2: st.button("🗑️ HAPUS TEKS PASTE", on_click=reset_paste)
with c3: st.button("🔴 RESET SEMUA DATA", on_click=reset_all)

# --- ENGINE ANALISA ---
def get_predictions(data, mode):
    cols = [[] for _ in range(4)]
    for item in data:
        chars = [c for c in item if c.isdigit()]
        for i in range(min(4, len(chars))): cols[i].append(chars[i])
    results = []
    for i in range(4):
        d, all_digits = cols[i], "0123456789"
        freq = Counter(d) if d else {}
        sorted_by_freq = sorted(all_digits, key=lambda x: freq.get(x, 0), reverse=True)
        if mode == "seimbang": results.append(sorted_by_freq[1:8])
        elif mode == "akurat": results.append(sorted_by_freq[:7])
        else: results.append(sorted_by_freq[::-1][:8])
    return results

# --- OUTPUT TABEL ---
if st.session_state.history:
    st.markdown("---")
    tabs = [("🍀 TABEL SEIMBANG", "seimbang", g1), ("🔥 TABEL AKURAT", "akurat", g2), ("❄️ TABEL KONTRA", "kontra", g3)]
    for title, mode, grad in tabs:
        st.subheader(title)
        data = get_predictions(st.session_state.history, mode)
        rows = 8 if mode == "kontra" else 7
        html = f"<table class='predict-table'><tr><th>RANK</th><th>KOL 1</th><th>KOL 2</th><th>KOL 3</th><th>KOL 4</th></tr>"
        for r in range(rows):
            html += f"<tr><td style='font-size:12px; background:rgba(0,0,0,0.5);'>#{r+1}</td>"
            for c in range(4):
                html += f"<td style='background:{grad};'>{data[c][r]}</td>"
            html += "</tr>"
        st.markdown(html + "</table>", unsafe_allow_html=True)
else:
    st.info("💡 Masukkan data di atas untuk melihat tabel prediksi dengan efek Cosmic Leaf.")
