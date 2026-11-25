import random
import re
from datetime import datetime
import streamlit as st
from eidos_client import enroll_speaker, verify_speaker, list_speakers
from storage import add_log
from frontend import (
    inject_styles,
    render_top_header,
    render_challenge_banner,
    render_verify_recorder_header,
    render_enroll_recorder_header,
    render_phone_companion,
)

st.set_page_config(
    page_title="VoicePass — Biometric Gate",
    page_icon="🎙️",
    layout="wide",
)

inject_styles()

CHALLENGES = [
    "My voice is my key — unlock lab gate Delta-904.",
    "Confirm CMRIT attendance token Sierra-318.",
    "Approve ₹10,000 transfer under voiceprint Echo-752.",
    "Verify campus access code Omega-621.",
]

if "known_speakers" not in st.session_state:
    st.session_state["known_speakers"] = ["test"]
if "challenge" not in st.session_state:
    st.session_state["challenge"] = CHALLENGES[0]
if "pin_required" not in st.session_state:
    st.session_state["pin_required"] = False
if "phone_status" not in st.session_state:
    st.session_state["phone_status"] = {
        "state": "idle",
        "user": "test",
        "action": "Mark Lab Attendance",
        "score": None,
        "time": datetime.now().strftime("%I:%M %p"),
    }

search_query = render_top_header()

# Load speakers
api_ids = []
try:
    speakers_res = list_speakers()
    raw_list = speakers_res if isinstance(speakers_res, list) else next(
        (speakers_res[k] for k in ("speakers", "data", "items", "results") if isinstance(speakers_res.get(k), list)),
        [],
    )
    for s in raw_list:
        sid = s.get("speaker_id") or s.get("id") if isinstance(s, dict) else str(s)
        if sid:
            api_ids.append(sid)
except Exception:
    pass

all_speakers = list(dict.fromkeys(api_ids + st.session_state["known_speakers"]))
if search_query.strip():
    filtered = [s for s in all_speakers if search_query.strip().lower() in s.lower()]
    if filtered:
        all_speakers = filtered

left_col, right_col = st.columns([1.65, 1], gap="large")

