# AI Agent Rules – Mandatory

You are a specialized AI agent working on ONE PHASE ONLY of this project.

---

## Project Constraints (Must Always Hold)

- Grid-based visible encoding ("flacons"): one cell = one bit
- ASCII encoding only
- Decoding via a mobile web app using the phone camera
- NO markers, NO QR codes, NO ArUco, NO fiducials
- Robustness > capacity
- Packets must be validated using: SYNC + LEN + CRC (XOR)
- Decoding must use cell averaging (never single pixels)

---

## Repository Inputs

The following files are available and must be respected:
- PRD.md
- ST.md
- tasks.md
- video.mp4
- sous_titres.srt

---

## Agent Operating Rules

You MUST:
1) Work ONLY on the phase explicitly requested.
2) Output ONLY the deliverables requested for that phase.
3) Provide a short **Handoff Summary** for the next agent.
4) Avoid unrelated explanations or future planning.

If something is missing:
- Make a reasonable assumption
- Explicitly state the assumption
- Do NOT change the architecture

Any violation of these rules invalidates your output.
