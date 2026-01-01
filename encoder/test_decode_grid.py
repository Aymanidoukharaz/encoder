import cv2
import numpy as np
import os

# Configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_VIDEO = os.path.join(SCRIPT_DIR, "../video_web_grid.mp4")

# Grid Configuration
GRID_COLS = 12
GRID_ROWS = 12
THRESHOLD = 128  # Luminance threshold to decide if a circle is present

def bits_to_text(matrix):
    """Convert 12x12 bit matrix back to text."""
    # Flatten matrix to list of bits
    bits = matrix.flatten().tolist()
    
    chars = []
    # Process 8 bits at a time
    for i in range(0, len(bits), 8):
        if i + 8 > len(bits):
            break
            
        byte_bits = bits[i:i+8]
        
        # Reconstruct byte value
        char_code = 0
        for bit_idx, bit in enumerate(byte_bits):
            if bit:
                char_code |= (1 << (7 - bit_idx))
                
        if char_code == 0:
            break # Stop at null terminator
            
        chars.append(chr(char_code))
        
    return "".join(chars)

def decode_frame(frame):
    """Extract bits from the frame."""
    height, width = frame.shape[:2]
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    cell_w = width // GRID_COLS
    cell_h = height // GRID_ROWS
    
    matrix = np.zeros((GRID_ROWS, GRID_COLS), dtype=int)
    
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            # Sample the center of the cell
            cx = int(col * cell_w + cell_w / 2)
            cy = int(row * cell_h + cell_h / 2)
            
            # Get pixel value
            val = gray[cy, cx]
            
            # Threshold
            if val > THRESHOLD:
                matrix[row, col] = 1
            else:
                matrix[row, col] = 0
                
    return matrix

def main():
    print(f"Testing decoder on {INPUT_VIDEO}...")
    cap = cv2.VideoCapture(INPUT_VIDEO)
    
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    frame_idx = 0
    last_text = ""
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        # Decode every 10th frame to be fast
        if frame_idx % 10 == 0:
            matrix = decode_frame(frame)
            text = bits_to_text(matrix)
            
            # Only print if text changed and is not empty
            if text and text != last_text:
                print(f"Frame {frame_idx}: Found text -> '{text}'")
                last_text = text
                
        frame_idx += 1
        
    cap.release()
    print("Test complete.")

if __name__ == "__main__":
    main()
