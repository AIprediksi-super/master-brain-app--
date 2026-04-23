import streamlit as st
from collections import Counter
import random

# --- CONFIG UI ---
st.set_page_config(page_title="Master Brain v15: 9-Engine Scoring", layout="wide")

if 'history' not in st.session_state:
    st.session_state.history = []

# --- TEMA & CSS ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: white; }
    .predict-table { width: 100%; border-collapse: separate; border-spacing: 5px; }
    .predict-table td { 
        border-radius: 12px; padding: 15px; text-align: center; font-size: 32px; font-weight: 900; 
        color: white !important; -webkit-text-stroke: 1.5px black;
        text-shadow: 0 0 15px rgba(255,255,255,0.7), 3px 3px 5px #000;
        box-shadow: inset 0 0 10px rgba(0,0,0,0.5); background: linear-gradient(135deg, #56ab2f 0%, #a8e063 100%);
    }
    textarea { color: #FFFFFF !important; font-weight: bold !important; background: rgba(0,0,0,0.4) !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🧠 MASTER BRAIN V15: 9-ENGINE SCORING")

# --- UI CONTROL ---
st.subheader("🛠️ FILTER & INPUT")
p_filter = st.radio("Saring hasil angka:", ["Semua", "Ganjil", "Genap", "Kecil (0-4)", "Besar (5-9)"], horizontal=True)
manual_input = st.text_area("Tempel Data 4-Digit:", height=150, placeholder="Tempel histori di sini...")

# --- ENGINE ANALISA: 9 KRITERIA ---
def get_predictions(data, mode, filter_mode):
    if not data: return []
    
    # Pisahkan data per kolom
    cols = [[] for _ in range(4)]
    all_rows = []
    for item in data:
        chars = [c for c in item if c.isdigit()]
        if len(chars) >= 4:
            all_rows.append(chars[:4])
            for i in range(4): cols[i].append(chars[i])
    
    if not cols[0]: return []

    results = []
    for i in range(4):
        d = cols[i]
        last_digit = d[-1]
        all_digits = [str(x) for x in range(10)]
        
        def hitung_skor_9_cara(angka):
            skor = 0
            # 1. FREKUENSI (Banyak/Sedikit)
            skor += d.count(angka) * 1.0
            
            # 2. RECENCY (Kehangatan di 5 data terakhir)
            skor += d[-5:].count(angka) * 2.0
            
            # 3. INTERVAL (Jarak kemunculan rata-rata)
            indices = [idx for idx, x in enumerate(d) if x == angka]
            if len(indices) > 1:
                intervals = [indices[j] - indices[j-1] for j in range(1, len(indices))]
                avg_int = sum(intervals) / len(intervals)
                skor += (10 / avg_int) if avg_int > 0 else 0
            
            # 4. PAIRING (Kaitan dengan kolom lain di baris yang sama)
            for row in all_rows:
                if angka in row: skor += 0.2
            
            # 5. TREND (Kenaikan frekuensi di 10 data terakhir)
            skor += d[-10:].count(angka) * 1.5
            
            # 6. DISTANCE (Lama absen sejak muncul terakhir)
            try:
                jarak_absen = list(reversed(d)).index(angka)
                skor += jarak_absen * 0.5 
            except ValueError: skor += 15
            
            # 7. ADJACENT (Sering muncul setelah angka terakhir di kolom ini)
            for j in range(len(d)-1):
                if d[j] == last_digit and d[j+1] == angka: skor += 3.0
                
            # 8. SUM/AVERAGE (Keseimbangan nilai rata-rata kolom)
            avg_kolom = sum(int(x) for x in d[-15:]) / 15 if len(d) >= 15 else 4.5
            if avg_kolom < 4.5 and int(angka) >= 5: skor += 2.5
            if avg_kolom > 4.5 and int(angka) <= 4: skor += 2.5
            
            # 9. CLUSTER (Kecenderungan angka kembar/berdekatan)
            if last_digit == angka: skor += 2.0
            
            return skor

        # Hitung skor untuk semua angka 0-9
        scored_list = sorted(all_digits, key=hitung_skor_9_cara, reverse=True)
        
        # Terapkan FILTER (Ganjil/Genap/Besar/Kecil)
        if filter_mode == "Ganjil": filtered = [x for x in scored_list if int(x) % 2 != 0]
        elif filter_mode == "Genap": filtered = [x for x in scored_list if int(x) % 2 == 0]
        elif filter_mode == "Kecil (0-4)": filtered = [x for x in scored_list if int(x) <= 4]
        elif filter_mode == "Besar (5-9)": filtered = [x for x in scored_list if int(x) >= 5]
        else: filtered = scored_list

        # Mode Output
        if mode == "seimbang": results.append(filtered[1:9])
        elif mode == "akurat": results.append(filtered[:8])
        else: results.append(filtered[::-1][:8])
            
    return results

# --- ACTION BUTTON ---
if st.button("🚀 JALANKAN ANALISA 9-ENGINE"):
    if manual_input:
        st.session_state.history = manual_input.replace(',', ' ').split()

# --- DISPLAY ---
if st.session_state.history:
    st.markdown("---")
    for title, mode in [("🍀 TABEL SEIMBANG", "seimbang"), ("🔥 TABEL AKURAT", "akurat"), ("❄️ TABEL KONTRA", "kontra")]:
        st.subheader(title)
        res = get_predictions(st.session_state.history, mode, p_filter)
        if res:
            html = "<table class='predict-table'><tr><th>RANK</th><th>KOL 1</th><th>KOL 2</th><th>KOL 3</th><th>KOL 4</th></tr>"
            for r in range(len(res[0])):
                html += f"<tr><td style='font-size:12px; background:rgba(0,0,0,0.5); text-stroke:0;'>#{r+1}</td>"
                for c in range(4):
                    val = res[c][r] if r < len(res[c]) else "-"
                    html += f"<td>{val}</td>"
                html += "</tr>"
            st.markdown(html + "</table>", unsafe_allow_html=True)
