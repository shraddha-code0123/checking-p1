import streamlit as st
import hashlib

from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

st.set_page_config(
    page_title="CryptoToolkit | Shraddha Mandhare",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""<style>
.stApp { background-color: #0d1117; }
.main .block-container { padding-top: 1.5rem; }
section[data-testid="stSidebar"] { background-color: #161b22; border-right: 1px solid #30363d; }
section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] span { color: #c9d1d9; }
.stTabs [data-baseweb="tab-list"] { background: #161b22; border-bottom: 1px solid #30363d; }
.stTabs [data-baseweb="tab"] { color: #8b949e; font-family: monospace; font-size: 0.9em; }
.stTabs [aria-selected="true"] { background: #0d2818 !important; color: #00ff88 !important; border-bottom: 2px solid #00ff88 !important; }
.stButton > button { background: transparent; color: #00ff88; border: 1px solid #00ff88; font-family: monospace; border-radius: 6px; font-weight: 600; letter-spacing: 1px; transition: all 0.2s; }
.stButton > button:hover { background: #00ff88 !important; color: #0d1117 !important; }
.stTextInput input, .stTextArea textarea { background: #161b22 !important; border: 1px solid #30363d !important; color: #e6edf3 !important; font-family: monospace; }
.stTextInput input:focus, .stTextArea textarea:focus { border-color: #00ff88 !important; box-shadow: 0 0 0 2px rgba(0,255,136,0.1) !important; }
[data-testid="stMetric"] { background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 12px 16px; }
[data-testid="stMetricValue"] { color: #00ff88 !important; font-family: monospace; font-size: 1.1em !important; }
[data-testid="stMetricLabel"] { color: #8b949e !important; font-family: monospace; font-size: 0.75em !important; }
.stCodeBlock, [data-testid="stCodeBlock"] { border: 1px solid #30363d; border-radius: 6px; }
details { background: #161b22 !important; border: 1px solid #30363d !important; border-radius: 6px; }
details summary { color: #58a6ff !important; font-family: monospace; font-size: 0.85em; }
.stCaption p { color: #8b949e !important; font-family: monospace; font-size: 0.78em !important; }
.stSpinner p { color: #00ff88 !important; font-family: monospace; }
div[data-testid="stDecoration"] { display: none; }
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }
</style>""", unsafe_allow_html=True)

# ── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding:24px 10px 16px;">
        <div style="width:72px;height:72px;border-radius:50%;background:linear-gradient(135deg,#00ff88,#00b359);
            display:flex;align-items:center;justify-content:center;margin:0 auto 12px;
            font-size:1.5em;font-weight:700;color:#0d1117;font-family:monospace;
            box-shadow:0 0 20px rgba(0,255,136,0.3);">SM</div>
        <div style="color:#00ff88;font-size:1em;font-weight:700;font-family:monospace;letter-spacing:1px;">
            Shraddha Mandhare</div>
        <div style="color:#8b949e;font-size:0.78em;font-family:monospace;margin-top:4px;">
            Cybersecurity Intern</div>
        <div style="color:#484f58;font-size:0.75em;font-family:monospace;margin-top:2px;">
            Nowrosjee Wadia College</div>
        <div style="color:#484f58;font-size:0.73em;font-family:monospace;margin-top:1px;">
            Codect Technologies</div>
    </div>
    <hr style="border:none;border-top:1px solid #30363d;margin:4px 0 16px;">
    <div style="font-family:monospace;font-size:0.8em;color:#58a6ff;font-weight:700;margin-bottom:8px;padding:0 4px;">
        &gt; PROJECT INFO</div>
    <div style="background:#0d1117;border:1px solid #30363d;border-radius:6px;padding:12px;
        font-family:monospace;font-size:0.78em;color:#8b949e;line-height:1.9;margin-bottom:16px;">
        <span style="color:#00ff88">►</span> Project #6<br>
        <span style="color:#00ff88">►</span> Cryptography Implementation<br>
        <span style="color:#00ff88">►</span> Python + pycryptodome<br>
        <span style="color:#00ff88">►</span> Streamlit Web App
    </div>
    <div style="font-family:monospace;font-size:0.8em;color:#58a6ff;font-weight:700;margin-bottom:8px;padding:0 4px;">
        &gt; SKILLS COVERED</div>
    <div style="font-family:monospace;font-size:0.78em;line-height:2;padding:0 4px;">
        <span style="color:#00ff88">✓</span> <span style="color:#c9d1d9">Symmetric Encryption</span><br>
        <span style="color:#00ff88">✓</span> <span style="color:#c9d1d9">Asymmetric Encryption</span><br>
        <span style="color:#00ff88">✓</span> <span style="color:#c9d1d9">Hash Functions</span><br>
        <span style="color:#00ff88">✓</span> <span style="color:#c9d1d9">Key Generation</span><br>
        <span style="color:#00ff88">✓</span> <span style="color:#c9d1d9">IV &amp; Padding Schemes</span><br>
        <span style="color:#00ff88">✓</span> <span style="color:#c9d1d9">Avalanche Effect</span>
    </div>
    <hr style="border:none;border-top:1px solid #30363d;margin:16px 0 12px;">
    <div style="font-family:monospace;font-size:0.72em;color:#484f58;text-align:center;line-height:1.7;">
        Cybersecurity Internship 2025<br>© Shraddha Rajendra Mandhare</div>
    """, unsafe_allow_html=True)

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:#161b22;border:1px solid #30363d;border-top:3px solid #00ff88;
    border-radius:8px;padding:28px 32px;margin-bottom:24px;">
    <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;">
        <div>
            <div style="color:#00ff88;font-size:1.8em;font-weight:700;font-family:monospace;
                letter-spacing:2px;text-shadow:0 0 30px rgba(0,255,136,0.3);">
                🔐 CRYPTOGRAPHY TOOLKIT</div>
            <div style="color:#8b949e;font-family:monospace;font-size:0.82em;margin-top:6px;">
                AES-256 · RSA-2048 · SHA Hashing — built from scratch in Python</div>
        </div>
        <div style="text-align:right;">
            <div style="color:#484f58;font-family:monospace;font-size:0.72em;">BY</div>
            <div style="color:#e6edf3;font-family:monospace;font-size:0.85em;font-weight:600;">
                Shraddha Rajendra Mandhare</div>
            <div style="color:#484f58;font-family:monospace;font-size:0.72em;">
                Nowrosjee Wadia College</div>
        </div>
    </div>
    <div style="margin-top:16px;display:flex;gap:8px;flex-wrap:wrap;">
        <span style="background:#0d2818;color:#00ff88;border:1px solid #00ff88;border-radius:20px;
            padding:3px 12px;font-size:0.72em;font-family:monospace;">Python 3</span>
        <span style="background:#0d2818;color:#00ff88;border:1px solid #00ff88;border-radius:20px;
            padding:3px 12px;font-size:0.72em;font-family:monospace;">pycryptodome</span>
        <span style="background:#0d2818;color:#00ff88;border:1px solid #00ff88;border-radius:20px;
            padding:3px 12px;font-size:0.72em;font-family:monospace;">Streamlit</span>
        <span style="background:#0d2818;color:#00ff88;border:1px solid #00ff88;border-radius:20px;
            padding:3px 12px;font-size:0.72em;font-family:monospace;">AES-256-CBC</span>
        <span style="background:#0d2818;color:#00ff88;border:1px solid #00ff88;border-radius:20px;
            padding:3px 12px;font-size:0.72em;font-family:monospace;">RSA-2048-OAEP</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["  🔒  AES Encryption  ", "  🗝️  RSA Encryption  ", "  #  SHA Hashing  "])

# ── TAB 1: AES ────────────────────────────────────────────────────────────────
with tab1:
    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown("""
        <div style="background:#161b22;border:1px solid #30363d;border-left:3px solid #00ff88;
            border-radius:6px;padding:16px;margin-bottom:12px;">
            <div style="color:#00ff88;font-family:monospace;font-weight:700;font-size:0.82em;
                margin-bottom:10px;letter-spacing:1px;">// AES-256 — SYMMETRIC ENCRYPTION</div>
            <div style="color:#8b949e;font-size:0.82em;line-height:1.8;font-family:monospace;">
                AES uses the <span style="color:#e6edf3">same key</span> to encrypt and decrypt.
                It works on 16-byte blocks using <span style="color:#e6edf3">CBC mode</span> 
                where each block is chained to the previous, hiding patterns.
            </div>
        </div>
        <div style="background:#161b22;border:1px solid #30363d;border-radius:6px;padding:16px;">
            <div style="color:#58a6ff;font-family:monospace;font-size:0.78em;font-weight:700;
                margin-bottom:10px;letter-spacing:1px;">EXECUTION STEPS</div>
            <div style="font-family:monospace;font-size:0.78em;color:#8b949e;line-height:2;">
                <span style="color:#00ff88;margin-right:8px;">①</span>Generate random 256-bit key<br>
                <span style="color:#00ff88;margin-right:8px;">②</span>Generate random 128-bit IV<br>
                <span style="color:#00ff88;margin-right:8px;">③</span>Pad plaintext to block boundary<br>
                <span style="color:#00ff88;margin-right:8px;">④</span>Encrypt with AES-CBC<br>
                <span style="color:#00ff88;margin-right:8px;">⑤</span>Decrypt using same key + IV<br>
                <span style="color:#00ff88;margin-right:8px;">⑥</span>Verify plaintext matches
            </div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown("<div style='color:#484f58;font-family:monospace;font-size:0.78em;margin-bottom:4px;'>// INPUT PLAINTEXT</div>", unsafe_allow_html=True)
        message = st.text_area("aes_input", value="Shraddha's confidential message — AES-256 protected!", height=90, label_visibility="collapsed")
        
        clicked = st.button("▶  EXECUTE ENCRYPTION", key="aes_btn", use_container_width=True)
        if clicked:
            key = get_random_bytes(32)
            enc = AES.new(key, AES.MODE_CBC)
            iv = enc.iv
            ct = enc.encrypt(pad(message.encode(), AES.block_size))
            dec = AES.new(key, AES.MODE_CBC, iv=iv)
            pt = unpad(dec.decrypt(ct), AES.block_size).decode()

            c1, c2, c3 = st.columns(3)
            c1.metric("KEY SIZE", "256 bit")
            c2.metric("MODE", "CBC")
            c3.metric("STATUS", "✓ OK")

            st.markdown(f"""
            <div style="background:#010409;border:1px solid #30363d;border-radius:6px;
                padding:16px;font-family:monospace;font-size:0.76em;line-height:2.1;margin-top:12px;">
                <span style="color:#484f58">SECRET KEY  </span><span style="color:#58a6ff">{key.hex()[:32]}…</span><br>
                <span style="color:#484f58">IV          </span><span style="color:#f78166">{iv.hex()}</span><br>
                <span style="color:#484f58">CIPHERTEXT  </span><span style="color:#e6edf3">{ct.hex()[:40]}…</span><br>
                <span style="color:#484f58">DECRYPTED   </span><span style="color:#00ff88">{pt}</span>
            </div>
            """, unsafe_allow_html=True)

            if pt == message:
                st.success("✓  Round-trip verified — encryption & decryption matched")

# ── TAB 2: RSA ────────────────────────────────────────────────────────────────
with tab2:
    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown("""
        <div style="background:#161b22;border:1px solid #30363d;border-left:3px solid #58a6ff;
            border-radius:6px;padding:16px;margin-bottom:12px;">
            <div style="color:#58a6ff;font-family:monospace;font-weight:700;font-size:0.82em;
                margin-bottom:10px;letter-spacing:1px;">// RSA-2048 — ASYMMETRIC ENCRYPTION</div>
            <div style="color:#8b949e;font-size:0.82em;line-height:1.8;font-family:monospace;">
                RSA uses mathematically-linked key pairs. The 
                <span style="color:#58a6ff">public key</span> encrypts data; 
                only the <span style="color:#f78166">private key</span> can decrypt it.
                Basis of all HTTPS on the internet.
            </div>
        </div>
        <div style="background:#161b22;border:1px solid #30363d;border-radius:6px;padding:16px;">
            <div style="color:#58a6ff;font-family:monospace;font-size:0.78em;font-weight:700;
                margin-bottom:10px;letter-spacing:1px;">KEY PAIR MODEL</div>
            <div style="font-family:monospace;font-size:0.78em;color:#8b949e;line-height:2;">
                <span style="color:#58a6ff">PUBLIC KEY </span> → share freely<br>
                               → encrypts data<br>
                <span style="color:#f78166">PRIVATE KEY</span> → never reveal<br>
                               → only key that decrypts<br><br>
                <span style="color:#484f58">// padding scheme: OAEP + SHA-1</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown("<div style='color:#484f58;font-family:monospace;font-size:0.78em;margin-bottom:4px;'>// SHORT MESSAGE TO ENCRYPT (RSA limit ~200 bytes)</div>", unsafe_allow_html=True)
        rsa_msg = st.text_input("rsa_input", value="Classified intel — RSA-2048 secured by Shraddha", label_visibility="collapsed")
        st.markdown("<div style='color:#484f58;font-family:monospace;font-size:0.72em;margin-bottom:6px;'>// generating a 2048-bit key pair takes ~1-2 sec</div>", unsafe_allow_html=True)

        if st.button("▶  GENERATE KEYS & ENCRYPT", key="rsa_btn", use_container_width=True):
            with st.spinner("Generating RSA-2048 key pair…"):
                rsa_key = RSA.generate(2048)
                pub = rsa_key.publickey()
                ct = PKCS1_OAEP.new(pub).encrypt(rsa_msg.encode())
                pt = PKCS1_OAEP.new(rsa_key).decrypt(ct).decode()

            c1, c2, c3 = st.columns(3)
            c1.metric("KEY SIZE", "2048 bit")
            c2.metric("PADDING", "OAEP")
            c3.metric("STATUS", "✓ OK")

            st.markdown(f"""
            <div style="background:#010409;border:1px solid #30363d;border-radius:6px;
                padding:16px;font-family:monospace;font-size:0.76em;line-height:2.1;margin-top:12px;">
                <span style="color:#484f58">CIPHERTEXT  </span><span style="color:#e6edf3">{ct.hex()[:48]}…</span><br>
                <span style="color:#484f58">DECRYPTED   </span><span style="color:#00ff88">{pt}</span>
            </div>
            """, unsafe_allow_html=True)

            st.success("✓  RSA encryption and decryption successful")
            col1, col2 = st.columns(2)
            with col1:
                with st.expander("🔓 Public Key"):
                    st.code(pub.export_key().decode(), language="text")
            with col2:
                with st.expander("🔒 Private Key"):
                    st.code(rsa_key.export_key().decode()[:400] + "\n...(truncated)", language="text")

# ── TAB 3: SHA ────────────────────────────────────────────────────────────────
with tab3:
    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown("""
        <div style="background:#161b22;border:1px solid #30363d;border-left:3px solid #f78166;
            border-radius:6px;padding:16px;margin-bottom:12px;">
            <div style="color:#f78166;font-family:monospace;font-weight:700;font-size:0.82em;
                margin-bottom:10px;letter-spacing:1px;">// SHA — ONE-WAY HASH FUNCTIONS</div>
            <div style="color:#8b949e;font-size:0.82em;line-height:1.8;font-family:monospace;">
                A hash is <span style="color:#e6edf3">irreversible</span> — 
                you can never recover the original input. Used for password storage, 
                file integrity checks, and digital signatures.
            </div>
        </div>
        <div style="background:#161b22;border:1px solid #30363d;border-radius:6px;padding:16px;">
            <div style="color:#58a6ff;font-family:monospace;font-size:0.78em;font-weight:700;
                margin-bottom:10px;letter-spacing:1px;">ALGORITHM COMPARISON</div>
            <div style="font-family:monospace;font-size:0.78em;color:#8b949e;line-height:2.1;">
                <span style="color:#f78166">MD5    </span> 128-bit  <span style="color:#484f58">// broken, avoid</span><br>
                <span style="color:#f78166">SHA-1  </span> 160-bit  <span style="color:#484f58">// deprecated</span><br>
                <span style="color:#00ff88">SHA-256</span> 256-bit  <span style="color:#484f58">// industry standard</span><br>
                <span style="color:#00ff88">SHA-512</span> 512-bit  <span style="color:#484f58">// highest security</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown("<div style='color:#484f58;font-family:monospace;font-size:0.78em;margin-bottom:4px;'>// ENTER ANY TEXT TO HASH</div>", unsafe_allow_html=True)
        text = st.text_input("sha_input", value="ShraddhaMandhare@WadiaCollege2025", label_visibility="collapsed")

        if text:
            for algo, color in [("md5","#f78166"),("sha1","#f78166"),("sha256","#00ff88"),("sha512","#00ff88")]:
                h = hashlib.new(algo, text.encode()).hexdigest()
                st.markdown(f"""
                <div style="background:#010409;border:1px solid #30363d;border-left:3px solid {color};
                    border-radius:4px;padding:9px 12px;font-family:monospace;font-size:0.74em;margin:5px 0;">
                    <span style="color:{color};font-weight:700">{algo.upper().ljust(7)}</span>
                    <span style="color:#e6edf3;word-break:break-all;">{h}</span>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("""<div style="color:#8b949e;font-family:monospace;font-size:0.78em;
                margin-top:14px;margin-bottom:6px;">// AVALANCHE EFFECT DEMO</div>""", unsafe_allow_html=True)
            h1 = hashlib.sha256(text.encode()).hexdigest()
            h2 = hashlib.sha256((text + "!").encode()).hexdigest()
            st.markdown(f"""
            <div style="background:#010409;border:1px solid #30363d;border-radius:6px;
                padding:12px;font-family:monospace;font-size:0.74em;line-height:2.1;">
                <span style="color:#484f58">ORIGINAL  </span><span style="color:#00ff88">{h1}</span><br>
                <span style="color:#484f58">+ '!' char </span><span style="color:#f78166">{h2}</span>
            </div>
            """, unsafe_allow_html=True)
            changed = sum(a != b for a, b in zip(h1, h2))
            st.metric("Hex chars changed from adding just one '!'", f"{changed} out of {len(h1)}")

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;color:#484f58;font-family:monospace;font-size:0.72em;
    border-top:1px solid #21262d;padding-top:20px;margin-top:48px;line-height:2;">
    <span style="color:#30363d">━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</span><br>
    Shraddha Rajendra Mandhare &nbsp;·&nbsp; Nowrosjee Wadia College &nbsp;·&nbsp;
    Codect Technologies Cybersecurity Internship 2025<br>
    <span style="color:#21262d">Project #6 — Cryptography Algorithms Implementation</span>
</div>
""", unsafe_allow_html=True)
