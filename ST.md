# Technical Specifications – AI Agent

This document defines **strict rules** that the AI assistant must follow during development.

---

## 1. Global Constraints

- The AI must respect the grid-based encoding architecture
- No QR codes, no fiducial markers, no ArUco
- Decoding must be compatible with **mobile browsers**
- All subtitle data must be recoverable via **camera capture**

---

## 2. Encoding Rules

- Encoding must use **grid-based luminance modulation**
- Each grid cell represents exactly **1 bit**
- ASCII encoding is mandatory
- Video compression must be assumed (H.264)
- Luminance values must be well separated (dark vs light)

---

## 3. Decoding Rules

- Decoding must work on **raw camera frames**
- No assumptions on pixel-perfect alignment
- Use **cell averaging**, never single pixels
- Threshold must be configurable
- Packet must be validated using CRC

---

## 4. Performance Constraints

- Target decoding FPS ≥ 10
- Processing must be real-time
- Avoid heavy per-pixel loops
- Prefer subsampling strategies

---

## 5. Error Handling

- Invalid packets must be ignored
- Subtitle should persist until a new valid packet
- CRC failures must not crash the app

---

## 6. Web App Constraints

- Use only standard web APIs
- Must run on mobile Safari and Chrome
- No server-side decoding
- No external native dependencies

---

## 7. Extensibility

The architecture must allow:
- UTF-8 extension
- Reed-Solomon error correction
- Adaptive grid sizes
- Automatic ROI detection

---

## 8. Forbidden Actions

❌ Adding visual markers  
❌ Using QR codes  
❌ Requiring native apps  
❌ Relying on uncompressed video  

---

## 9. AI Development Behavior

The AI assistant must:
- Prioritize robustness over capacity
- Explain trade-offs clearly
- Produce readable, modular code
- Keep encoding and decoding symmetric

