import re
import streamlit as st
from eidos_client import enroll_speaker, verify_speaker, list_speakers
from storage import load_logs, add_log

st.set_page_config(page_title="VoicePass — Voice as a Key", page_icon="🎙️", layout="centered")
st.title("🎙️ VoicePass — Spoken Attendance & Payment Gate")
st.caption("Powered by DetectifAI Eidos Speaker Verification | Track 02: Voice as a Key")

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
                    st.success(f"Enrolled **{clean_id}** successfully!")
                    st.json(res)
                except Exception as e:
                    st.error(f"Enrollment failed: {e}")

# --- TAB 2: VERIFICATION ---
with tab_verify:
    st.subheader("Verify Identity (Attendance / Payment Approval)")
    try:
        speakers_res = list_speakers()
        speakers = speakers_res.get("speakers", speakers_res if isinstance(speakers_res, list) else [])
    except Exception as e:
        speakers = []
        st.error(f"Could not fetch enrolled speakers: {e}")

    if not speakers:
        st.info("No speakers enrolled yet. Go to Tab 1 to enroll your voice first.")
    else:
        speaker_ids = [
            s.get("speaker_id", s.get("id")) if isinstance(s, dict) else str(s)
            for s in speakers
        ]
        selected_id = st.selectbox("Select Claimed Identity", speaker_ids)

        action_type = st.radio("Action to Authorize", ["Mark Lab/Hostel Attendance", "Approve ₹10,000 Payment"], horizontal=True)
        verify_audio = st.audio_input("Speak Passphrase to Verify (3–60s)", key="verify_mic")
        if not verify_audio:
            verify_audio = st.file_uploader("Or upload verification clip", type=["wav", "mp3", "m4a"], key="verify_up")

        if verify_audio and st.button("Verify Voice", type="primary"):
            with st.spinner("Matching voiceprint with Eidos..."):
                try:
                    result = verify_speaker(selected_id, verify_audio.getvalue(), verify_audio.name)
                    matched = result.get("match") or result.get("verified") or (result.get("verdict") == "match")

                    if matched:
                        st.success(f"✅ Identity Verified! **{action_type}** authorized for {selected_id}.")
                        add_log(selected_id, selected_id, "VERIFIED", result)
                    else:
                        st.error("🚨 Voice Mismatch! Access denied.")
                        add_log(selected_id, selected_id, "REJECTED", result)

                    with st.expander("View Raw Eidos API Evidence"):
                        st.json(result)

                    st.info("**Rule 03 Notice:** Voice match scores serve as biometric evidence, not absolute proof. Require a backup PIN/OTP if verification fails.")
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