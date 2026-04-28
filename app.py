import streamlit as st
from collections import Counter
import random

# --- 1. CONFIG & STATE (UTUH) ---
st.set_page_config(page_title="Master Brain v15: Ultimate Edition", layout="wide")

if 'history' not in st.session_state:
    st.session_state.history = []

# --- 2. DAFTAR TEMA & GRADASI (UTUH) ---
app_themes = {
    "Pelangi & Cosmic 🌈": {"bg": "linear-gradient(135deg, #1a2a6c, #b21f1f, #fdbb2d)", "txt": "#FFFFFF"},
    "Biru Laut & Nature": {"bg": "linear-gradient(to bottom, #000428, #004e92)", "txt": "#E0F7FA"},
    "Gelap Neon (Leaf)": {"bg": "#0E1117", "txt": "#00FF00"},
}

gradien_options = {
    "Hijau Emerald": "linear-gradient(135deg, #56ab2f 0%, #a8e063 100%)",
    "Biru Cyan": "linear-gradient(135deg, #00d2ff 0%, #3a7bd5 100%)",
    "Merah Muda Magma": "linear-gradient(135deg, #f80759 0%, #bc4e9c 100%)",
    "Emas Mewah": "linear-gradient(135deg, #f2994a 0%, #f2c94c 100%)"
}

p_app = st.sidebar.selectbox("Tema Aplikasi:", list(app_themes.keys()))
t_app = app_themes[p_app]

# --- 3. CSS & ANIMASI (UTUH) ---
st.markdown(f"""
    <style>
    .stApp {{ background: {t_app['bg']}; color: {t_app['txt']}; overflow-x: hidden; }}
    .leaf-frame {{
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        pointer-events: none; border: 20px solid transparent;
        z-index: 9999; animation: leafMove 5s infinite alternate ease-in-out;
    }}
    @keyframes leafMove {{ 0% {{ transform: scale(1); filter: hue-rotate(0deg); }} 100% {{ transform: scale(1.02); filter: hue-rotate(20deg); }} }}
    .star {{ position: absolute; background: white; border-radius: 50%; opacity: 0.5; animation: fall linear infinite; }}
    @keyframes fall {{ from {{ transform: translateY(-10vh) translateX(0); }} to {{ transform: translateY(110vh) translateX(20vw); }} }}
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

for _ in range(20):
    size, left, dur = random.randint(2, 5), random.randint(0, 100), random.randint(3, 8)
    st.markdown(f'<div class="star" style="width:{size}px; height:{size}px; left:{left}%; animation-duration:{dur}s;"></div>', unsafe_allow_html=True)

st.title("🧠 MASTER BRAIN V15: ULTIMATE 9-ENGINE")

# --- 4. KONTROL GRADASI ---
c_t1, c_t2, c_t3 = st.columns(3)
with c_t1: p_t1 = st.selectbox("Gradasi Tabel 1:", list(gradien_options.keys()), index=0)
with c_t2: p_t2 = st.selectbox("Gradasi Tabel 2:", list(gradien_options.keys()), index=1)
with c_t3: p_t3 = st.selectbox("Gradasi Tabel 3:", list(gradien_options.keys()), index=2)
g1, g2, g3 = gradien_options[p_t1], gradien_options[p_t2], gradien_options[p_t3]

# --- 5. FILTER & INPUT ---
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

# --- 6. ENGINE ANALISA: SUPER POWER (BOBOT MOMENTUM +5.0) ---
def get_predictions(data, mode, filter_mode):
    if not data: return []
    cols = [[] for _ in range(4)]
    all_rows = []
    for item in data:
        chars = [c for c in item if c.isdigit()]
        if len(chars) >= 4:
            all_rows.append([int(x) for x in chars[:4]])
            for i in range(4): cols[i].append(chars[i])
    
    results = []
    last_row = all_rows[-1] if all_rows else [None]*4
    
    for i in range(4):
        d = cols[i]
        if not d: continue
        last_digit = d[-1]
        all_digits = [str(x) for x in range(10)]
        
        def hitung_skor_9_cara(angka):
            skor = 0.0
            total_n = len(d)
            a_int = int(angka)
            
            # 1. Frekuensi
            skor += d.count(angka) * 0.5 
            # 2. Momentum Terkini (BOBOT BARU: +5.0)
            skor += d[-3:].count(angka) * 5.0
            
            # 3. Siklus (BOBOT: +7.0)
            indices = [idx for idx, x in enumerate(d) if x == angka]
            if len(indices) > 1:
                avg_gap = (indices[-1] - indices[0]) / (len(indices) - 1)
                if abs((total_n - indices[-1]) - avg_gap) <= 1: skor += 7.0
            
            # 4. Pairing
            for row in all_rows[-15:]:
                if a_int in row: skor += 1.0 
            
            # 5. Trend/Velocity
            if total_n >= 5:
                vel = int(d[-1]) - int(d[-5])
                if (vel > 0 and a_int > int(d[-1])) or (vel < 0 and a_int < int(d[-1])): skor += 3.0

            # 6. Distance Power
            try: skor += (list(reversed(d)).index(angka) * 1.5)
            except ValueError: skor += 12.0
            
            # 7. Adjacent (BOBOT: +8.0)
            for j in range(total_n - 1):
                if d[j] == last_digit and d[j+1] == angka: skor += 8.0
            
            # 8. Dynamic Balance (Ganjil/Genap & Besar/Kecil)
            p_p = [int(x)%2 for x in d[-10:]]; skor += 3.5 if p_p.count(a_int % 2) < 5 else 0
            p_s = [1 if int(x)>=5 else 0 for x in d[-10:]]; skor += 3.5 if p_s.count(1 if a_int>=5 else 0) < 5 else 0
            
            # 9. Cluster & Stock Logic
            if last_digit == angka: skor += 3.0 if d[-15:].count(last_digit) < 2 else -1.5
            if a_int in last_row: skor -= 4.0 # Depletion Logic
            
            return skor

        scored = sorted(all_digits, key=hitung_skor_9_cara, reverse=True)
        if filter_mode == "Ganjil": filtered = [x for x in scored if int(x)%2!=0]
        elif filter_mode == "Genap": filtered = [x for x in scored if int(x)%2==0]
        elif filter_mode == "Kecil (0-4)": filtered = [x for x in scored if int(x)<=4]
        elif filter_mode == "Besar (5-9)": filtered = [x for x in scored if int(x)>=5]
        else: filtered = scored

        if mode == "seimbang": results.append(filtered[1:7]) 
        elif mode == "akurat": results.append(filtered[:6])  
        else: results.append(filtered[::-1][:8])            
    return results

# --- 7. DISPLAY TABEL (UTUH) ---
if st.session_state.history:
    st.markdown("---")
    tabs_conf = [("🍀 TABEL SEIMBANG", "seimbang", g1), ("🔥 TABEL AKURAT", "akurat", g2), ("❄️ TABEL KONTRA", "kontra", g3)]
    for title, mode, grad in tabs_conf:
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
                html += "</tr>"
            st.markdown(html + "</table>", unsafe_allow_html=True)
