# Feature Specification: Voice Processing & Streaming Pipeline
## Enterprise Multilingual Speech-to-Text, Voice Activity Detection & Audio Streaming

---

### Feature Metadata
- **Feature ID:** SPEC-001-VOICE
- **Feature Owner:** Member 1 (Conversation & Requirements Lead)
- **Status:** APPROVED & LOCKED
- **Target Release:** Milestone M0 (Spike) / Milestone M2 (Production Integration)

---

## 1. Feature Description & Scope

The Voice Pipeline is the primary conversational ingestion interface for Voice-to-Website AI. It provides non-technical shop owners with an intuitive, hands-free experience allowing them to describe their website and modifications using natural speech in Urdu, English, or mixed bilingual code-switching ("Urdish").

### Scope:
- In-browser microphone audio capture via standard MediaStream / AudioWorklet API.
- Client-side Voice Activity Detection (VAD) and silence detection.
- Audio normalization, format validation, and secure S3 archival.
- Bilingual Speech-to-Text (STT) inference using Whisper large-v3-turbo with domain-specific prompting.
- Mandatory editable transcript confirmation modal.
- Text-to-Speech (TTS) audio streaming response playback using Edge-TTS / ElevenLabs.

---

## 2. Technical Architecture & Audio Data Flow

```
┌──────────────────┐       Web Audio API        ┌───────────────────────┐
│ Browser Client   │ ─────────────────────────► │ WebRTC / Silero VAD   │
│ Microphone (Mic) │ (Linear PCM 16kHz / Opus)  │ (Noise Gate & Silence)│
└──────────────────┘                            └───────────┬───────────┘
                                                            │
                                                            ▼ Valid Audio Frame
                                                ┌───────────────────────┐
                                                │ FastAPI Audio Ingest  │
                                                │ (/api/v1/voice/upload)│
                                                └─────┬───────────┬─────┘
                                                      │           │
                              Raw WebM/WAV Stream     ▼           ▼ Background Upload
                                      ┌──────────────────┐   ┌──────────────────┐
                                      │ Whisper ASR      │   │ AWS S3 / MinIO   │
                                      │ (GPU / Serverless│   │ Audio Archive    │
                                      └────────┬─────────┘   └──────────────────┘
                                               │
                                               ▼ Transcribed Text + Tokens
                                      ┌──────────────────┐
                                      │ Transcript Modal │
                                      │ (Human Confirms) │
                                      └────────┬─────────┘
                                               │ Verified Prompt
                                               ▼
                                      ┌──────────────────┐
                                      │ LangGraph Engine │
                                      └──────────────────┘
```

---

## 3. Detailed Component Specifications

### 3.1 Audio Ingestion & Format Normalization
- **Sample Rate:** 16,000 Hz (16 kHz), 16-bit Mono channel Linear PCM.
- **Client Container:** Opus inside WebM (browser standard), converted to uncompressed 16kHz WAV on server ingest via `ffmpeg-python` or `librosa`.
- **Validation Constraints:**
  - Minimum Duration: 1.0 second (rejects accidental clicks).
  - Maximum Duration: 120.0 seconds per voice note.
  - Maximum File Size: 15 MB.
  - Audio Level Check: RMS energy $> -45\text{ dBFS}$ (rejects completely silent files).

### 3.2 Voice Activity Detection (VAD)
- **Engine:** Silero VAD v5 / WebRTC VAD.
- **Sensitivity:** Threshold set to 0.5 probability of speech.
- **Silence Window:** Automatic speech termination trigger after 1,800 ms of continuous silence.

### 3.3 Bilingual Whisper ASR Inference
- **Model:** Whisper Large-v3-Turbo (or OpenAI Whisper API).
- **Prompt Engineering for ASR:** To combat phonetic confusion between Pakistani names, Urdu ecommerce vocabulary, and English web terminology, the Whisper model is primed with a bilingual domain prompt:
  ```text
  "The following is a conversation with a Pakistani shop owner discussing an ecommerce website. Terminology includes: dukaan, kapra, jora, khussa, shalwar kameez, add to cart, checkout, delivery charges, cash on delivery (COD), header, banner, catalog, contact number, WhatsApp button, Lahore, Karachi, Islamabad."
  ```
- **Language Detection:** Whisper auto-detects `ur` (Urdu) or `en` (English). If Urdu is detected, Arabic-script Urdu is extracted alongside a normalized Roman Urdu transcription.

### 3.4 Text-to-Speech (TTS) Feedback
- **Engine:** Edge-TTS (`ur-PK-AsadNeural` for Urdu, `en-US-ChristopherNeural` for English) / ElevenLabs.
- **Streaming:** Chunks streamed via WebSocket directly to client AudioContext for minimal perceived response latency ($<600\text{ ms}$).

---

## 4. Latency Budget Allocation

| Step | Operation | Target Latency | P95 Latency |
|---|---|---|---|
| 1 | Client Audio Recording & VAD Stop | 0 ms | 0 ms |
| 2 | WebSocket / HTTP Chunk Upload to FastAPI | 150 ms | 350 ms |
| 3 | Audio Conversion & Normalization (FFmpeg) | 120 ms | 250 ms |
| 4 | Whisper Large-v3-Turbo ASR Inference (GPU) | 650 ms | 1,200 ms |
| 5 | Network Return to Browser & Modal Display | 100 ms | 200 ms |
| **Total** | **End-to-End Voice-to-Transcript Display** | **1,020 ms** | **2,000 ms** |

---

## 5. API Contracts

### 5.1 POST `/api/v1/voice/transcribe`
- **Request:** `multipart/form-data`
  - `audio_file`: Binary file (WebM / WAV)
  - `project_id`: UUID
  - `language_hint`: Optional string (`"ur"`, `"en"`, `"auto"`)
- **Response Schema:**
```json
{
  "status": "success",
  "transcription_id": "8f3b2e71-9c1a-4d2b-9831-2c0f681a9412",
  "raw_text": "Mujhe apni kapray ki dukaan ke liye aik modern website banani hai jisme WhatsApp order button ho.",
  "language_detected": "ur",
  "confidence_score": 0.964,
  "duration_seconds": 5.4,
  "audio_s3_key": "audio/proj_123/msg_456.webm",
  "requires_confirmation": true
}
```

---

## 6. Testing & Acceptance Criteria

### Unit Tests
- `test_audio_validation_rejects_empty_file`: Asserts HTTP 400 when audio energy is below $-45\text{ dBFS}$.
- `test_audio_conversion_16khz`: Asserts FFmpeg converts varying sample rates to exact 16kHz mono PCM.
- `test_vad_detection_bounds`: Verifies Silero VAD correctly segments speech from leading/trailing silence.

### Integration Tests
- `test_whisper_urdu_transcription`: Validates Word Error Rate (WER) $\le 12\%$ on 30 benchmark Pakistani audio clips.
- `test_s3_audio_persistence`: Asserts binary audio exists in S3 bucket with correct metadata tags.

### Manual Acceptance Checklist
1. Click microphone in browser on mobile Chrome and desktop Safari.
2. Speak in conversational Urdu: "Hero image par 20% discount likh do".
3. Verify transcript modal appears in $<2$ seconds displaying correct text.
4. Edit one word in the transcript modal and click "Confirm".
5. Verify confirmed edited text is transmitted to LangGraph state machine.
