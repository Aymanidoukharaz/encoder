"""
Video Encoder - Main orchestrator for encoding subtitles into video frames
"""
import cv2
import argparse
import os
from typing import List, Optional
from srt_parser import parse_srt, SubtitleEntry, get_subtitle_at_time
from packet import build_packet, packet_to_bits, text_to_packets
from grid_embed import embed_bits_in_frame, embed_empty_grid, get_roi_info, draw_grid_overlay


# Encoding parameters
REPETITION_COUNT = 4  # Repeat each packet N times for robustness


def get_current_subtitle(subtitles: List[SubtitleEntry], frame_number: int, fps: float) -> str:
    """
    Get the subtitle text that should be displayed at a given frame
    
    Args:
        subtitles: List of subtitle entries
        frame_number: Current frame number (0-indexed)
        fps: Video frames per second
    
    Returns:
        Subtitle text, or empty string if no subtitle at this frame
    """
    # Convert frame number to milliseconds
    time_ms = int((frame_number / fps) * 1000)
    
    return get_subtitle_at_time(subtitles, time_ms)


def encode_subtitle_to_packets(text: str) -> List[List[int]]:
    """
    Encode subtitle text into repeated packets for robustness
    
    Args:
        text: Subtitle text (ASCII)
    
    Returns:
        List of packets, with each packet repeated REPETITION_COUNT times
    """
    if not text.strip():
        return []
    
    # Split text into packets (8 chars each)
    base_packets = text_to_packets(text)
    
    # Repeat each packet for robustness
    repeated_packets = []
    for packet in base_packets:
        for _ in range(REPETITION_COUNT):
            repeated_packets.append(packet)
    
    return repeated_packets


