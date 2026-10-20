# Phase 3: S3 Object Storage & Audio Validation Pipeline

---

### Navigation
- **Current Phase:** Phase 3 of 20
- **Previous Phase:** [Phase 2: PostgreSQL with pgvector Schema & Database Migrations](file:///d:/VoicetoAI/docs/PHASES/PHASE_02_Postgres_and_pgvector.md)
- **Next Phase:** [Phase 4: Bilingual Whisper ASR & Transcript Confirmation Engine](file:///d:/VoicetoAI/docs/PHASES/PHASE_04_Whisper_ASR_and_Transcript.md)
- **Master Guide:** [00_START_HERE_PHASE_GUIDE.md](file:///d:/VoicetoAI/docs/00_START_HERE_PHASE_GUIDE.md)
- **Related Specs:** [VoicePipeline.md](file:///d:/VoicetoAI/docs/FEATURE_SPECS/VoicePipeline.md), [DEVOPS.md](file:///d:/VoicetoAI/docs/DEVOPS.md)

---

### Objective
Implement secure object storage for audio files, visual screenshots, and site zip archives using an S3-compatible API with cryptographic pre-signed URLs.

### Business Goal
Safely store customer voice recordings and audit trail media with low cost and high durability.

### Technical Goal
Deploy MinIO for local development and configure `boto3` / `aioboto3` client with upload validation (MIME type, size, duration, audio energy).

### Features Included
- Local MinIO container in Docker Compose with auto-created buckets: `voicetoai-audio`, `voicetoai-artifacts`.
- Asynchronous S3 storage service in backend.
- Audio file validation: checks file size ($< 15\text{ MB}$), duration ($1.0\text{s} - 120.0\text{s}$), and RMS audio energy ($> -45\text{ dBFS}$).
- Pre-signed URL generation for secure, temporary media access.

### Features NOT Included
- Whisper speech-to-text processing, streaming WebSockets.

### Dependencies
- Phase 1 (Repository), Phase 2 (Database for message linkage).

### Deliverables
- MinIO service in `docker-compose.yml`.
- `backend/app/services/storage.py` (S3 client).
- `backend/app/services/audio_validator.py`.
- Unit and integration tests for storage operations.

### Architecture Changes
- Backend gains object storage capability; audio binary data is detached from PostgreSQL and stored in S3.

### Database Changes
- None (populates existing `messages.audio_s3_key`).

### API Changes
- `POST /api/v1/storage/upload-audio`: Uploads and validates raw audio blob.
- `GET /api/v1/storage/signed-url`: Generates 15-minute expiring read URL.

### Frontend Changes
- None.

### Backend Changes
- Integration of `aioboto3` for non-blocking file streaming to S3.
- Audio validation pipeline using `soundfile` and `pydub` / `librosa`.

### ML Changes
- Audio preprocessing filter to detect silent or corrupt audio.

### Infrastructure Changes
- MinIO service running on ports 9000 (API) and 9001 (Console).

### Configuration Required
- S3 access keys, bucket policies, and endpoint URLs.

### Environment Variables
- `S3_ENDPOINT_URL=http://localhost:9000`
- `S3_ACCESS_KEY=minioadmin`
- `S3_SECRET_KEY=minioadmin`
- `S3_AUDIO_BUCKET=voicetoai-audio`
- `S3_ARTIFACTS_BUCKET=voicetoai-artifacts`

### Third-party Services
- AWS S3 or Cloudflare R2 in production; MinIO in development.

### Tasks
- [x] Task 3.1: Add MinIO service to Docker Compose.
- [x] Task 3.2: Implement asynchronous S3 client service.
- [x] Task 3.3: Implement audio validation and loudness checker.
- [x] Task 3.4: Expose upload and pre-signed URL endpoints in FastAPI.

### Subtasks
- Subtask 3.3.1: Write RMS decibel calculation function.
- Subtask 3.3.2: Implement file signature / magic-byte verification for WebM and WAV.

### Acceptance Criteria
- Uploading a 5-second valid audio clip stores the file in MinIO and returns an S3 key.
- Uploading a completely silent audio file is rejected with HTTP 422 Unprocessable Entity.
- Pre-signed URL allows downloading the audio clip in an external browser.

### Definition of Done
- Storage service verified with integration tests against MinIO; documentation updated.

### Unit Tests
- `test_audio_validator_valid_audio()`
- `test_audio_validator_silent_audio_rejected()`
- `test_audio_validator_oversized_file_rejected()`

### Integration Tests
- `test_s3_upload_and_download_roundtrip()`
- `test_presigned_url_expiration()`

### End-to-End Tests
- None.

### Manual Testing Checklist
- [ ] Start MinIO, open `http://localhost:9001` in browser.
- [ ] Post a sample WAV file via Swagger UI at `/docs`.
- [ ] Verify object appears in `voicetoai-audio` bucket in MinIO console.

### Regression Tests
- Re-run Phase 1 and 2 test suites.

### Rollback Strategy
- Remove MinIO container and revert `storage.py`.

### Estimated Complexity
- Low (2/5).

### Estimated Time
- 3 days.

### Risks
- Network timeouts during large file uploads.
- *Mitigation:* Strict 15 MB file size limit enforced before reading buffer into memory.

### Future Improvements
- Client-direct S3 pre-signed POST uploads to bypass backend gateway for multi-megabyte files.
