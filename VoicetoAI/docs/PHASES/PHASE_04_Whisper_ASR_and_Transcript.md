# Phase 4: Bilingual Whisper ASR & Transcript Confirmation Engine

---

### Navigation
- **Current Phase:** Phase 4 of 20
- **Previous Phase:** [Phase 3: S3 Object Storage & Audio Validation Pipeline](file:///d:/VoicetoAI/docs/PHASES/PHASE_03_S3_Storage_and_Audio_Validation.md)
- **Next Phase:** [Phase 5: Voice Activity Detection (VAD) & Real-time Audio Ingestion Stream](file:///d:/VoicetoAI/docs/PHASES/PHASE_05_VAD_and_Audio_Streaming.md)
- **Master Guide:** [00_START_HERE_PHASE_GUIDE.md](file:///d:/VoicetoAI/docs/00_START_HERE_PHASE_GUIDE.md)
- **Related Specs:** [VoicePipeline.md](file:///d:/VoicetoAI/docs/FEATURE_SPECS/VoicePipeline.md), [MLOPS.md](file:///d:/VoicetoAI/docs/MLOPS.md)

---

### Objective
Deploy the speech-to-text pipeline supporting Urdu, English, and bilingual code-switching ("Urdish") using Whisper Large-v3-Turbo, with mandatory UI transcript confirmation.

### Business Goal
Allow Pakistani and international shop owners to describe their requirements effortlessly without typing friction, while preventing AI hallucinations through explicit transcript confirmation.

### Technical Goal
Implement high-throughput ASR inference with domain-specific priming prompts, achieving $<1.5\text{s}$ latency and $<14\%$ WER on conversational retail speech.

### Features Included
- Whisper ASR engine (supporting local Faster-Whisper and OpenAI Whisper API fallback).
- Domain-specific priming prompt injection for Pakistani retail terminology.
- Audio format normalization (converting WebM/Opus to 16kHz mono WAV).
- Transcript confirmation modal in the Next.js frontend.

### Features NOT Included
- LangGraph orchestration, code planning, automated editing.

### Dependencies
- Phase 1 (Contracts), Phase 2 (Database), Phase 3 (Audio Storage).

### Deliverables
- `backend/app/services/asr.py`.
- `frontend/components/voice/TranscriptModal.tsx`.
- Benchmark evaluation script for 30 test audio clips.

### Architecture Changes
- ASR processing service integrated into backend; FastAPI exposes audio-to-text pipeline.

### Database Changes
- Updates `messages` table with `audio_s3_key` and transcribed `content`.

### API Changes
- `POST /api/v1/voice/transcribe`: Accepts audio, uploads to S3, runs Whisper, returns transcript.

### Frontend Changes
- Audio recording button component with live recording timer.
- Transcript confirmation modal with editable text input and "Confirm / Re-record" buttons.

### Backend Changes
- Implementation of Whisper inference wrapper with retry and timeout logic.

### ML Changes
- Whisper prompt tuning with Urdu/English retail lexicon.

### Infrastructure Changes
- Local CUDA support or OpenAI API integration.

### Configuration Required
- Whisper model selection (`large-v3-turbo` vs API).

### Environment Variables
- `WHISPER_BACKEND=openai` (or `local`)
- `OPENAI_API_KEY=sk-...`

### Third-party Services
- OpenAI Whisper API (or local GPU instance).

### Tasks
- [x] Task 4.1: Implement audio normalization utility (16kHz mono WAV).
- [x] Task 4.2: Build Whisper ASR service with domain priming prompt.
- [x] Task 4.3: Implement FastAPI transcription endpoint.
- [x] Task 4.4: Build frontend audio recorder and transcript confirmation modal.
- [x] Task 4.5: Run ASR benchmark on 30 test clips.

### Subtasks
- Subtask 4.2.1: Construct Pakistani retail terminology prompt string.
- Subtask 4.4.1: Implement browser `MediaRecorder` hook in React.

### Acceptance Criteria
- Spoken voice note is transcribed into editable text in $<2.0\text{ seconds}$.
- Transcript confirmation modal displays text accurately in UI.
- User can edit a misspelled word and click "Confirm".
- ASR Word Error Rate on 30 test clips is $\le 14\%$.

### Definition of Done
- Complete voice-to-transcript flow operates seamlessly in the web browser; PR reviewed and merged.

### Unit Tests
- `test_audio_normalization_resample()`
- `test_whisper_prompt_formatting()`

### Integration Tests
- `test_transcribe_endpoint_with_sample_wav()`
- `test_asr_error_handling_corrupt_payload()`

### End-to-End Tests
- Playwright test: Record simulated audio $\to$ inspect modal $\to$ click confirm $\to$ assert backend message saved.

### Manual Testing Checklist
- [ ] Speak into laptop microphone in Urdu: "Meri jooton ki dukaan hai".
- [ ] Verify transcribed text appears in modal.
- [ ] Edit text to add "Lahore mein" and submit.
- [ ] Verify final text in database includes manual edit.

### Regression Tests
- Re-run Phases 1–3 test suites.

### Rollback Strategy
- Fall back to purely typed text input by disabling the microphone trigger component.

### Estimated Complexity
- Medium (3/5).

### Estimated Time
- 4 days.

### Risks
- High phonetic variation in regional Urdu accents causing misspellings.
- *Mitigation:* Mandatory transcript confirmation modal ensures user validates intent before LLM generation.

### Future Improvements
- Fine-tune Whisper LoRA on Pakistani e-commerce voice notes.
