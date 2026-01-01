import cv2
import numpy as np
import re
import os

# Configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_VIDEO = os.path.join(SCRIPT_DIR, "../video.mp4")
INPUT_SRT = os.path.join(SCRIPT_DIR, "../sous_titres.srt")
OUTPUT_VIDEO = os.path.join(SCRIPT_DIR, "../video_encoded_grid.mp4")

# Grid Configuration
GRID_COLS = 12  # 12 columns
GRID_ROWS = 12  # 12 rows
# Total bits = 144. Capacity = 18 characters (8 bits each).

# Visual Configuration
# Colors (BGR)
COLOR_ON = (255, 255, 255)  # White for bit 1
COLOR_OFF = (0, 0, 0)       # Black for bit 0
COLOR_GRID = (100, 100, 100) # Gray for grid lines
OPACITY = 0.7 # Opacity of the overlay

def parse_time(time_str):
    """Convert SRT timestamp (00:00:02,280) to seconds."""
    h, m, s = time_str.replace(',', '.').split(':')
    return int(h) * 3600 + int(m) * 60 + float(s)

def parse_srt(filepath):
    """Parse SRT file into a list of subtitles."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find subtitle blocks
    # Matches: Index, Time range, Text
    pattern = re.compile(r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n((?:(?!\n\n).)*)', re.DOTALL)
    
    subtitles = []
    for match in pattern.finditer(content):
        start_time = parse_time(match.group(2))
        end_time = parse_time(match.group(3))
        text = match.group(4).replace('\n', ' ').strip()
        subtitles.append({
            'start': start_time,
            'end': end_time,
            'text': text
        })
    return subtitles

def text_to_bits(text):
    """Convert text to a 12x12 bit matrix (Linear mapping)."""
    total_bits = GRID_COLS * GRID_ROWS
    max_chars = total_bits // 8
    
    # Truncate text to fit capacity
    text = text[:max_chars]
    
    # Convert text to bit string
    bits = []
    for char in text:
        try:
            code = ord(char)
            if code > 255: code = ord('?')
        except:
            code = ord('?')
        
        # Get 8 bits (MSB first)
        for i in range(8):
            bits.append((code >> (7 - i)) & 1)
            
    # Pad with zeros if needed
    while len(bits) < total_bits:
        bits.append(0)
        
    # Reshape into matrix
    matrix = np.array(bits).reshape((GRID_ROWS, GRID_COLS))
    return matrix

def draw_grid(frame, matrix):
    """Draw the 12x12 grid on the frame with circles (flacons)."""
    height, width = frame.shape[:2]
    
    # Calculate cell size
    cell_w = width // GRID_COLS
    cell_h = height // GRID_ROWS
    
    # Calculate radius for the circle (20% of cell size)
    radius = int(min(cell_w, cell_h) * 0.20)
    
    # Create an overlay
    overlay = frame.copy()
    
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            bit = matrix[row, col]
            
            # Calculate center of the cell
            cx = int(col * cell_w + cell_w / 2)
            cy = int(row * cell_h + cell_h / 2)
            
            if bit == 1:
                # Draw filled white circle for bit 1
                cv2.circle(overlay, (cx, cy), radius, COLOR_ON, -1)
            
            # No grid lines drawn anymore
            # No drawing for bit 0 (transparent)

    # Blend overlay with original frame
    cv2.addWeighted(overlay, OPACITY, frame, 1 - OPACITY, 0, frame)

def main():
    print("Starting encoding...")
    
    # Load resources
    subs = parse_srt(INPUT_SRT)
    cap = cv2.VideoCapture(INPUT_VIDEO)
    
    if not cap.isOpened():
        print(f"Error: Could not open video {INPUT_VIDEO}")
        return

    # Video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Output setup
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(OUTPUT_VIDEO, fourcc, fps, (width, height))
    
    frame_idx = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        current_time = frame_idx / fps
        
        # Find active subtitle
        active_text = ""
        for sub in subs:
            if sub['start'] <= current_time <= sub['end']:
                active_text = sub['text']
                break
        
        # If we have text, draw the grid
        if active_text:
            # print(f"Frame {frame_idx}: Encoding '{active_text}'")
            matrix = text_to_bits(active_text)
            draw_grid(frame, matrix)
        else:
            # Optional: Draw empty grid or nothing?
            # Let's draw an empty grid (all zeros = NULL chars) or just nothing.
            # User said "caque cellules contient un flacon", implies grid is always there?
            # Let's leave it empty (video only) when no subtitle, or maybe a "blank" grid?
            # For now: No grid if no subtitle, to let the video breathe.
            pass

        out.write(frame)
        
        if frame_idx % 100 == 0:
            print(f"Processed {frame_idx}/{total_frames} frames")
            
        frame_idx += 1
        
    cap.release()
    out.release()
    print(f"Encoding complete. Output saved to {OUTPUT_VIDEO}")

if __name__ == "__main__":
    main()