def encode_video(input_video: str, input_srt: str, output_video: str, 
                 debug_overlay: bool = False, codec: str = 'mp4v'):
    """
    Encode subtitles from SRT file into video frames
    
    Args:
        input_video: Path to input video file
        input_srt: Path to input .srt subtitle file
        output_video: Path to output encoded video file
        debug_overlay: If True, draw grid overlay for visualization
        codec: Video codec fourcc code
    """
    print("=" * 60)
    print("SUBTITLE VIDEO ENCODER - Phase 2")
    print("=" * 60)
    
    # Parse subtitles
    print(f"\n[1/5] Parsing subtitles: {input_srt}")
    subtitles = parse_srt(input_srt)
    print(f"      Loaded {len(subtitles)} subtitle entries")
    
    # Open input video
    print(f"\n[2/5] Opening input video: {input_video}")
    cap = cv2.VideoCapture(input_video)
    
    if not cap.isOpened():
        raise ValueError(f"Cannot open video file: {input_video}")
    
    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    print(f"      Resolution: {frame_width}x{frame_height}")
    print(f"      FPS: {fps:.2f}")
    print(f"      Total frames: {total_frames}")
    print(f"      Duration: {total_frames/fps:.2f} seconds")
    
    # Display ROI info
    roi_info = get_roi_info(frame_width, frame_height)
    print(f"\n      ROI Info:")
    print(f"        Position: {roi_info['roi_position']}")
    print(f"        Size: {roi_info['roi_size']}")
    print(f"        Cell size: {roi_info['cell_size']}")
    
    # Setup output video
    print(f"\n[3/5] Setting up output video: {output_video}")
    
    # Use MJPEG for intermediate (lossless)
    temp_codec = 'MJPG' if codec == 'h264' else codec
    fourcc = cv2.VideoWriter_fourcc(*temp_codec)
    temp_output = output_video.replace('.mp4', '_temp.avi') if codec == 'h264' else output_video
    
    out = cv2.VideoWriter(temp_output, fourcc, fps, (frame_width, frame_height))
    
    if not out.isOpened():
        raise ValueError(f"Cannot create output video file: {temp_output}")
    
    # Pre-compute packet sequences for each subtitle
    print(f"\n[4/5] Pre-computing packet sequences...")
    subtitle_packets = {}
    for subtitle in subtitles:
        packets = encode_subtitle_to_packets(subtitle.text)
        subtitle_packets[subtitle.index] = {
            'packets': packets,
            'frame_index': 0  # Current position in packet list
        }
        print(f"      Subtitle {subtitle.index}: '{subtitle.text[:30]}...' -> {len(packets)} packets")
    
    # Process video frame by frame
    print(f"\n[5/5] Encoding frames...")
    print(f"      Repetition: {REPETITION_COUNT}x per packet")
    
    frame_number = 0
    current_subtitle_text = ""
    current_subtitle_index = None
    packet_sequence = []
    packet_index = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Get subtitle for current frame
        subtitle_text = get_current_subtitle(subtitles, frame_number, fps)
        
        # Detect subtitle change
        if subtitle_text != current_subtitle_text:
            current_subtitle_text = subtitle_text
            
            # Find subtitle entry
            current_subtitle_index = None
            for subtitle in subtitles:
                if subtitle.text == subtitle_text:
                    current_subtitle_index = subtitle.index
                    break
            
            # Reset packet sequence
            if current_subtitle_index and current_subtitle_index in subtitle_packets:
                packet_sequence = subtitle_packets[current_subtitle_index]['packets']
                packet_index = 0
            else:
                packet_sequence = []
                packet_index = 0
        
        # Encode frame
        if packet_sequence and packet_index < len(packet_sequence):
            # Get current packet
            packet = packet_sequence[packet_index]
            bits = packet_to_bits(packet)
            
            # Embed bits into frame
            encoded_frame = embed_bits_in_frame(frame, bits)
            
            # Move to next packet
            packet_index += 1
        else:
            # No subtitle or finished encoding current subtitle
            encoded_frame = embed_empty_grid(frame)
        
        # Add debug overlay if requested
        if debug_overlay:
            encoded_frame = draw_grid_overlay(encoded_frame)
        
        # Write frame
        out.write(encoded_frame)
        
        # Progress update
        if frame_number % 100 == 0:
            progress = (frame_number / total_frames) * 100
            print(f"      Progress: {progress:.1f}% ({frame_number}/{total_frames} frames)")
        
        frame_number += 1
    
    # Cleanup
    cap.release()
    out.release()
    
    # Convert to H.264 if needed
    if codec == 'h264':
        print(f"\n[6/6] Converting to H.264 with high quality...")
        import subprocess
        import os
        
        # Use ffmpeg for lossless H.264 conversion
        ffmpeg_cmd = [
            'ffmpeg', '-y', '-i', temp_output,
            '-c:v', 'libx264',
            '-preset', 'veryslow',
            '-qp', '0',  # Truly lossless
            '-pix_fmt', 'yuv444p',  # No chroma subsampling
            output_video
        ]
        
        try:
            subprocess.run(ffmpeg_cmd, check=True, capture_output=True)
            os.remove(temp_output)  # Remove temp file
            print(f"      [OK] Converted to H.264 (lossless)")
        except subprocess.CalledProcessError as e:
            print(f"      [X] FFmpeg conversion failed. Using temp file instead.")
            print(f"      Error: {e.stderr.decode()}")
            # Rename temp to output
            os.rename(temp_output, output_video)
        except FileNotFoundError:
            print(f"      [X] FFmpeg not found. Using temp file instead.")
            os.rename(temp_output, output_video)
    
    print(f"\n[OK] Encoding complete!")
    print(f"  Output file: {output_video}")
    print(f"  Processed {frame_number} frames")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Encode SRT subtitles into video frames using grid-based luminance modulation"
    )
    
    parser.add_argument(
        '--video', '-v',
        required=True,
        help='Input video file path (e.g., video.mp4)'
    )
    
    parser.add_argument(
        '--srt', '-s',
        required=True,
        help='Input SRT subtitle file path (e.g., sous_titres.srt)'
    )
    
    parser.add_argument(
        '--output', '-o',
        default='video_encoded.mp4',
        help='Output video file path (default: video_encoded.mp4)'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Draw grid overlay on video for debugging'
    )
    
    parser.add_argument(
        '--codec',
        default='mp4v',
        help='Video codec fourcc code (default: mp4v)'
    )
    
    args = parser.parse_args()
    
    # Validate input files
    if not os.path.exists(args.video):
        print(f"Error: Video file not found: {args.video}")
        return 1
    
    if not os.path.exists(args.srt):
        print(f"Error: SRT file not found: {args.srt}")
        return 1
    
    try:
        encode_video(args.video, args.srt, args.output, args.debug, args.codec)
        return 0
    except Exception as e:
        print(f"\nError during encoding: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
