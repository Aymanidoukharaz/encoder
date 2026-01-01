# Development Tasks & Phases

---

## Phase 1 – Project Foundations
- [x] Define grid dimensions (R × C)
- [x] Choose ROI placement strategy
- [x] Define ASCII packet format
- [x] Define CRC method

---

## Phase 2 – Encoder Development (Python)
- [x] Parse `.srt` subtitles
- [x] Convert subtitle text to ASCII bytes
- [x] Build binary packet (SYNC + LEN + PAYLOAD + CRC)
- [x] Convert bytes → bits
- [x] Map bits to grid cells
- [x] Encode grid into video frames (OpenCV)
- [x] Optimize luminance values for robustness
- [x] Export encoded video

---

## Phase 3 – Decoder Core (JavaScript)
- [x] Access camera using `getUserMedia`
- [x] Draw video frames into `<canvas>`
- [x] Extract ROI from frame
- [x] Divide ROI into grid cells
- [x] Compute luminance average per cell
- [x] Threshold luminance → bits
- [x] Convert bits → bytes
- [x] Detect SYNC pattern
- [x] Validate CRC
- [x] Decode ASCII subtitle text

---

## Phase 4 – Mobile Web App (UI/UX)
- [ ] Subtitle overlay display
- [ ] Live debug HUD (FPS, CRC status)
- [ ] Adjustable threshold slider
- [ ] Adjustable grid parameters
- [ ] ROI visualization

---

## Phase 5 – Calibration & Robustness
- [ ] Manual ROI adjustment
- [ ] Optional 4-point calibration
- [ ] Temporal smoothing (frame voting)
- [ ] Error handling (CRC failure)
- [ ] Subtitle persistence between frames

---

## Phase 6 – Performance & Testing
- [ ] Test on multiple phones
- [ ] Test under different lighting
- [ ] Test compressed videos
- [ ] Measure latency and FPS
- [ ] Optimize sampling strategy

---

## Phase 7 – Documentation & Delivery
- [ ] Final README
- [ ] Usage guide
- [ ] Demo video
- [ ] Architecture diagrams

