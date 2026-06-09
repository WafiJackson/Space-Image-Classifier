# pyrefly: ignore [missing-import]
import streamlit as st
import requests
import time

# ──────────────────────────────────────────────────────────────
# Page Configuration
# ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🌌 Space Image Classifier",
    page_icon="🔭",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────
# Custom CSS – Premium Space Theme
# ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Font ─────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');

/* ── Root Variables ──────────────────────────────────────── */
:root {
    --bg-primary: #0a0e1a;
    --bg-card: rgba(15, 23, 42, 0.65);
    --bg-card-hover: rgba(30, 41, 72, 0.7);
    --accent-blue: #6366f1;
    --accent-purple: #a855f7;
    --accent-cyan: #22d3ee;
    --accent-pink: #ec4899;
    --text-primary: #f1f5f9;
    --text-secondary: #94a3b8;
    --border-glass: rgba(148, 163, 184, 0.12);
    --glow-purple: rgba(168, 85, 247, 0.35);
    --glow-blue: rgba(99, 102, 241, 0.35);
}

/* ── Hide default Streamlit elements ─────────────────────── */
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}

/* ── Body / Background ───────────────────────────────────── */
.stApp {
    background: linear-gradient(145deg, #0a0e1a 0%, #111827 40%, #1e1b4b 70%, #0f172a 100%);
    background-attachment: fixed;
    font-family: 'Inter', sans-serif;
}

/* ── Twinkling Stars Overlay ─────────────────────────────── */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        radial-gradient(1px 1px at 10% 20%, rgba(255,255,255,0.7) 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 25% 55%, rgba(255,255,255,0.5) 0%, transparent 100%),
        radial-gradient(1px 1px at 40% 15%, rgba(255,255,255,0.6) 0%, transparent 100%),
        radial-gradient(1.2px 1.2px at 55% 75%, rgba(255,255,255,0.4) 0%, transparent 100%),
        radial-gradient(1px 1px at 70% 35%, rgba(255,255,255,0.55) 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 85% 60%, rgba(255,255,255,0.45) 0%, transparent 100%),
        radial-gradient(1px 1px at 15% 80%, rgba(255,255,255,0.5) 0%, transparent 100%),
        radial-gradient(1.3px 1.3px at 60% 45%, rgba(255,255,255,0.6) 0%, transparent 100%),
        radial-gradient(1px 1px at 90% 10%, rgba(255,255,255,0.5) 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 35% 90%, rgba(255,255,255,0.4) 0%, transparent 100%),
        radial-gradient(1px 1px at 78% 82%, rgba(255,255,255,0.55) 0%, transparent 100%),
        radial-gradient(1.2px 1.2px at 5% 50%, rgba(255,255,255,0.45) 0%, transparent 100%);
    pointer-events: none;
    z-index: 0;
    animation: twinkle 4s ease-in-out infinite alternate;
}
@keyframes twinkle {
    0%   { opacity: 0.6; }
    50%  { opacity: 1;   }
    100% { opacity: 0.7; }
}

/* ── Sidebar ─────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1e1b4b 100%) !important;
    border-right: 1px solid var(--border-glass);
}
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] .stMarkdown li,
section[data-testid="stSidebar"] .stMarkdown h1,
section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] .stMarkdown h3 {
    color: var(--text-primary) !important;
}

/* ── Glass Card ──────────────────────────────────────────── */
.glass-card {
    background: var(--bg-card);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid var(--border-glass);
    border-radius: 20px;
    padding: 2rem 2.2rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    transition: transform 0.25s ease, box-shadow 0.25s ease;
}
.glass-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 40px rgba(99, 102, 241, 0.15);
}

/* ── Hero Title ──────────────────────────────────────────── */
.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #6366f1 0%, #a855f7 40%, #22d3ee 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-align: center;
    margin-bottom: 0.3rem;
    letter-spacing: -0.5px;
}
.hero-subtitle {
    text-align: center;
    color: var(--text-secondary);
    font-size: 1.05rem;
    font-weight: 400;
    margin-bottom: 1.5rem;
    line-height: 1.6;
}

/* ── Divider Glow ────────────────────────────────────────── */
.glow-divider {
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--accent-blue), var(--accent-purple), var(--accent-cyan), transparent);
    border: none;
    margin: 1rem 0 1.8rem 0;
    border-radius: 2px;
}

