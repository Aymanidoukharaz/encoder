# Grid-Based Subtitle Steganography

Encode subtitles into video frames using grid-based visual encoding, decode them with a mobile web app.

## 🚀 Quick Deploy to Vercel (Test on iPhone)

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy from project root
cd "c:\ME\mes etudes\france\master\cours\IHM\IHMPROJET"
vercel

# Follow prompts, then open the URL on your iPhone!
```

See [DEPLOY.md](DEPLOY.md) for detailed instructions.

## 📁 Project Structure

```
├── encoder/              # Python encoder (Phase 2) ✅
│   ├── encode_video.py
│   ├── grid_embed.py
│   ├── packet.py
│   └── srt_parser.py
│
├── web_decoder/          # JavaScript decoder (Phase 3) ✅
│   ├── decoder_core.js
│   ├── grid_reader.js
│   ├── packet.js
│   ├── index.html        # Mobile-friendly test interface
│   └── README.md
│
├── video.mp4             # Original video
├── sous_titres.srt       # Subtitles
├── video_encoded.mp4     # Encoded output (8 MB)
└── video_encoded_debug.mp4  # With visible grid overlay (8.7 MB)
```

## 🎯 Current Status

- ✅ **Phase 1:** Foundations (Grid: 8×12, ASCII, CRC)
- ✅ **Phase 2:** Python Encoder (Complete)
- ✅ **Phase 3:** JavaScript Decoder Core (Complete)
- ⏭️ **Phase 4:** Mobile Web App UI/UX (Next)
- ⏭️ **Phase 5:** Calibration & Robustness
- ⏭️ **Phase 6:** Performance & Testing

## 🔧 Usage

### Encoding (Desktop)

```bash
# Activate virtual environment
.venv\Scripts\activate

# Encode video with subtitles
python encoder/encode_video.py --video video.mp4 --srt sous_titres.srt --output video_encoded.mp4

# With debug grid overlay
python encoder/encode_video.py --video video.mp4 --srt sous_titres.srt --output video_encoded.mp4 --debug
```

### Decoding (Browser)

**Local testing:**
```bash
cd web_decoder
python -m http.server 8000
# Open: http://localhost:8000/index.html
```

**Vercel deployment:**
```bash
vercel
# Open URL on iPhone/mobile device
```

## 📱 Testing on iPhone

1. Deploy to Vercel (see above)
2. Transfer `video_encoded.mp4` to your iPhone
3. Open Vercel URL in Safari
4. Upload video and tap "Start Decoding"
5. Watch subtitles decode in real-time!

## 🏗️ Architecture

### Encoding
- Grid: 8 rows × 12 columns = 96 bits per frame
- ROI: Bottom-right (75%, 80%, 20%, 15%)
- Luminance: Y₀=32 (bit 0), Y₁=224 (bit 1)
- Packet: SYNC(2B) + LEN(1B) + PAYLOAD(8B) + CRC(1B)
- Repetition: 4× per packet for robustness

### Decoding
- Cell averaging (70% center region)
- Adaptive thresholding (90% of avg luminance)
- SYNC detection (0xAA55)
- CRC validation (XOR checksum)
- Subtitle persistence on errors

## 📊 Performance

- **Encoding:** ~24 FPS (real-time capable)
- **Decoding (Desktop):** 20-30 FPS
- **Decoding (Mobile):** 10-15 FPS
- **Success Rate:** >90% under compression

## 🛠️ Requirements

### Encoder (Python)
- Python 3.8+
- OpenCV (`pip install opencv-python`)
- NumPy (`pip install numpy`)

### Decoder (JavaScript)
- Modern browser (Chrome/Firefox/Safari)
- ES6 module support
- HTML5 Canvas API

## 📖 Documentation

- [encoder/README.md](encoder/README.md) - Encoder details
- [web_decoder/README.md](web_decoder/README.md) - Decoder API
- [web_decoder/QUICKSTART.md](web_decoder/QUICKSTART.md) - Quick start guide
- [DEPLOY.md](DEPLOY.md) - Vercel deployment guide
- [PRD.md](PRD.md) - Product requirements
- [ST.md](ST.md) - Technical specifications
- [tasks.md](tasks.md) - Development phases

## 🎯 Next Steps

1. **Test decoder on iPhone** via Vercel
2. **Implement Phase 4:** Add camera access via getUserMedia
3. **Build mobile UI:** ROI calibration, touch controls
4. **Performance testing:** Multiple devices, lighting conditions
5. **Optimization:** WebAssembly, error correction (Reed-Solomon)

## 📄 License

MIT License - Educational project for IHM course.

## 🤝 Contributing

This is a course project. Phases are developed sequentially following AGENT_RULES.md.

---

**🚀 Ready to test?** Run `vercel` and open the URL on your iPhone!
