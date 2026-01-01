# Deployment Guide - Vercel

Deploy the Grid Subtitle Decoder to Vercel for mobile testing.

---

## Quick Deploy (Recommended)

### 1. Install Vercel CLI

```bash
npm install -g vercel
```

### 2. Deploy from Project Root

```bash
cd "c:\ME\mes etudes\france\master\cours\IHM\IHMPROJET"
vercel
```

**Follow the prompts:**
- Set up and deploy? **Y**
- Which scope? Select your account
- Link to existing project? **N** (first time)
- Project name? **grid-subtitle-decoder** (or your choice)
- Directory? **.** (current directory)
- Override settings? **N**

### 3. Access on iPhone

After deployment completes, Vercel will provide a URL like:
```
https://grid-subtitle-decoder.vercel.app
```

Open this URL on your iPhone to test the decoder!

---

## Manual Deploy via Vercel Website

### 1. Push to GitHub

```bash
# Initialize git if not already done
git init
git add .
git commit -m "Add decoder web app"

# Create a GitHub repository and push
git remote add origin https://github.com/YOUR_USERNAME/grid-subtitle-decoder.git
git branch -M main
git push -u origin main
```

### 2. Import to Vercel

1. Go to [vercel.com](https://vercel.com)
2. Click "New Project"
3. Import your GitHub repository
4. Vercel will auto-detect settings
5. Click "Deploy"

---

## Testing on iPhone

### Using Encoded Video

**Option 1: Upload from iPhone**
1. Transfer `video_encoded.mp4` to your iPhone (AirDrop, Files app, etc.)
2. Open the Vercel URL on iPhone
3. Tap "Choose File" and select the video
4. Tap "Start Decoding"

**Option 2: Stream from Server**
If you want to preload a test video, you can:
1. Upload `video_encoded.mp4` to the repository
2. Modify `index.html` to include a "Load Sample Video" button
3. Redeploy to Vercel

### Expected Behavior

On iPhone:
- Video should play with native controls
- `playsinline` attribute prevents fullscreen hijacking
- Touch controls work (sliders, buttons)
- Decoder should run at 5-10 FPS on modern iPhones
- Subtitles appear in real-time below video

---

## Configuration Files

### vercel.json
```json
{
  "version": 2,
  "public": true,
  "cleanUrls": true,
  "trailingSlash": false,
  "rewrites": [
    {
      "source": "/",
      "destination": "/web_decoder/index.html"
    }
  ]
}
```

This configuration:
- Routes root URL to the decoder interface
- Enables clean URLs (no `.html` extension needed)
- Serves all files from the project

### .vercelignore
Excludes unnecessary files:
- Python cache
- Virtual environment
- Logs

---

## Troubleshooting

### Video Won't Load
- **Issue:** iPhone can't play the video codec
- **Solution:** Ensure video is encoded with H.264 (most compatible)
- **Check:** Run `ffmpeg -i video_encoded.mp4` to verify codec

### Decoder Not Working
- **Issue:** ES6 modules not loading
- **Solution:** Check browser console for errors
- **Verify:** Safari supports ES6 modules (iOS 11+)

### Performance Issues
- **Issue:** Decoder runs slowly on iPhone
- **Solution:** Reduce FPS slider to 5-8
- **Alternative:** Use smaller video resolution

### CORS Errors
- **Issue:** Module import blocked by CORS
- **Solution:** Vercel automatically handles CORS for static files
- **Verify:** Files are in correct directory structure

---

## Adding Sample Video to Deployment

If you want to include the encoded video in the deployment:

### 1. Optimize Video Size
```bash
# Compress video for web (optional)
ffmpeg -i video_encoded.mp4 -vcodec h264 -acodec aac -b:v 500k video_encoded_web.mp4
```

### 2. Update .vercelignore
Remove video files from ignore list or don't add them:
```
# Don't ignore
# *.mp4
```

### 3. Add Load Sample Button (Optional)

Add to `index.html`:
```html
<button id="loadSampleBtn">Load Sample Video</button>

<script>
document.getElementById('loadSampleBtn').addEventListener('click', () => {
    videoPlayer.src = '../video_encoded.mp4';
    log('Loaded sample video');
});
</script>
```

**Note:** This will increase deployment size. Encoded video is ~8MB.

---

## Alternative: Share Video via URL

Instead of including the video in deployment:

1. Upload `video_encoded.mp4` to a file hosting service:
   - Google Drive (get shareable link)
   - Dropbox (get direct link)
   - GitHub Releases

2. Use the direct video URL:
   ```javascript
   videoPlayer.src = 'https://your-direct-video-link.mp4';
   ```

---

## Environment URLs

Vercel provides:
- **Production:** `https://your-project.vercel.app`
- **Preview:** Unique URL for each deployment
- **Development:** Local testing with `vercel dev`

---

## Updating Deployment

After making changes:

```bash
# Quick update
vercel --prod

# Or with Git (if using GitHub integration)
git add .
git commit -m "Update decoder"
git push
# Vercel auto-deploys on push
```

---

## Local Testing Before Deploy

Test locally with Vercel environment:

```bash
vercel dev
```

This starts a local server that mimics Vercel's environment.

---

## Next Steps After Vercel Deploy

1. ✅ Test decoder with sample video on iPhone
2. ✅ Verify touch controls work properly
3. ✅ Check performance (FPS, latency)
4. ✅ Test with different threshold values
5. ⏭️ If working: Proceed to Phase 4 (add camera access)
6. ⏭️ If issues: Debug using Safari Web Inspector

---

## Safari Web Inspector (Debugging on iPhone)

To debug on iPhone:

1. **Enable Web Inspector on iPhone:**
   - Settings → Safari → Advanced → Web Inspector: ON

2. **Connect iPhone to Mac:**
   - Connect via USB
   - Open Safari on Mac
   - Develop menu → [Your iPhone] → Select the page

3. **View Console:**
   - See JavaScript errors
   - Monitor performance
   - Inspect network requests

---

## Cost

Vercel free tier includes:
- Unlimited deployments
- 100GB bandwidth/month
- HTTPS enabled
- Custom domains (optional)

This project easily fits within free tier limits.

---

## Share Your Results

After testing, you can share:
- Vercel URL with others for testing
- Screenshots/videos of decoder working on iPhone
- Performance metrics (FPS, success rate)

This validates the decoder core before building the full mobile app in Phase 4!
