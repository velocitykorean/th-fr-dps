# The Freudian Depths (th-fr-dps)

> **Autonomous Psychoanalytic & Philosophical Video Production Engine**  
> Dedicated to exploring the unconscious mind, human desire, defense mechanisms, and the architecture of civilization through the lens of Sigmund Freud.

---

## Channel Overview
- **YouTube Channel**: [The Freudian Depths](https://youtube.com/@thefreudiandepths)
- **Official Handle**: `@thefreudiandepths`
- **Tagline**: *Sigmund Freud, The Unconscious Mind & Human Desire*
- **Aesthetic**: Dark academic study, warm antique gold typography, sepia portraits, single-line dynamic subtitle synchronization.

---

## System Architecture

1. **Psychoanalytic Story Engine (`story_generator.py`)**:
   - 12 pre-crafted master curriculum topics covering Freud's seminal works (*The Ego and the Id*, *The Interpretation of Dreams*, *Civilization and Its Discontents*, *Beyond the Pleasure Principle*, *Totem and Taboo*).
   - Dynamic AI topic expansion via Pollinations AI.

2. **Neural Speech Synthesis (`tts_engine.py`)**:
   - Kokoro-82M ONNX local neural voice (`bm_lewis`, speed `0.85`, British analytic cadence).
   - Sample-accurate acoustic phoneme duration modeling (`compute_acoustic_word_timings`) for real-time word-to-speech alignment.

3. **Cinematic 1080p Video Composer (`video_composer.py`)**:
   - Single static portrait per video (no distracting mid-video transitions).
   - Strictly single-line subtitles (48pt) with radiant gold active highlighting (`#FFD700`).
   - Floating music spectrum visualizer with ~125px breathing space below subtitles.
   - Zero bounding boxes or container slates for an uncluttered, high-end presentation.

4. **Automated YouTube & Facebook Publisher (`auto_pipeline.py`)**:
   - Autonomous scheduled execution via GitHub Actions (`.github/workflows/generate_video.yml`).
   - Generates high-CTR 1080p thumbnails, SEO-optimized metadata with timestamps, tags, and descriptions.

---

## Local Execution

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Render a 60-second test preview
python auto_pipeline.py --preview 60 --dry-run

# 3. Render a full 20-minute episode
python auto_pipeline.py --duration 20.0 --dry-run
```
