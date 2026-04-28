import streamlit as st
from collections import Counter
import random

# --- 1. CONFIG & STATE (TETAP) ---
st.set_page_config(page_title="Master Brain v15: Ultimate Edition", layout="wide")
if 'history' not in st.session_state: st.session_state.history = []

# --- 2. DAFTAR TEMA & GRADASI (TETAP) ---
app_themes = {
    "Pelangi & Cosmic 🌈": {"bg": "linear-gradient(135deg, #1a2a6c, #b21f1f, #fdbb2d)", "txt": "#FFFFFF"},
    "Biru Laut & Nature": {"bg": "linear-gradient(to bottom, #000428, #004e92)", "txt": "#E0F7FA"},
    "Gelap Neon (Leaf)": {"bg": "#0E1117", "txt": "#00FF00"},
}
gradien_options = {"Hijau Emerald": "linear-gradient(135deg, #56ab2f 0%, #a8e063 100%)", "Biru Cyan": "linear-gradient(135deg, #00d2ff 0%, #3a7bd5 100%)", "Merah Muda Magma": "linear-gradient(135deg, #f80759 0%, #bc4e9c 100%)", "Emas Mewah": "linear-gradient(135deg, #f2994a 0%, #f2c94c 100%)"}

p_app = st.sidebar.selectbox("Tema Aplikasi:", list(app_themes.keys()))
t_app = app_themes[p_app]

# --- 3. CSS & ANIMASI (TETAP) ---
st.markdown(f"""
    <style>
    .stApp {{ background: {t_app['bg']}; color: {t_app['txt']}; overflow-x: hidden; }}
    .leaf-frame {{ position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; border: 20px solid transparent; z-index: 9999; animation: leafMove 5s infinite alternate ease-in-out; }}
    @keyframes leafMove {{ 0% {{ transform: scale(1); filter: hue-rotate(0deg); }} 100% {{ transform: scale(1.02); filter: hue-rotate(20deg); }} }}
    .star {{ position: absolute; background: white; border-radius: 50%; opacity: 0.5; animation: fall linear infinite; }}
    @keyframes fall {{ from {{ transform: translateY(-10vh) translateX(0); }} to {{ transform: translateY(110vh) translateX(20vw); }} }}
    .predict-table {{ width: 100%; border-collapse: separate; border-spacing: 5px; }}
    .predict-table td {{ border-radius: 12px; padding: 15px; text-align: center; font-size: 32px; font-weight: 900; color: white !important; -webkit-text-stroke: 1.5px black; text-shadow: 0 0 15px rgba(255,255,255,0.7), 3px 3px 5px #000; box-shadow: inset 0 0 10px rgba(0,0,0,0.5); }}
    textarea {{ color: white !important; font-weight: bold !important; font-size: 20px !important; background: rgba(0,0,0,0.4) !important; }}
    </style>
    <div class="leaf-frame"></div>
    """, unsafe_allow_html=True)

for _ in range(20):
    size, left, dur = random.randint(2, 5), random.randint(0, 100), random.randint(3, 8)
    st.markdown(f'<div class="star" style="width:{size}px; height:{size}px; left:{left}%; animation-duration:{dur}s;"></div>', unsafe_allow_html=True)

st.title("🧠 MASTER BRAIN V15: ULTIMATE MASTER")

# --- 4. KONTROL GRADASI (TETAP) ---
c_t1, c_t2, c_t3 = st.columns(3)
with c_t1: p_t1 = st.selectbox("Gradasi Tabel 1:", list(gradien_options.keys()), index=0)
with c_t2: p_t2 = st.selectbox("Gradasi Tabel 2:", list(gradien_options.keys()), index=1)
with c_t3: p_t3 = st.selectbox("Gradasi Tabel 3:", list(gradien_options.keys()), index=2)
g1, g2, g3 = gradien_options[p_t1], gradien_options[p_t2], gradien_options[p_t3]

# --- 5. FILTER & INPUT (TETAP) ---
st.markdown("---")
p_filter = st.radio("Saring hasil angka:", ["Semua", "Ganjil", "Genap", "Kecil (0-4)", "Besar (5-9)"], horizontal=True)
manual_input = st.text_area("Tempel Data 4-Digit:", height=150, key="input_area")

def reset_paste(): st.session_state["input_area"] = ""
def reset_all(): 
    st.session_state["input_area"] = ""
    st.session_state.history = []

c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🚀 JALANKAN ANALISA"):
        if manual_input: st.session_state.history = manual_input.replace(',', ' ').replace('\n', ' ').split()
with c2: st.button("🗑️ HAPUS TEKS PASTE", on_click=reset_paste)
with c3: st.button("🔴 RESET SEMUA DATA", on_click=reset_all)

