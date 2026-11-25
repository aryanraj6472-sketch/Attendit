<div align="center">

# 🎙️ VoicePass
### *Your Voice is Your Password.*

[![Track](https://img.shields.io/badge/Track_02-Voice_as_a_Key-ff4b4b?style=for-the-badge)](https://platform.detectif.ai)
[![Powered By](https://img.shields.io/badge/DetectifAI-Eidos_Speaker_Verification-111827?style=for-the-badge)](https://platform.detectif.ai)
[![Built With](https://img.shields.io/badge/Python-Streamlit-00a8e8?style=for-the-badge&logo=python&logoColor=white)](https://streamlit.io)

**A spoken biometric gate for proxy-proof college attendance and high-value payment approvals.**  
*Built in 48 hours for the **CMRIT x DetectifAI Hackathon**.*

</div>

---

## 🚨 The Problem
ID cards get borrowed. PINs get shoulder-surfed. OTPs get forwarded.  
Whether it is **proxy attendance in college labs/hostels** or **unauthorized high-value UPI/account transfers**, traditional keys verify *what you hold*—not *who you are*.

## 💡 The Solution: VoicePass
**VoicePass** turns a person's natural vocal fingerprint into a zero-friction security key powered by **DetectifAI's Eidos** speaker verification model. Speak a quick passphrase, and VoicePass verifies your vocal biometrics in milliseconds before unlocking access.

```text
  [1. ENROLL]  ──►  15–60s Baseline Voiceprint  ──►  Stored in DetectifAI Eidos
                                                                │
  [2. VERIFY]  ──►  4–60s Live Spoken Passphrase ──►  Compare vs. 0.53 Threshold
                                                                │
                    ┌───────────────────────────────────────────┴───────────────────────────────────────────┐
                    ▼                                                                                       ▼
        🟢 Similarity ≥ 0.53 (MATCH)                                                            🔴 Similarity < 0.53 (MISMATCH)
   ✅ Attendance Marked / Payment Approved                                                 🚨 Access Blocked + Backup OTP/PIN