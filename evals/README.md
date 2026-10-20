# Evaluation Harness: Voice-to-Website AI

This directory houses the quantitative benchmark suites for the FYP defense:

1. `audio_clips/`: 30 bilingual Urdu/English benchmark voice notes for ASR evaluation (WER < 14%).
2. `personas/`: 20 scripted shop owner persona scenarios evaluating turns-to-ready (<= 3 turns).
3. `build_scenarios/`: 30 greenfield business prompts for headless compilation verification (>= 85% pass rate).
4. `edit_tasks/`: 30 surgical modification prompts testing 3-signal manifest retrieval (Recall@3 >= 90%).