/* ── File Uploader ───────────────────────────────────────── */
section[data-testid="stFileUploader"] {
    background: var(--bg-card);
    border: 2px dashed rgba(99, 102, 241, 0.35);
    border-radius: 16px;
    padding: 1rem;
    transition: border-color 0.3s ease, background 0.3s ease;
}
section[data-testid="stFileUploader"]:hover {
    border-color: var(--accent-purple);
    background: var(--bg-card-hover);
}

/* ── Buttons ─────────────────────────────────────────────── */
.stButton > button {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 0.75rem 2.5rem !important;
    font-size: 1.05rem !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    letter-spacing: 0.3px;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.35) !important;
    width: 100%;
}
.stButton > button:hover {
    transform: translateY(-2px) scale(1.01) !important;
    box-shadow: 0 8px 25px rgba(139, 92, 246, 0.5) !important;
}
.stButton > button:active {
    transform: translateY(0px) scale(0.99) !important;
}

/* ── Result Cards ────────────────────────────────────────── */
.result-card {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(168, 85, 247, 0.1) 100%);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(99, 102, 241, 0.25);
    border-radius: 18px;
    padding: 2rem;
    text-align: center;
    animation: fadeSlideUp 0.6s ease-out;
}
@keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0);    }
}

.result-label {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    background: linear-gradient(135deg, #22d3ee, #6366f1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0.5rem 0;
}
.result-confidence {
    font-size: 1.1rem;
    color: var(--text-secondary);
    margin-top: 0.25rem;
}

/* ── Confidence Bar ──────────────────────────────────────── */
.conf-bar-bg {
    background: rgba(30, 41, 59, 0.7);
    border-radius: 12px;
    height: 28px;
    overflow: hidden;
    margin-top: 1rem;
    border: 1px solid var(--border-glass);
}
.conf-bar-fill {
    height: 100%;
    border-radius: 12px;
    background: linear-gradient(90deg, #6366f1, #a855f7, #22d3ee);
    background-size: 200% 100%;
    animation: gradientShift 2s ease infinite;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    padding-right: 12px;
    font-weight: 700;
    font-size: 0.85rem;
    color: white;
    text-shadow: 0 1px 4px rgba(0,0,0,0.4);
    transition: width 1s cubic-bezier(0.4, 0, 0.2, 1);
}
@keyframes gradientShift {
    0%   { background-position: 0% 50%;   }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%;   }
}

/* ── Metric Stat Chips ───────────────────────────────────── */
.stat-chip {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(99, 102, 241, 0.12);
    border: 1px solid rgba(99, 102, 241, 0.2);
    border-radius: 99px;
    padding: 0.4rem 1rem;
    font-size: 0.9rem;
    color: var(--text-primary);
    font-weight: 500;
}

/* ── Image Container ─────────────────────────────────────── */
.stImage {
    border-radius: 16px;
    overflow: hidden;
    border: 1px solid var(--border-glass);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
}
.stImage img {
    border-radius: 16px;
}

/* ── Success / Error Alerts ──────────────────────────────── */
.stAlert {
    border-radius: 14px !important;
    backdrop-filter: blur(8px);
}

/* ── Spinner ─────────────────────────────────────────────── */
.stSpinner > div {
    border-top-color: var(--accent-purple) !important;
}

/* ── Global text colour fix ──────────────────────────────── */
.stMarkdown, .stMarkdown p, .stMarkdown li {
    color: var(--text-primary);
}
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
# Class → Icon mapping
# ──────────────────────────────────────────────────────────────
CLASS_ICONS = {
    "constellation": "✨",
    "cosmos space": "🌀",
    "galaxies": "🌌",
    "nebula": "🔮",
    "planets": "🪐",
    "stars": "⭐",
}

CLASS_DESCRIPTIONS = {
    "constellation": "Pola bintang yang membentuk rasi di langit malam.",
    "cosmos space": "Pemandangan luas dari ruang angkasa kosmik.",
    "galaxies": "Kumpulan bintang, gas, dan debu yang terikat gravitasi.",
    "nebula": "Awan gas dan debu antarbintang yang bercahaya.",
    "planets": "Benda langit yang mengorbit bintang.",
    "stars": "Bola plasma raksasa yang memancarkan cahaya.",
}

# ──────────────────────────────────────────────────────────────
# Sidebar
# ──────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔭 Tentang Aplikasi")
    st.markdown(
        "Aplikasi ini menggunakan model **Deep Learning (CNN)** "
        "untuk mengklasifikasikan gambar benda langit ke dalam 6 kategori."
    )
    st.markdown("---")
    st.markdown("### 🪐 Kategori yang Didukung")
    for cls, icon in CLASS_ICONS.items():
        st.markdown(f"&nbsp;&nbsp;{icon}&ensp;**{cls.title()}**")

    st.markdown("---")
    st.markdown("### ⚙️ Tech Stack")
    st.markdown(
        "- 🐍 Python & TensorFlow\n"
        "- ⚡ FastAPI Backend\n"
        "- 🎨 Streamlit Frontend"
    )
    st.markdown("---")
    st.markdown(
        "<p style='text-align:center; color:#64748b; font-size:0.8rem;'>"
        "Praktikum Machine Learning — UAS<br>"
        "Semester 6 · 2026</p>",
        unsafe_allow_html=True,
    )

# ──────────────────────────────────────────────────────────────
# Hero Header
# ──────────────────────────────────────────────────────────────
st.markdown('<h1 class="hero-title">🌌 Space Image Classifier</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="hero-subtitle">'
    'Unggah gambar benda langit dan biarkan AI mengidentifikasinya dalam hitungan detik.'
    '</p>',
    unsafe_allow_html=True,
)
st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
# Upload Section
# ──────────────────────────────────────────────────────────────
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown("#### 📤 Unggah Gambar")
st.markdown(
    '<span style="color:#94a3b8; font-size:0.9rem;">'
    'Format yang didukung: JPG, JPEG, PNG'
    '</span>',
    unsafe_allow_html=True,
)

uploaded_file = st.file_uploader(
    "Upload gambar benda langit",
    type=["jpg", "jpeg", "png"],
    label_visibility="collapsed",
)
st.markdown('</div>', unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
# Preview + Classify
# ──────────────────────────────────────────────────────────────
if uploaded_file is not None:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("#### 🖼️ Preview Gambar")
    st.image(uploaded_file, caption="Gambar yang diunggah", width="stretch")
    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        classify_btn = st.button("🚀  Klasifikasikan Sekarang", use_container_width=True)

    if classify_btn:
        with st.spinner("🔍 Menganalisis gambar..."):
            files = {"file": uploaded_file.getvalue()}
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/predict/",
                    files=files,
                    timeout=30,
                )
            except requests.exceptions.ConnectionError:
                st.error("❌ Tidak dapat terhubung ke API Backend. Pastikan server FastAPI berjalan di port 8000.")
                st.stop()
            except requests.exceptions.Timeout:
                st.error("⏱️ Request timeout. Silakan coba lagi.")
                st.stop()

        if response.status_code == 200:
            result = response.json()
            label_asli = result["label"]
            akurasi = result["confidence"] * 100
            icon = CLASS_ICONS.get(label_asli, "🔭")
            description = CLASS_DESCRIPTIONS.get(label_asli, "")

            # ── Result Card ──────────────────────────────────
            st.markdown("---")
            st.markdown(
                f"""
                <div class="result-card">
                    <p style="font-size:3rem; margin:0;">{icon}</p>
                    <p class="result-label">{label_asli.title()}</p>
                    <p class="result-confidence">{description}</p>
                    <div class="conf-bar-bg">
                        <div class="conf-bar-fill" style="width:{akurasi:.1f}%;">{akurasi:.2f}%</div>
                    </div>
                    <p style="color:#64748b; font-size:0.8rem; margin-top:0.6rem;">Confidence Score</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # ── Detail Metrics ───────────────────────────────
            st.markdown("")
            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric(label="🏷️ Kelas", value=label_asli.title())
            with m2:
                st.metric(label="📊 Confidence", value=f"{akurasi:.2f}%")
            with m3:
                level = "Tinggi" if akurasi >= 80 else "Sedang" if akurasi >= 50 else "Rendah"
                st.metric(label="🎯 Tingkat Keyakinan", value=level)

            st.success("✅ Analisis berhasil diselesaikan!")

        else:
            st.error(
                "❌ Terjadi kesalahan saat menghubungi API Backend. "
                f"Status code: {response.status_code}"
            )

# ──────────────────────────────────────────────────────────────
# Footer
# ──────────────────────────────────────────────────────────────
st.markdown("")
st.markdown("")
st.markdown(
    """
    <div style="text-align:center; padding:2rem 0 1rem 0;">
        <div class="glow-divider"></div>
        <p style="color:#475569; font-size:0.85rem; margin-top:1rem;">
            Built with ❤️ using Streamlit & TensorFlow &ensp;·&ensp; Space Image Classifier v1.0
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)