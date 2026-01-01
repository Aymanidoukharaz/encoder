# Project Title
Grid-Based Subtitle Steganography & Mobile Web Decoder

---

## 1. Overview

This project aims to encode video subtitles directly into video frames using a **grid-based visual encoding system** (called “flacons”), and to decode them in real time using a **mobile web application** running on a smartphone.

The decoding is performed via the phone camera, without any visible markers or QR codes, and reconstructs subtitles using **ASCII encoding**.

---

## 2. Problem Statement

Traditional subtitles:
- require direct access to the video file,
- are lost in screen captures or projections,
- cannot be recovered from a recorded screen.

This project solves that by:
- embedding subtitles visually inside the video frames,
- allowing recovery from **any camera recording of the screen**,
- using only a **web app** (no native installation).

---

## 3. Goals & Objectives

### Primary Goals
- Encode subtitles into video frames using a **grid of visual cells**
- Decode subtitles using a **smartphone web app**
- Use **ASCII encoding**
- Avoid all visual markers (QR, ArUco, corner markers)

### Secondary Goals
- Robust decoding under compression (H.264)
- Real-time decoding (≥ 10 FPS)
- Simple calibration and UX on mobile

---

## 4. High-Level Architecture

### Encoding Side (Offline / Desktop)
- Input: video + `.srt` subtitles
- Output: encoded video with subtitle grid
- Tools: Python + OpenCV

### Decoding Side (Mobile)
- Input: live camera feed
- Output: decoded subtitles displayed on phone
- Tools: JavaScript + HTML5 + Canvas + WebRTC

---

## 5. Encoding Concept (Flacons Grid)

- A fixed **ROI (Region of Interest)** is defined in the video
- ROI is subdivided into a **grid (R × C)**
- Each cell encodes **1 bit** using luminance
- 8 cells = 1 ASCII character

### Bit Encoding
- Bit `1` → bright cell
- Bit `0` → dark cell
- Encoding done on luminance (Y channel)

---

## 6. Data Format

Each grid encodes a binary packet:

| Field      | Size |
|-----------|------|
| SYNC      | 2 bytes (`0xAA 0x55`) |
| LENGTH    | 1 byte |
| PAYLOAD   | N bytes (ASCII subtitle) |
| CRC       | 1 byte (XOR) |

---

## 7. Decoding Concept

- Smartphone camera captures the screen
- Web app extracts ROI
- Grid cells are averaged
- Thresholding converts luminance → bits
- Bits → bytes → ASCII → subtitles

---

## 8. User Experience

1. User opens the web app
2. Grants camera permission
3. Points phone at the video screen
4. Adjusts ROI (or calibrates once)
5. Subtitles appear in real time on phone

---

## 9. Constraints

- Must run entirely in browser
- No native apps
- No markers or fiducials
- Must tolerate compression and blur

---

## 10. Success Metrics

- ≥ 95% subtitle accuracy under compression
- Subtitle latency < 300 ms
- Works on mid-range smartphones

---

## 11. Non-Goals

- DRM protection
- Audio decoding
- Invisible watermarking

---

## 12. Target Platforms

- Android (Chrome)
- iOS (Safari)
- Desktop browsers (for testing)