# --- 6. ENGINE ANALISA (SUPER POWER AI) ---
def get_predictions(data, mode, filter_mode):
    if not data: return []
    cols = [[] for _ in range(4)]
    for item in data:
        chars = [c for c in item if c.isdigit()]
        if len(chars) >= 4:
            for i in range(4): cols[i].append(chars[i])
    results = []
    for i in range(4):
        d = cols[i]
        if not d: continue
        all_digits = [str(x) for x in range(10)]
        def hitung_skor(angka):
            sk = 0.0
            sk += d.count(angka) * 0.5 
            sk += d[-5:].count(angka) * 3.5 
            for j in range(len(d)-1):
                if d[j] == d[-1] and d[j+1] == angka: sk += 8.0
            return sk
        scored = sorted(all_digits, key=hitung_skor, reverse=True)
        if filter_mode == "Ganjil": filtered = [x for x in scored if int(x)%2!=0]
        elif filter_mode == "Genap": filtered = [x for x in scored if int(x)%2==0]
        elif filter_mode == "Kecil (0-4)": filtered = [x for x in scored if int(x)<=4]
        elif filter_mode == "Besar (5-9)": filtered = [x for x in scored if int(x)>=5]
        else: filtered = scored
        if mode == "akurat" or mode == "seimbang": results.append(filtered)
        else: results.append(filtered[::-1])
    return results

# --- 7. DISPLAY TABEL ---
if st.session_state.history:
    r8 = st.session_state.history[-8:]
    all_data = {"seimbang": [], "akurat": [], "kontra": [], "master": []}
    
    confs = [("🍀 TABEL SEIMBANG", "seimbang", g1), ("🔥 TABEL AKURAT", "akurat", g2), ("❄️ TABEL KONTRA", "kontra", g3)]
    for title, mode, grad in confs:
        st.subheader(title)
        res = get_predictions(st.session_state.history, mode, p_filter)
        if res:
            all_data[mode] = res
            if mode == "kontra": limit = 4 if p_filter != "Semua" else 8
            else: limit = 4 if p_filter != "Semua" else 6
            
            d_res = [c[1:limit+1] if mode == "seimbang" else c[:limit] for c in res]
            html = f"<table class='predict-table'><tr><th>RANK</th><th>KOL 1</th><th>KOL 2</th><th>KOL 3</th><th>KOL 4</th></tr>"
            for r in range(len(d_res)):
                html += f"<tr><td style='font-size:12px; background:rgba(0,0,0,0.5);'>#{r+1}</td>"
                for c in range(4): html += f"<td style='background:{grad};'>{d_res[c][r]}</td>"
                html += "</tr>"
            st.markdown(html + "</table>", unsafe_allow_html=True)

    st.subheader("💎 TABEL MASTER")
    lm = 4 if p_filter != "Semua" else 6
    mf = [[] for _ in range(4)]
    for c in range(4):
        p = all_data["akurat"][c][:5] + all_data["seimbang"][c][:5]
        cts = Counter(p)
        ms = {k: cts[k] + (sum(1 for row in r8 if str(k) in row) * 2.0) for k in cts}
        top = sorted(ms, key=ms.get, reverse=True)[:lm]
        while len(top) < lm: top.append("-")
        mf[c] = top
    all_data["master"] = mf
    gm = "linear-gradient(135deg, #FFD700 0%, #B8860B 100%)"
    hm = f"<table class='predict-table'><tr><th>RANK</th><th>KOL 1</th><th>KOL 2</th><th>KOL 3</th><th>KOL 4</th></tr>"
    for r in range(lm):
        hm += f"<tr><td style='font-size:12px; background:rgba(0,0,0,0.5);'>#{r+1}</td>"
        for c in range(4): hm += f"<td style='background:{gm};'>{mf[c][r]}</td>"
        hm += "</tr>"
    st.markdown(hm + "</table>", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("💀 TABEL ELIMINASI (ANGKA MATI)")
    le = 4 if p_filter != "Semua" else 8
    ef = [[] for _ in range(4)]
    for c in range(4):
        m = all_data["seimbang"][c][-2:] + all_data["akurat"][c][-2:] + all_data["kontra"][c][-2:] + all_data["master"][c][-2:]
        pr = [f"({x})" if sum(1 for row in r8 if str(x) in row) > 0 else x for x in m]
        res_e = pr[:le]
        while len(res_e) < le: res_e.append("-")
        ef[c] = res_e
    ge = "linear-gradient(135deg, #232526 0%, #414345 100%)"
    he = f"<table class='predict-table'><tr><th>DEAD</th><th>KOL 1</th><th>KOL 2</th><th>KOL 3</th><th>KOL 4</th></tr>"
    for r in range(le):
        he += f"<tr><td style='font-size:12px; background:red;'>DEAD</td>"
        for c in range(4): he += f"<td style='background:{ge}; color:#FF4B4B !important;'>{ef[c][r]}</td>"
        he += "</tr>"
    st.markdown(he + "</table>", unsafe_allow_html=True)
