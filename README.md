<div align="center">

# 🎙️ VoicePass
### *Your Voice is Your Password.*

[![Track](https://img.shields.io/badge/Track_02-Voice_as_a_Key-00F5D4?style=for-the-badge&labelColor=090D16)](https://platform.detectif.ai)
[![Engine](https://img.shields.io/badge/DetectifAI-Eidos_Speaker_Verification-38BDF8?style=for-the-badge&labelColor=090D16)](https://platform.detectif.ai)
[![Stack](https://img.shields.io/badge/Python-Streamlit-A855F7?style=for-the-badge&logo=python&logoColor=white&labelColor=090D16)](https://streamlit.io)

**A spoken biometric security gate for proxy-proof lab attendance and high-value payment approvals.**  
*Built at **CMR Institute of Technology (CMRIT), Bengaluru** for the **DetectifAI Hackathon**.*

</div>

---

## 🚨 The Problem
Student IDs get borrowed for proxy attendance. PINs get shoulder-surfed. OTPs get forwarded.  
Traditional authentication checks *what you hold*—not *who you are*.

## 💡 The Solution: VoicePass
**VoicePass** turns your natural vocal signature into an unborrowable key powered by **DetectifAI's Eidos** speaker verification API. Speak a randomized one-time challenge phrase into the live microphone, and VoicePass scores your vocal biometrics against a `0.53` decision threshold before unlocking access and pushing a real-time alert to the synced mobile pass view.

```text
  [1. ENROLL]    ──►  15–60s Baseline Voiceprint  ──►  Stored in DetectifAI Eidos
                                                                  │
  [2. CHALLENGE] ──►  Randomized Anti-Replay Phrase (prevents pre-recorded spoofing)
                                                                  │
  [3. VERIFY]    ──►  4–60s Live Mic Capture      ──►  Compare vs. 0.53 Threshold
                                                                  │
                      ┌───────────────────────────────────────────┴───────────────────────────────────────────┐
                      ▼                                                                                       ▼
          🟢 Similarity ≥ 0.53 (MATCH)                                                            🔴 Similarity < 0.53 (MISMATCH)
     ✅ Attendance Marked / Payment Approved                                                 🚨 Access Blocked + Backup PIN (Rule 03)
     📱 Live Approved Alert on Mobile Pass                                                   📱 Live Security Alert on Mobile Pass