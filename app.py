import streamlit as st
from collections import Counter
import random

# --- 1. CONFIG & STATE ---
st.set_page_config(page_title="Master Brain v15: Ultimate Master", layout="wide")
if 'history' not in st.session_state: st.session_state.history = []

# --- 2. DAFTAR TEMA & GRADASI ---
app_themes = {
    "Pelangi & Cosmic 🌈": {"bg": "linear-gradient(135deg, #1a2a6c, #b21f1f, #fdbb2d)", "txt": "#FFFFFF"},
    "Biru Laut & Nature": {"bg": "linear-gradient(to bottom, #000428, #004e92)", "txt": "#E0F7FA"},
    "Gelap Neon (Leaf)": {"bg": "#0E1117", "txt": "#00FF00"},
}
gradien_options = {"Hijau Emerald": "linear-gradient(135deg, #56ab2f 0%, #a8e063 100%)", "Biru Cyan": "linear-gradient(135deg, #00d2ff 0%, #3a7bd5 100%)", "Merah Muda Magma": "linear-gradient(135deg, #f80759 0%, #bc4e9c 100%)", "Emas Mewah": "linear-gradient(135deg, #f2994a 0%, #f2c94c 100%)"}

p_app = st.sidebar.selectbox("Tema Aplikasi:", list(app_themes.keys()))
t_app = app_themes[p_app]

# --- 3. CSS & ANIMASI ---
st.markdown(f"""
    <style>
    .stApp {{ background: {t_app['bg']}; color: {t_app['txt']}; overflow-x: hidden; }}
    .predict-table {{ width: 100%; border-collapse: separate; border-spacing: 5px; }}
    .predict-table td {{ border-radius: 12px; padding: 15px; text-align: center; font-size: 32px; font-weight: 900; color: white !important; -webkit-text-stroke: 1.5px black; text-shadow: 0 0 15px rgba(255,255,255,0.7), 3px 3px 5px #000; box-shadow: inset 0 0 10px rgba(0,0,0,0.5); }}
    textarea {{ color: white !important; font-weight: bold !important; font-size: 20px !important; background: rgba(0,0,0,0.4) !important; }}
    </style>
    """, unsafe_allow_html=True)

st.title("🧠 MASTER BRAIN V15: ULTIMATE MASTER")

# --- 4. KONTROL & INPUT ---
c_t1, c_t2, c_t3 = st.columns(3)
with c_t1: p_t1 = st.selectbox("Gradasi Tabel 1:", list(gradien_options.keys()), index=0)
with c_t2: p_t2 = st.selectbox("Gradasi Tabel 2:", list(gradien_options.keys()), index=1)
with c_t3: p_t3 = st.selectbox("Gradasi Tabel 3:", list(gradien_options.keys()), index=2)
g1, g2, g3 = gradien_options[p_t1], gradien_options[p_t2], gradien_options[p_t3]

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

# --- 6. ENGINE ANALISA ---
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
            skor = 0.0
            skor += d.count(angka) * 0.5 
            skor += d[-5:].count(angka) * 3.5 
            for j in range(len(d)-1):
                if d[j] == d[-1] and d[j+1] == angka: skor += 8.0
            return skor
        scored = sorted(all_digits, key=hitung_skor, reverse=True)
        if filter_mode == "Ganjil": filtered = [x for x in scored if int(x)%2!=0]
        elif filter_mode == "Genap": filtered = [x for x in scored if int(x)%2==0]
        elif filter_mode == "Kecil (0-4)": filtered = [x for x in scored if int(x)<=4]
        elif filter_mode == "Besar (5-9)": filtered = [x for x in scored if int(x)>=5]
        else: filtered = scored
        if mode == "akurat": results.append(filtered)
        elif mode == "seimbang": results.append(filtered)
        else: results.append(filtered[::-1])
    return results

