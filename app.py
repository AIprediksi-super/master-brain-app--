import streamlit as st
from collections import Counter
import random

# --- 1. CONFIG & STATE ---
st.set_page_config(page_title="Master Brain v15: Ultimate Master", layout="wide")
if 'history' not in st.session_state: st.session_state.history = []

# --- 2. THEMES & CSS (UTUH) ---
app_themes = {
    "Pelangi & Cosmic 🌈": {"bg": "linear-gradient(135deg, #1a2a6c, #b21f1f, #fdbb2d)", "txt": "#FFFFFF"},
    "Biru Laut & Nature": {"bg": "linear-gradient(to bottom, #000428, #004e92)", "txt": "#E0F7FA"},
    "Gelap Neon (Leaf)": {"bg": "#0E1117", "txt": "#00FF00"},
}
gradien_options = {"Hijau Emerald": "linear-gradient(135deg, #56ab2f 0%, #a8e063 100%)", "Biru Cyan": "linear-gradient(135deg, #00d2ff 0%, #3a7bd5 100%)", "Merah Muda Magma": "linear-gradient(135deg, #f80759 0%, #bc4e9c 100%)", "Emas Mewah": "linear-gradient(135deg, #f2994a 0%, #f2c94c 100%)"}

p_app = st.sidebar.selectbox("Tema Aplikasi:", list(app_themes.keys()))
t_app = app_themes[p_app]
st.markdown(f"<style>.stApp {{ background: {t_app['bg']}; color: {t_app['txt']}; overflow-x: hidden; }} .predict-table {{ width: 100%; border-collapse: separate; border-spacing: 5px; }} .predict-table td {{ border-radius: 12px; padding: 15px; text-align: center; font-size: 32px; font-weight: 900; color: white !important; -webkit-text-stroke: 1.5px black; text-shadow: 0 0 15px rgba(255,255,255,0.7), 3px 3px 5px #000; box-shadow: inset 0 0 10px rgba(0,0,0,0.5); }} textarea {{ color: #FFFFFF !important; font-weight: bold !important; font-size: 20px !important; background: rgba(0,0,0,0.4) !important; }} </style>", unsafe_allow_html=True)

st.title("🧠 MASTER BRAIN V15: ULTIMATE MASTER")

# --- 4. KONTROL & INPUT ---
c_t1, c_t2, c_t3 = st.columns(3)
with c_t1: p_t1 = st.selectbox("Gradasi Tabel 1:", list(gradien_options.keys()), index=0)
with c_t2: p_t2 = st.selectbox("Gradasi Tabel 2:", list(gradien_options.keys()), index=1)
with c_t3: p_t3 = st.selectbox("Gradasi Tabel 3:", list(gradien_options.keys()), index=2)
g1, g2, g3 = gradien_options[p_t1], gradien_options[p_t2], gradien_options[p_t3]

p_filter = st.radio("Saring hasil angka:", ["Semua", "Ganjil", "Genap", "Kecil (0-4)", "Besar (5-9)"], horizontal=True)
manual_input = st.text_area("Tempel Data 4-Digit:", height=150, key="input_area")

if st.button("🚀 JALANKAN ANALISA"):
    if manual_input: st.session_state.history = manual_input.replace(',', ' ').replace('\n', ' ').split()

# --- 6. ENGINE ANALISA: TRUE CATEGORY LOGIC ---
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
            total_n = len(d)
            # Logika Inti (Adjacent, Cycle, Momentum)
            skor += d.count(angka) * 1.0
            skor += d[-5:].count(angka) * 3.0
            for j in range(total_n - 1):
                if d[j] == d[-1] and d[j+1] == angka: skor += 6.0
            return skor

        scored = sorted(all_digits, key=hitung_skor, reverse=True)
        # Filter tetap berlaku
        if filter_mode == "Ganjil": filtered = [x for x in scored if int(x)%2!=0]
        elif filter_mode == "Genap": filtered = [x for x in scored if int(x)%2==0]
        elif filter_mode == "Kecil (0-4)": filtered = [x for x in scored if int(x)<=4]
        elif filter_mode == "Besar (5-9)": filtered = [x for x in scored if int(x)>=5]
        else: filtered = scored

        # PEMISAHAN KARAKTER TABEL
        if mode == "akurat":
            # Isi: Benar-benar angka peringkat teratas
            results.append(filtered[:6])
        elif mode == "seimbang":
            # Isi: Angka kemungkinan (diambil dari tengah/acak stabil)
            results.append(filtered[1:7] if len(filtered) > 1 else filtered)
        else: # mode == "kontra"
            # Isi: Angka yang benar-benar tidak ada harapan (skor terendah)
            limit_k = 4 if filter_mode != "Semua" else 8
            results.append(filtered[::-1][:limit_k])
    return results

# --- 7. DISPLAY TABEL ---
if st.session_state.history:
    pool_master = [[] for _ in range(4)]
    
    # Render 3 Tabel Utama
    confs = [("🍀 TABEL SEIMBANG", "seimbang", g1), ("🔥 TABEL AKURAT", "akurat", g2), ("❄️ TABEL KONTRA", "kontra", g3)]
    for title, mode, grad in confs:
        st.subheader(title)
        res = get_predictions(st.session_state.history, mode, p_filter)
        if res:
            html = f"<table class='predict-table'><tr><th>RANK</th><th>KOL 1</th><th>KOL 2</th><th>KOL 3</th><th>KOL 4</th></tr>"
            max_r = max(len(c) for c in res)
            for r in range(max_r):
                html += f"<tr><td style='font-size:12px; background:rgba(0,0,0,0.5);'>#{r+1}</td>"
                for c in range(4):
                    val = res[c][r] if r < len(res[c]) else "-"
                    html += f"<td style='background:{grad};'>{val}</td>"
                    if val != "-": pool_master[c].append(val)
                html += "</tr>"
            st.markdown(html + "</table>", unsafe_allow_html=True)

    # 💎 TABEL MASTER (PREDIKSI LAPIS KEDUA)
    st.markdown("---")
    st.subheader("💎 TABEL MASTER (FINAL AI PREDICTION)")
    grad_master = "linear-gradient(135deg, #FFD700 0%, #B8860B 100%)"
    html_m = f"<table class='predict-table'><tr><th>RANK</th><th>KOL 1</th><th>KOL 2</th><th>KOL 3</th><th>KOL 4</th></tr>"
    
    for c in range(4):
        # Master mengambil intisari unik dari ketiga tabel di atas
        c_counts = Counter(pool_master[c]).most_common(6)
        final_vals = [x[0] for x in c_counts]
        while len(final_vals) < 6: final_vals.append("-")
        pool_master[c] = final_vals

    for r in range(6):
        html_m += f"<tr><td style='font-size:12px; background:rgba(0,0,0,0.5);'>#{r+1}</td>"
        for c in range(4):
            val = pool_master[c][r]
            html_m += f"<td style='background:{grad_master};'>{val}</td>"
        html_m += "</tr>"
    st.markdown(html_m + "</table>", unsafe_allow_html=True)