with left_col:
    tab_verify, tab_enroll = st.tabs([
        "🔐 Verify & Unlock",
        "🧬 Enroll Voice Key",
    ])

    # --- TAB 1: VERIFY & UNLOCK (LIVE MIC ONLY) ---
    with tab_verify:
        c1, c2 = st.columns(2)
        with c1:
            selected_id = st.selectbox("Claimed Identity", all_speakers)
        with c2:
            action_type = st.selectbox("Protected Action", ["Mark Lab Attendance", "Approve ₹10,000 Payment"])

        p1, p2 = st.columns([3.5, 1])
        with p1:
            render_challenge_banner(st.session_state["challenge"])
        with p2:
            st.write("")
            if st.button("🎲 New", help="Generate a new anti-replay sentence", use_container_width=True):
                st.session_state["challenge"] = random.choice(CHALLENGES)
                st.rerun()

        render_verify_recorder_header()
        verify_audio = st.audio_input("Record Spoken Passphrase", key="verify_mic", label_visibility="collapsed")

        if verify_audio and st.button("Authenticate Voice", type="primary", use_container_width=True):
            with st.spinner("Verifying voiceprint with DetectifAI Eidos..."):
                try:
                    payload = verify_speaker(selected_id, verify_audio.getvalue(), verify_audio.name)
                    res_data = payload.get("result", {})
                    similarity = float(res_data.get("similarity", 0.0))
                    threshold = float(res_data.get("threshold", 0.53))
                    matched = (str(res_data.get("decision", "")).lower() == "match") and (similarity >= threshold)

                    m1, m2, m3 = st.columns(3)
                    m1.metric("Similarity Score", f"{similarity:.3f}")
                    m2.metric("Gate Threshold", f"{threshold:.2f}")
                    m3.metric("Margin", f"{similarity - threshold:+.3f}")
                    st.progress(min(max(similarity, 0.0), 1.0))

                    now_str = datetime.now().strftime("%I:%M %p")
                    if matched:
                        st.session_state["pin_required"] = False
                        st.session_state["phone_status"] = {
                            "state": "verified",
                            "user": selected_id,
                            "action": action_type,
                            "score": similarity,
                            "time": now_str,
                        }
                        st.success(f"✅ Identity Verified! **{action_type}** authorized for **{selected_id}**.")
                        add_log(selected_id, selected_id, "VERIFIED", payload)
                    else:
                        st.session_state["pin_required"] = True
                        st.session_state["phone_status"] = {
                            "state": "rejected",
                            "user": selected_id,
                            "action": action_type,
                            "score": similarity,
                            "time": now_str,
                        }
                        st.error("🚨 Voice Mismatch! Access blocked. Enter backup PIN below.")
                        add_log(selected_id, selected_id, "REJECTED", payload)

                    with st.expander("Raw Eidos API Evidence", expanded=False):
                        st.json(payload)
                except Exception as e:
                    st.error(f"Verification failed: {e}")

        if st.session_state["pin_required"]:
            with st.container(border=True):
                st.markdown("#### 🔢 Rule 03 Backup PIN Fallback")
                pin_c1, pin_c2 = st.columns([2, 1])
                with pin_c1:
                    pin_code = st.text_input("Enter 4-Digit Backup PIN (Demo: 2614)", type="password", max_chars=4)
                with pin_c2:
                    st.write("")
                    if st.button("Unlock", use_container_width=True):
                        if pin_code == "2614":
                            st.session_state["pin_required"] = False
                            st.session_state["phone_status"] = {
                                "state": "verified",
                                "user": selected_id,
                                "action": f"{action_type} (PIN)",
                                "score": None,
                                "time": datetime.now().strftime("%I:%M %p"),
                            }
                            add_log(selected_id, selected_id, "VERIFIED", {"method": "backup_pin"})
                            st.rerun()
                        else:
                            st.error("Incorrect PIN.")

    # --- TAB 2: ENROLL VOICE KEY (LIVE MIC + FILE UPLOAD) ---
    with tab_enroll:
        st.subheader("Register New Voice Key")
        raw_name = st.text_input("Speaker / Student ID", placeholder="e.g., Aryan_26IS140")
        render_enroll_recorder_header()
        enroll_audio = st.audio_input("Record Enrollment Voice", key="enroll_mic", label_visibility="collapsed")
        if not enroll_audio:
            enroll_audio = st.file_uploader(
                "Or upload enrollment audio (.wav, .mp3, .m4a)",
                type=["wav", "mp3", "m4a"],
                key="enroll_up",
            )

        if st.button("Create Biometric Voice Key", type="primary", use_container_width=True):
            clean_id = re.sub(r"[^a-zA-Z0-9_.:-]", "_", raw_name.strip())
            if not clean_id or not enroll_audio:
                st.warning("Enter an ID and record or upload 15–60 seconds of audio.")
            else:
                with st.spinner(f"Enrolling '{clean_id}' with Eidos..."):
                    try:
                        res = enroll_speaker(clean_id, enroll_audio.getvalue(), enroll_audio.name)
                        if clean_id not in st.session_state["known_speakers"]:
                            st.session_state["known_speakers"].append(clean_id)
                        st.session_state["phone_status"] = {
                            "state": "enrolled",
                            "user": clean_id,
                            "action": "New Voice Key Created",
                            "score": None,
                            "time": datetime.now().strftime("%I:%M %p"),
                        }
                        st.success(f"✅ Enrolled **{clean_id}**! Switch to Tab 1 to verify.")
                        with st.expander("Enrollment Details", expanded=False):
                            st.json(res)
                    except Exception as e:
                        st.error(f"Enrollment failed: {e}")

with right_col:
    render_phone_companion(st.session_state["phone_status"])