import os
import uuid
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("DETECTIF_API_KEY")
BASE_URL = "https://platform.detectif.ai/v1"


def _headers() -> dict:
    if not API_KEY:
        raise ValueError("Missing DETECTIF_API_KEY in .env file.")
    return {
        "Authorization": f"Bearer {API_KEY}",
        "Idempotency-Key": str(uuid.uuid4()),
    }


def _raise_with_detail(response: requests.Response) -> None:
    if not response.ok:
        raise RuntimeError(f"HTTP {response.status_code}: {response.text}")


def enroll_speaker(speaker_id: str, audio_bytes: bytes, filename: str = "enroll.wav") -> dict:
    """Registers a new speaker voiceprint (requires 15-60s audio)."""
    files = {"file": (filename, audio_bytes, "audio/wav")}
    data = {"speaker_id": speaker_id}
    response = requests.post(
        f"{BASE_URL}/speakers/enroll",
        headers=_headers(),
        data=data,
        files=files,
        timeout=30,
    )
    _raise_with_detail(response)
    return response.json()


def verify_speaker(speaker_id: str, audio_bytes: bytes, filename: str = "verify.wav") -> dict:
    """Verifies a new audio clip (requires 3-60s audio) against speaker_id."""
    files = {"file": (filename, audio_bytes, "audio/wav")}
    data = {"speaker_id": speaker_id}
    response = requests.post(
        f"{BASE_URL}/speakers/verify",
        headers=_headers(),
        data=data,
        files=files,
        timeout=30,
    )
    _raise_with_detail(response)
    return response.json()


def list_speakers() -> dict:
    """Fetches all speakers enrolled under your DetectifAI account."""
    response = requests.get(
        f"{BASE_URL}/speakers",
        headers={"Authorization": f"Bearer {API_KEY}"},
        timeout=30,
    )
    _raise_with_detail(response)
    return response.json()