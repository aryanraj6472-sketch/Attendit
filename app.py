import re
import streamlit as st
from eidos_client import enroll_speaker, verify_speaker, list_speakers
from storage import load_logs, add_log

st.set_page_config(page_title="VoicePass — Voice as a Key", page_icon="🎙️", layout="centered")
st.title("🎙️ VoicePass — Spoken Attendance & Payment Gate")
st.caption("Powered by DetectifAI Eidos Speaker Verification | Track 02: Voice as a Key")

if "known_speakers" not in st.session_state:
    st.session_state["known_speakers"] = ["test"]

tab_enroll, tab_verify, tab_logs = st.tabs([
    "1. Enroll Voiceprint",
    "2. Verify & Unlock",
    "3. Audit & Attendance Log"
])

# --- TAB 1: ENROLLMENT ---
with tab_enroll:
    st.subheader("Register a New User")
    st.write("Record a clear **15–60 second** voice sample (at least 10s of speech) to create a voice key.")
    raw_name = st.text_input("Speaker ID / Student ID (letters, numbers, _ . : - only, e.g., Aryan_26IS140)")
    enroll_audio = st.audio_input("Record Enrollment Voice (15–60s)", key="enroll_mic")
    if not enroll_audio:
        enroll_audio = st.file_uploader("Or upload enrollment audio", type=["wav", "mp3", "m4a"], key="enroll_up")

    if st.button("Create Voice Key", type="primary"):
        clean_id = re.sub(r"[^a-zA-Z0-9_.:-]", "_", raw_name.strip())
        if not clean_id or not enroll_audio:
            st.warning("Enter an ID and record/upload 15–60 seconds of audio.")
        else:
            with st.spinner(f"Enrolling '{clean_id}' with DetectifAI Eidos..."):
                try:
                    res = enroll_speaker(clean_id, enroll_audio.getvalue(), enroll_audio.name)
                    if clean_id not in st.session_state["known_speakers"]:
                        st.session_state["known_speakers"].append(clean_id)
                    st.success(f"✅ Voice key created for **{clean_id}**! Switch to Tab 2 to verify.")
                    with st.expander("Technical Details (API Response)", expanded=False):
                        st.json(res)
                except Exception as e:
                    st.error(f"Enrollment failed: {e}")

# --- TAB 2: VERIFICATION ---
with tab_verify:
    st.subheader("Verify Identity (Attendance / Payment Approval)")
    api_ids = []
    try:
        speakers_res = list_speakers()
        raw_list = []
        if isinstance(speakers_res, list):
            raw_list = speakers_res
        elif isinstance(speakers_res, dict):
            for key in ("speakers", "data", "items", "results"):
                if isinstance(speakers_res.get(key), list):
                    raw_list = speakers_res[key]
                    break
        for s in raw_list:
            sid = s.get("speaker_id") or s.get("id") if isinstance(s, dict) else str(s)
            if sid:
                api_ids.append(sid)
    except Exception:
        pass

    all_speakers = list(dict.fromkeys(api_ids + st.session_state["known_speakers"]))

    selected_id = st.selectbox("Select Claimed Identity", all_speakers)
    action_type = st.radio(
        "Action to Authorize",
        ["Mark Lab/Hostel Attendance", "Approve ₹10,000 Payment"],
        horizontal=True
    )
    verify_audio = st.audio_input("Speak Passphrase to Verify (4–60s)", key="verify_mic")
    if not verify_audio:
        verify_audio = st.file_uploader("Or upload verification clip", type=["wav", "mp3", "m4a"], key="verify_up")

    if verify_audio and st.button("Verify Voice", type="primary"):
        with st.spinner("Matching voiceprint with Eidos..."):
            try:
                payload = verify_speaker(selected_id, verify_audio.getvalue(), verify_audio.name)
                res_data = payload.get("result", {})
                decision = str(res_data.get("decision", "")).lower()
                similarity = res_data.get("similarity")
                threshold = res_data.get("threshold", 0.53)

                if similarity is not None:
                    st.metric(
                        label="Voice Similarity Score (Not a Percentage)",
                        value=f"{similarity:.3f}",
                        delta=f"{similarity - threshold:+.3f} vs {threshold} threshold"
                    )

                if decision == "match":
                    st.success(f"✅ Identity Verified! **{action_type}** authorized for **{selected_id}**.")
                    add_log(selected_id, selected_id, "VERIFIED", payload)
                else:
                    st.error("🚨 Voice Mismatch! Access denied. Please use your backup PIN/OTP.")
                    add_log(selected_id, selected_id, "REJECTED", payload)

                with st.expander("Technical Details (Raw Eidos Evidence)", expanded=False):
                    st.json(payload)

                st.info("**Rule 03 Notice:** Similarity scores serve as biometric evidence, not absolute proof. Require a backup PIN/OTP if verification fails or falls near the threshold.")
            except Exception as e:
                st.error(f"Verification request failed: {e}")

# --- TAB 3: AUDIT LOGS ---
with tab_logs:
    st.subheader("Live Verification & Attendance Log")
    logs = load_logs()
    if not logs:
        st.write("No verification attempts recorded yet.")
    else:
        for entry in logs:
            badge = "🟢" if entry["status"] == "VERIFIED" else "🔴"
            st.markdown(f"{badge} **{entry['timestamp']}** — `{entry['name']}` → **{entry['status']}**")