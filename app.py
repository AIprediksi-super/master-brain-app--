import streamlit as st
from collections import Counter
import random

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Master Brain v22.0: High Precision", layout="wide")

# --- 2. INITIAL SESSION STATE ---
if 'history' not in st.session_state: st.session_state.history = []
if 'input_area' not in st.session_state: st.session_state.input_area = ""

# --- 3. DAFTAR TEMA (SAMA DENGAN V18.0) ---
app_themes = {
    "Pelangi & Cosmic 🌈": {"bg": "linear-gradient(135deg, #1a2a6c, #b21f1f, #fdbb2d)", "txt": "#FFFFFF"},
    "Biru Laut & Nature": {"bg": "linear-gradient(to bottom, #000428, #004e92)", "txt": "#E0F7FA"},
    "Gelap Neon (Leaf)": {"bg": "#0E1117", "txt": "#00FF00"},
}

p_app = st.sidebar.selectbox("Tema Aplikasi:", list(app_themes.keys()))
t_app = app_themes[p_app]

# --- 4. CSS STYLING (KEMBALI KE V18.0) ---
st.markdown(f"""
    <style>
    .stApp {{ background: {t_app['bg']}; color: {t_app['txt']}; }}
    .leaf-frame {{ position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; border: 20px solid transparent; z-index: 9999; animation: leafMove 5s infinite alternate ease-in-out; }}
    @keyframes leafMove {{ 0% {{ transform: scale(1); filter: hue-rotate(0deg); }} 100% {{ transform: scale(1.02); filter: hue-rotate(20deg); }} }}
    .star {{ position: absolute; background: white; border-radius: 50%; opacity: 0.5; animation: fall linear infinite; }}
    @keyframes fall {{ from {{ transform: translateY(-10vh); }} to {{ transform: translateY(110vh); }} }}
    .predict-table {{ width: 100%; border-collapse: separate; border-spacing: 5px; }}
    .predict-table td {{ 
        border-radius: 12px; padding: 15px; text-align: center; font-size: 28px; font-weight: 900; 
        color: white !important; -webkit-text-stroke: 1px black; text-shadow: 2px 2px 4px #000;
    }}
    .dead-row {{ background: rgba(255, 0, 0, 0.6) !important; font-size: 18px !important; color: #ffcccc !important; }}
    .boom-box {{ 
        background: rgba(0,0,0,0.5); padding: 20px; border-radius: 15px; border: 2px solid gold; 
        text-align: center; margin-bottom: 10px;
    }}
    </style>
    <div class="leaf-frame"></div>
    """, unsafe_allow_html=True)

# --- 5. ANIMASI BINTANG ---
for i in range(15):
    st.markdown(f'<div class="star" style="width:3px; height:3px; left:{random.randint(0,100)}%; animation-duration:{random.randint(5,10)}s;"></div>', unsafe_allow_html=True)

# --- 6. INPUT AREA ---
manual_input = st.text_area("Tempel Data 4D:", height=150, value=st.session_state.input_area)

# --- 7. MESIN PREDIKSI V22.0 (AKURASI DIPERBAIKI) ---
def get_advanced_predictions(data):
    if not data: return None
    rows = [[int(d) for d in item if d.isdigit()][:4] for item in data if len([c for c in item if c.isdigit()]) >= 4]
    if len(rows) < 5: return None

    final_results = []
    # Logika: Moving Average & Decay Factor
    # Memberikan bobot sangat tinggi pada 5-10 data terakhir saja
    for i in range(4):
        col = [r[i] for r in rows]
        scores = {}
        for n in range(10):
            # Hitung frekuensi dasar
            freq = col.count(n)
            # Hitung kemunculan di 10 data terakhir (Bobot Utama)
            recent_15 = col[-15:].count(n)
            # Hitung jarak (gap) - semakin lama tidak keluar, skor bertambah dikit (potensi keluar)
            try: last_idx = len(col) - 1 - list(reversed(col)).index(n)
            except: last_idx = 0
            gap = len(col) - last_idx
            
            # RUMUS: (Dasar * 1) + (Recent * 25) + (Gap * 0.7)
            scores[n] = (freq * 1) + (recent_15 * 25) + (gap * 0.7)
            
        final_results.append(sorted(scores.items(), key=lambda x: x[1], reverse=True))
    return final_results

# --- 8. TOMBOL AKSI ---
if st.button("🚀 JALANKAN ANALISA AKURAT"):
    if manual_input:
        st.session_state.history = manual_input.replace(',', ' ').split()

# --- 9. DISPLAY HASIL ---
if st.session_state.history:
    res = get_advanced_predictions(st.session_state.history)
    if res:
        # TRIPLE BOOM
        st.subheader("💣 BOOM PREDIKSI TERKUAT")
        b1, b2, b3 = st.columns(3)
        with b1: st.markdown(f"<div class='boom-box'>BOOM #1<br><h1 style='color:#00ffcc;'>{''.join([str(res[i][0][0]) for i in range(4)])}</h1></div>", unsafe_allow_html=True)
        with b2: st.markdown(f"<div class='boom-box'>BOOM #2<br><h1 style='color:#ffff00;'>{''.join([str(res[i][1][0]) for i in range(4)])}</h1></div>", unsafe_allow_html=True)
        with b3: st.markdown(f"<div class='boom-box'>BOOM #3<br><h1 style='color:#ff00ff;'>{''.join([str(res[i][2][0]) for i in range(4)])}</h1></div>", unsafe_allow_html=True)

        # TABEL PREDIKSI
        st.subheader("📊 TABEL TRACKING ANALISA")
        h = "<table class='predict-table'><tr><th>LEVEL</th><th>KOL 1</th><th>KOL 2</th><th>KOL 3</th><th>KOL 4</th></tr>"
        # Rank 1-5
        for r in range(5):
            h += f"<tr><td style='font-size:12px; background:rgba(0,0,0,0.5);'>RANK {r+1}</td>"
            for c in range(4):
                h += f"<td style='background:linear-gradient(135deg, #56ab2f, #a8e063);'>{res[c][r][0]}</td>"
            h += "</tr>"
        # Angka Mati (2 Baris Terakhir)
        for r in range(8, 10):
            h += f"<tr class='dead-row'><td>DEAD</td>"
            for c in range(4):
                h += f"<td>{res[c][r][0]}</td>"
            h += "</tr>"
        st.markdown(h + "</table>", unsafe_allow_html=True)
