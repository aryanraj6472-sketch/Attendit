from datetime import datetime
import streamlit as st


def inject_styles() -> None:
    """Injects dark-mode CSS, glowing search bar, custom audio recorder capsule, and phone styling."""
    st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');

    #MainMenu, footer, header {visibility: hidden;}
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #090D16;
        color: #F8FAFC;
    }
    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 1.5rem;
        max-width: 1150px;
    }

    /* Glowing Dark Search Bar */
    div[data-testid="stTextInput"] input {
        background-color: #111827 !important;
        color: #F8FAFC !important;
        border: 1.5px solid rgba(0, 245, 212, 0.35) !important;
        border-radius: 12px !important;
        padding: 10px 14px !important;
        box-shadow: 0 2px 14px rgba(0, 245, 212, 0.08) !important;
        transition: all 0.2s ease !important;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: #00F5D4 !important;
        box-shadow: 0 0 0 3px rgba(0, 245, 212, 0.22) !important;
    }

    /* --- CUSTOM STYLED AUDIO RECORDER CAPSULE --- */
    div[data-testid="stAudioInput"] {
        background: linear-gradient(145deg, #0D1424, #090D16) !important;
        border: 1.5px solid rgba(0, 245, 212, 0.32) !important;
        border-radius: 16px !important;
        padding: 10px 16px !important;
        box-shadow: 0 6px 24px rgba(0, 245, 212, 0.08), inset 0 0 18px rgba(0, 245, 212, 0.04) !important;
        transition: border-color 0.25s ease, box-shadow 0.25s ease !important;
    }
    div[data-testid="stAudioInput"]:hover {
        border-color: #00F5D4 !important;
        box-shadow: 0 8px 28px rgba(0, 245, 212, 0.16) !important;
    }
    div[data-testid="stAudioInput"] > div {
        background: transparent !important;
    }
    div[data-testid="stAudioInput"] button {
        background: rgba(0, 245, 212, 0.14) !important;
        border: 1px solid rgba(0, 245, 212, 0.45) !important;
        color: #00F5D4 !important;
        border-radius: 50% !important;
        transition: transform 0.15s ease, background 0.15s ease !important;
    }
    div[data-testid="stAudioInput"] button:hover {
        background: #00F5D4 !important;
        color: #090D16 !important;
        transform: scale(1.06);
    }
    div[data-testid="stAudioInput"] span,
    div[data-testid="stAudioInput"] p {
        font-family: 'JetBrains Mono', monospace !important;
        color: #00F5D4 !important;
        font-weight: 700 !important;
    }

    /* --- ANIMATION 1: RADAR SONAR RINGS (FOR VERIFY TAB) --- */
    @keyframes sonar-ping {
        0% { transform: scale(0.75); opacity: 0.85; }
        100% { transform: scale(1.75); opacity: 0; }
    }
    .verify-rec-card {
        background: linear-gradient(145deg, #111827, #0B1120);
        border: 1px solid rgba(0, 245, 212, 0.3);
        border-radius: 16px;
        padding: 16px 20px;
        margin: 10px 0 10px 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .sonar-wrapper {
        position: relative;
        width: 42px;
        height: 42px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .sonar-ring {
        position: absolute;
        width: 34px;
        height: 34px;
        border-radius: 50%;
        border: 2px solid #00F5D4;
        animation: sonar-ping 2.2s cubic-bezier(0.2, 0.6, 0.3, 1) infinite;
    }
    .sonar-ring-delay {
        animation-delay: 1.1s;
    }
    .sonar-core {
        width: 28px;
        height: 28px;
        border-radius: 50%;
        background: rgba(0, 245, 212, 0.18);
        border: 1.5px solid #00F5D4;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 13px;
        z-index: 2;
    }

    /* --- ANIMATION 2: LASER BEAM SCANNER (FOR ENROLL TAB) --- */
    @keyframes beam-glide {
        0% { top: 8%; opacity: 0.3; }
        50% { top: 84%; opacity: 1; }
        100% { top: 8%; opacity: 0.3; }
    }
    .enroll-rec-card {
        position: relative;
        overflow: hidden;
        background: linear-gradient(145deg, #131B2E, #0B1120);
        border: 1px solid rgba(168, 85, 247, 0.4);
        border-radius: 16px;
        padding: 16px 20px;
        margin: 10px 0 10px 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .scanner-beam {
        position: absolute;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, #A855F7, #38BDF8, transparent);
        box-shadow: 0 0 10px #A855F7;
        animation: beam-glide 2.8s ease-in-out infinite;
        pointer-events: none;
    }
    .enroll-pill {
        background: rgba(168, 85, 247, 0.18);
        border: 1px solid rgba(168, 85, 247, 0.5);
        color: #E9D5FF;
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 999px;
    }

    /* Primary Button */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #00F5D4 0%, #38BDF8 100%);
        color: #090D16;
        font-weight: 800;
        border: none;
        border-radius: 12px;
    }

    /* Compact Right-Panel Smartphone */
    .phone-frame {
        width: 255px;
        margin: 0 auto;
        background: #1E293B;
        border: 3px solid #334155;
        border-radius: 32px;
        padding: 10px;
        box-shadow: 0 18px 40px rgba(0, 0, 0, 0.55);
    }
    .phone-inner {
        background: #090D16;
        border-radius: 23px;
        padding: 12px 14px 16px 14px;
        min-height: 390px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        border: 1px solid rgba(255, 255, 255, 0.06);
    }
    .phone-notch {
        width: 74px;
        height: 16px;
        background: #020617;
        border-radius: 999px;
        margin: 0 auto 10px auto;
    }
    .phone-id-card {
        background: linear-gradient(135deg, #132A4A 0%, #0F172A 100%);
        border: 1px solid rgba(0, 245, 212, 0.35);
        border-radius: 14px;
        padding: 11px 12px;
        margin: 8px 0;
    }
    .phone-alert-idle {
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 14px;
        padding: 11px 12px;
    }
    .phone-alert-ok {
        background: rgba(6, 78, 59, 0.65);
        border: 1px solid #10B981;
        border-radius: 14px;
        padding: 11px 12px;
    }
    .phone-alert-bad {
        background: rgba(127, 29, 29, 0.65);
        border: 1px solid #EF4444;
        border-radius: 14px;
        padding: 11px 12px;
    }
    .phone-bar {
        width: 85px;
        height: 4px;
        background: rgba(255, 255, 255, 0.3);
        border-radius: 99px;
        margin: 12px auto 0 auto;
    }
</style>
""", unsafe_allow_html=True)
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');

    #MainMenu, footer, header {visibility: hidden;}
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #090D16;
        color: #F8FAFC;
    }
    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 1.5rem;
        max-width: 1150px;
    }

    /* Glowing Dark Search Bar */
    div[data-testid="stTextInput"] input {
        background-color: #111827 !important;
        color: #F8FAFC !important;
        border: 1.5px solid rgba(0, 245, 212, 0.35) !important;
        border-radius: 12px !important;
        padding: 10px 14px !important;
        box-shadow: 0 2px 14px rgba(0, 245, 212, 0.08) !important;
        transition: all 0.2s ease !important;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: #00F5D4 !important;
        box-shadow: 0 0 0 3px rgba(0, 245, 212, 0.22) !important;
    }

    /* --- ANIMATION 1: RADAR SONAR RINGS (FOR VERIFY TAB) --- */
    @keyframes sonar-ping {
        0% { transform: scale(0.75); opacity: 0.85; }
        100% { transform: scale(1.75); opacity: 0; }
    }
    .verify-rec-card {
        background: linear-gradient(145deg, #111827, #0B1120);
        border: 1px solid rgba(0, 245, 212, 0.3);
        border-radius: 16px;
        padding: 16px 20px;
        margin: 10px 0 12px 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .sonar-wrapper {
        position: relative;
        width: 42px;
        height: 42px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .sonar-ring {
        position: absolute;
        width: 34px;
        height: 34px;
        border-radius: 50%;
        border: 2px solid #00F5D4;
        animation: sonar-ping 2.2s cubic-bezier(0.2, 0.6, 0.3, 1) infinite;
    }
    .sonar-ring-delay {
        animation-delay: 1.1s;
    }
    .sonar-core {
        width: 28px;
        height: 28px;
        border-radius: 50%;
        background: rgba(0, 245, 212, 0.18);
        border: 1.5px solid #00F5D4;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 13px;
        z-index: 2;
    }

    /* --- ANIMATION 2: LASER BEAM SCANNER (FOR ENROLL TAB) --- */
    @keyframes beam-glide {
        0% { top: 8%; opacity: 0.3; }
        50% { top: 84%; opacity: 1; }
        100% { top: 8%; opacity: 0.3; }
    }
    .enroll-rec-card {
        position: relative;
        overflow: hidden;
        background: linear-gradient(145deg, #131B2E, #0B1120);
        border: 1px solid rgba(168, 85, 247, 0.4);
        border-radius: 16px;
        padding: 16px 20px;
        margin: 10px 0 12px 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .scanner-beam {
        position: absolute;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, #A855F7, #38BDF8, transparent);
        box-shadow: 0 0 10px #A855F7;
        animation: beam-glide 2.8s ease-in-out infinite;
        pointer-events: none;
    }
    .enroll-pill {
        background: rgba(168, 85, 247, 0.18);
        border: 1px solid rgba(168, 85, 247, 0.5);
        color: #E9D5FF;
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 999px;
    }

    /* Primary Button */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #00F5D4 0%, #38BDF8 100%);
        color: #090D16;
        font-weight: 800;
        border: none;
        border-radius: 12px;
    }

    /* Compact Right-Panel Smartphone */
    .phone-frame {
        width: 255px;
        margin: 0 auto;
        background: #1E293B;
        border: 3px solid #334155;
        border-radius: 32px;
        padding: 10px;
        box-shadow: 0 18px 40px rgba(0, 0, 0, 0.55);
    }
    .phone-inner {
        background: #090D16;
        border-radius: 23px;
        padding: 12px 14px 16px 14px;
        min-height: 390px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        border: 1px solid rgba(255, 255, 255, 0.06);
    }
    .phone-notch {
        width: 74px;
        height: 16px;
        background: #020617;
        border-radius: 999px;
        margin: 0 auto 10px auto;
    }
    .phone-id-card {
        background: linear-gradient(135deg, #132A4A 0%, #0F172A 100%);
        border: 1px solid rgba(0, 245, 212, 0.35);
        border-radius: 14px;
        padding: 11px 12px;
        margin: 8px 0;
    }
    .phone-alert-idle {
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 14px;
        padding: 11px 12px;
    }
    .phone-alert-ok {
        background: rgba(6, 78, 59, 0.65);
        border: 1px solid #10B981;
        border-radius: 14px;
        padding: 11px 12px;
    }
    .phone-alert-bad {
        background: rgba(127, 29, 29, 0.65);
        border: 1px solid #EF4444;
        border-radius: 14px;
        padding: 11px 12px;
    }
    .phone-bar {
        width: 85px;
        height: 4px;
        background: rgba(255, 255, 255, 0.3);
        border-radius: 99px;
        margin: 12px auto 0 auto;
    }
</style>
""", unsafe_allow_html=True)


def render_top_header() -> str:
    """Renders the dark header and glowing search bar, returning the search query."""
    top_l, top_r = st.columns([1.3, 1.7])
    with top_l:
        st.markdown(
            '<h3 style="margin:0; color:#F8FAFC;">🎙️ VoicePass Gate</h3>'
            '<div style="font-size:12px; color:#94A3B8;">DetectifAI Eidos Biometrics • Track 02</div>',
            unsafe_allow_html=True,
        )
    with top_r:
        query = st.text_input(
            "Search",
            placeholder="🔍 Search Student ID or Voice Key...",
            label_visibility="collapsed",
        )
    st.divider()
    return query


def render_challenge_banner(phrase: str) -> None:
    """Renders the anti-replay challenge phrase box."""
    st.markdown(
        f'<div style="background:#111827; border-left:4px solid #00F5D4; padding:10px 14px; border-radius:8px; margin:6px 0;">'
        f'<div style="font-size:11px; color:#00F5D4; font-weight:700;">LIVE ANTI-REPLAY PHRASE (SPEAK THIS)</div>'
        f'<div style="color:#F8FAFC; font-size:14.5px; margin-top:2px;">“{phrase}”</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def render_verify_recorder_header() -> None:
    """Renders the Radar Sonar Ring recorder header for Tab 1 (Verify)."""
    st.markdown(
        '<div class="verify-rec-card">'
        '<div style="display:flex; align-items:center; gap:12px;">'
        '<div class="sonar-wrapper">'
        '<div class="sonar-ring"></div>'
        '<div class="sonar-ring sonar-ring-delay"></div>'
        '<div class="sonar-core">🎙️</div>'
        '</div>'
        '<div>'
        '<div style="color:#F8FAFC; font-weight:700; font-size:14px;">Sonar Voice Sensor</div>'
        '<div style="color:#94A3B8; font-size:12px;">Speak passphrase clearly (4–60s)</div>'
        '</div>'
        '</div>'
        '<span style="font-family:JetBrains Mono,monospace; font-size:11px; color:#00F5D4; border:1px solid rgba(0,245,212,0.4); padding:4px 10px; border-radius:999px;">● SONAR ACTIVE</span>'
        '</div>',
        unsafe_allow_html=True,
    )


def render_enroll_recorder_header() -> None:
    """Renders the Laser Beam Scanner recorder header for Tab 2 (Enroll)."""
    st.markdown(
        '<div class="enroll-rec-card">'
        '<div class="scanner-beam"></div>'
        '<div>'
        '<div style="color:#F8FAFC; font-weight:700; font-size:14px;">🧬 Biometric Voiceprint Scanner</div>'
        '<div style="color:#CBD5E1; font-size:12px;">Record 15–60s baseline speech to map vocal harmonics</div>'
        '</div>'
        '<span class="enroll-pill">● 15–60 SEC</span>'
        '</div>',
        unsafe_allow_html=True,
    )


def render_phone_companion(p_info: dict) -> None:
    """Renders the compact right-panel smartphone companion."""
    clock_now = datetime.now().strftime("%H:%M")

    if p_info["state"] == "verified":
        score_txt = f"Score: {p_info['score']:.3f}" if p_info["score"] is not None else "Backup PIN Used"
        notif_html = (
            f'<div class="phone-alert-ok">'
            f'<div style="font-size:10px; font-weight:800; color:#34D399;">✅ APPROVED • {p_info["time"]}</div>'
            f'<div style="font-size:13.5px; font-weight:700; color:#FFFFFF; margin:3px 0;">{p_info["action"]}</div>'
            f'<div style="font-size:11.5px; color:#D1FAE5;">ID: <b>{p_info["user"]}</b> • {score_txt}</div>'
            f'</div>'
        )
    elif p_info["state"] == "rejected":
        score_txt = f"Score: {p_info['score']:.3f} (<0.53)" if p_info["score"] is not None else "Mismatch"
        notif_html = (
            f'<div class="phone-alert-bad">'
            f'<div style="font-size:10px; font-weight:800; color:#F87171;">🚨 BLOCKED • {p_info["time"]}</div>'
            f'<div style="font-size:13.5px; font-weight:700; color:#FFFFFF; margin:3px 0;">Unauthorized Voice</div>'
            f'<div style="font-size:11.5px; color:#FECACA;">ID: <b>{p_info["user"]}</b> • {score_txt}</div>'
            f'</div>'
        )
    elif p_info["state"] == "enrolled":
        notif_html = (
            f'<div class="phone-alert-ok">'
            f'<div style="font-size:10px; font-weight:800; color:#38BDF8;">🧬 ENROLLED • {p_info["time"]}</div>'
            f'<div style="font-size:13.5px; font-weight:700; color:#FFFFFF; margin:3px 0;">Voice Key Ready</div>'
            f'<div style="font-size:11.5px; color:#E0F2FE;">Bound to: <b>{p_info["user"]}</b></div>'
            f'</div>'
        )
    else:
        notif_html = (
            '<div class="phone-alert-idle">'
            '<div style="font-size:10px; font-weight:700; color:#00F5D4;">📡 LIVE GATE SYNC</div>'
            '<div style="font-size:12px; color:#CBD5E1; margin-top:3px;">Ready. Scan voice on left to receive instant gate alerts.</div>'
            '</div>'
        )

    phone_html = (
        f'<div class="phone-frame">'
        f'<div class="phone-inner">'
        f'<div>'
        f'<div style="display:flex; justify-content:space-between; font-size:10px; color:#94A3B8; padding:0 4px;">'
        f'<span><b>{clock_now}</b></span><span>5G • 100%</span>'
        f'</div>'
        f'<div class="phone-notch"></div>'
        f'<div style="text-align:center; margin:6px 0 10px 0;">'
        f'<div style="font-size:10px; color:#00F5D4; font-weight:700; letter-spacing:0.8px;">VOICEPASS MOBILE</div>'
        f'<div style="font-size:16px; font-weight:800; color:#FFFFFF;">Campus & UPI Pass</div>'
        f'</div>'
        f'<div class="phone-id-card">'
        f'<div style="display:flex; justify-content:space-between; font-size:10px;">'
        f'<span style="color:#94A3B8;">ACTIVE KEY</span>'
        f'<span style="color:#34D399; font-weight:700;">● PROTECTED</span>'
        f'</div>'
        f'<div style="font-size:15px; font-weight:800; color:#FFFFFF; margin:3px 0;">{p_info["user"]}</div>'
        f'<div style="font-size:11px; color:#94A3B8;">CMRIT Lab & Payment Gate</div>'
        f'</div>'
        f'{notif_html}'
        f'</div>'
        f'<div>'
        f'<div style="text-align:center; font-size:10px; color:#64748B;">DetectifAI Eidos Biometrics</div>'
        f'<div class="phone-bar"></div>'
        f'</div>'
        f'</div>'
        f'</div>'
    )
    st.markdown(phone_html, unsafe_allow_html=True)