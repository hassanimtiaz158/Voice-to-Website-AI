# Phase 5: Voice Activity Detection (VAD) & Real-time Audio Ingestion Stream

---

### Navigation
- **Current Phase:** Phase 5 of 20
- **Previous Phase:** [Phase 4: Bilingual Whisper ASR & Transcript Confirmation Engine](file:///d:/VoicetoAI/docs/PHASES/PHASE_04_Whisper_ASR_and_Transcript.md)
- **Next Phase:** [Phase 6: Pinned Scaffolds & E2B / Docker Sandbox Runner Engine](file:///d:/VoicetoAI/docs/PHASES/PHASE_06_Scaffold_and_Sandbox_Runner.md)
- **Master Guide:** [00_START_HERE_PHASE_GUIDE.md](file:///d:/VoicetoAI/docs/00_START_HERE_PHASE_GUIDE.md)
- **Related Specs:** [VoicePipeline.md](file:///d:/VoicetoAI/docs/FEATURE_SPECS/VoicePipeline.md)

---

### Objective
Integrate client-side and server-side Voice Activity Detection (VAD) to automatically detect speech boundaries, silence, and background noise.

### Business Goal
Provide a frictionless, hands-free conversational experience where recording stops automatically when the merchant finishes speaking.

### Technical Goal
Deploy Silero VAD / WebRTC VAD with a 1,800 ms silence trigger and real-time audio chunk streaming over WebSockets.

### Features Included
- Silero VAD integration in client/backend.
- Silence threshold detection (1,800 ms of trailing silence triggers automatic stop).
- WebSocket streaming audio endpoint `/ws/v1/voice/stream`.
- Visual waveform / audio level indicator in frontend UI.

### Features NOT Included
- Direct LLM streaming responses, code generation.

### Dependencies
- Phase 4 (ASR & Audio Processing).

### Deliverables
- `frontend/hooks/useVAD.ts`.
- `backend/app/services/vad.py`.
- WebSocket streaming handler in `backend/app/api/ws_voice.py`.

### Architecture Changes
- Introduction of WebSocket communication layer for real-time bidirectional audio streaming.

### Database Changes
- None.

### API Changes
- `WebSocket /ws/v1/voice/stream`: Bidirectional audio streaming and real-time transcription status.

### Frontend Changes
- Animated pulsating microphone button responding to voice volume.
- Auto-submit trigger when VAD detects end of speech.

### Backend Changes
- Chunked audio buffer accumulator with VAD evaluation per 30ms audio frame.

### ML Changes
- Silero VAD ONNX runtime integration.

### Infrastructure Changes
- None.

### Configuration Required
- VAD silence sensitivity threshold (default: 0.5 probability).

### Environment Variables
- `VAD_SILENCE_TIMEOUT_MS=1800`

### Third-party Services
- None.

### Tasks
- [x] Task 5.1: Package Silero VAD ONNX model for Python runtime.
- [x] Task 5.2: Implement WebSocket streaming chunk accumulator.
- [x] Task 5.3: Implement frontend audio worklet with volume visualization.
- [x] Task 5.4: Implement automatic stop-on-silence logic.

### Subtasks
- Subtask 5.2.1: Write 30ms PCM frame slicing algorithm.
- Subtask 5.3.1: Build Canvas-based audio waveform component.

### Acceptance Criteria
- User speaks; waveform oscillates in real time.
- User stops speaking; recording automatically terminates after 1.8 seconds.
- WebSocket emits transcription event within 800 ms of speech cessation.

### Definition of Done
- Hands-free voice recording operates reliably across Chrome, Firefox, and Safari without manual button tapping.

### Unit Tests
- `test_vad_frame_slicing()`
- `test_vad_silence_detection()`

### Integration Tests
- `test_websocket_audio_stream_complete_flow()`

### End-to-End Tests
- Automated browser test verifying recording stop event triggers upon feeding a 3-second audio file followed by 2 seconds of silence.

### Manual Testing Checklist
- [ ] Speak continuously for 10 seconds; verify no premature cutoff.
- [ ] Pause speaking for 2 seconds; verify recording ends automatically and transcript modal opens.

### Regression Tests
- Re-run Phase 4 transcription tests.

### Rollback Strategy
- Disable VAD auto-stop flag; revert to manual click-to-start / click-to-stop recording.

### Estimated Complexity
- Medium (3/5).

### Estimated Time
- 3 days.

### Risks
- Background fan noise or traffic in retail shops preventing silence detection.
- *Mitigation:* Audio energy gate combined with probability thresholding prevents ambient noise from keeping VAD open indefinitely.

### Future Improvements
- Background noise cancellation via WebAssembly Krisp or RNNoise in the browser.