# --- 7. DISPLAY TABEL ---
if st.session_state.history:
    recent_8 = st.session_state.history[-8:]
    all_table_data = {"seimbang": [], "akurat": [], "kontra": [], "master": []}
    
    confs = [("🍀 TABEL SEIMBANG", "seimbang", g1), ("🔥 TABEL AKURAT", "akurat", g2), ("❄️ TABEL KONTRA", "kontra", g3)]
    for title, mode, grad in confs:
        st.subheader(title)
        res = get_predictions(st.session_state.history, mode, p_filter)
        if res:
            all_table_data[mode] = res
            limit = 6 if mode != "kontra" else (4 if p_filter != "Semua" else 8)
            d_res = [c[1:7] if mode == "seimbang" else c[:limit] for c in res]
            
            html = f"<table class='predict-table'><tr><th>RANK</th><th>KOL 1</th><th>KOL 2</th><th>KOL 3</th><th>KOL 4</th></tr>"
            for r in range(len(d_res)):
                html += f"<tr><td style='font-size:12px; background:rgba(0,0,0,0.5);'>#{r+1}</td>"
                for c in range(4): html += f"<td style='background:{grad};'>{d_res[c][r]}</td>"
                html += "</tr>"
            st.markdown(html + "</table>", unsafe_allow_html=True)

    st.subheader("💎 TABEL MASTER")
    l_m = 4 if p_filter != "Semua" else 6
    m_final = [[] for _ in range(4)]
    for c in range(4):
        pool = all_table_data["akurat"][c] + all_table_data["seimbang"][c]
        cts = Counter(pool)
        m_sc = {k: cts[k] + (sum(1 for row in recent_8 if str(k) in row) * 2.0) for k in cts}
        top = sorted(m_sc, key=m_sc.get, reverse=True)[:l_m]
        while len(top) < l_m: top.append("-")
        m_final[c] = top
    all_table_data["master"] = m_final
    g_m = "linear-gradient(135deg, #FFD700 0%, #B8860B 100%)"
    h_m = f"<table class='predict-table'><tr><th>RANK</th><th>KOL 1</th><th>KOL 2</th><th>KOL 3</th><th>KOL 4</th></tr>"
    for r in range(l_m):
        h_m += f"<tr><td style='font-size:12px; background:rgba(0,0,0,0.5);'>#{r+1}</td>"
        for c in range(4): h_m += f"<td style='background:{g_m};'>{m_final[c][r]}</td>"
        h_m += "</tr>"
    st.markdown(h_m + "</table>", unsafe_allow_html=True)

    # 💀 7c. TABEL ELIMINASI (FIXED WITH BRACKETS)
    st.markdown("---")
    st.subheader("💀 TABEL ELIMINASI (ANGKA MATI)")
    l_e = 4 if p_filter != "Semua" else 8
    e_final = [[] for _ in range(4)]
    for c in range(4):
        raw_list = all_table_data["seimbang"][c][-2:] + all_table_data["akurat"][c][-2:] + all_table_data["kontra"][c][-2:] + all_table_data["master"][c][-2:]
        proc = []
        for m in raw_list:
            if m == "-": proc.append("-")
            else:
                is_active = sum(1 for row in recent_8 if str(m) in row)
                proc.append(f"({m})" if is_active > 0 else m)
        res_e = proc[:l_e]
        while len(res_e) < l_e: res_e.append("-")
        e_final[c] = res_e
        
    g_e = "linear-gradient(135deg, #232526 0%, #414345 100%)"
    h_e = f"<table class='predict-table'><tr><th>DEAD</th><th>KOL 1</th><th>KOL 2</th><th>KOL 3</th><th>KOL 4</th></tr>"
    for r in range(l_e):
        h_e += f"<tr><td style='font-size:12px; background:red;'>DEAD</td>"
        for c in range(4): h_e += f"<td style='background:{g_e}; color:#FF4B4B !important;'>{e_final[c][r]}</td>"
        h_e += "</tr>"
    st.markdown(h_e + "</table>", unsafe_allow_html=True)
