import subprocess
import os
import math
import glob

def count_frames(input_file):
    """Count actual frames in a video using ffprobe."""
    try:
        cmd = [
            "ffprobe", "-v", "error",
            "-select_streams", "v:0",
            "-count_frames",
            "-show_entries", "stream=nb_read_frames",
            "-of", "csv=p=0",
            input_file
        ]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return int(result.stdout.strip())
    except Exception as e:
        print(f"⚠️ Could not count frames for {input_file}, defaulting to 100. Error: {e}")
        return 100


    except Exception as e:
        print(f"⚠️ Could not count frames for {input_file}, defaulting to 100. Error: {e}")
        return 100


def make_spritesheet(input_file, fps=12, width=512, chroma="0x00FF00", similarity=0.3, blend=0.1):
    """Convert a green-screen MP4 into a transparent sprite sheet with auto grid size."""
    base, _ = os.path.splitext(input_file)
    output_file = f"{base}_spritesheet.png"

    # Count frames at chosen FPS
    frame_count = count_frames(input_file)
    cmd_fps = [
        "ffprobe", "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=avg_frame_rate",
        "-of", "csv=p=0",
        input_file
    ]
    orig_fps_str = subprocess.run(cmd_fps, stdout=subprocess.PIPE, text=True).stdout.strip()
    num, den = map(int, orig_fps_str.split('/')) if '/' in orig_fps_str else (int(orig_fps_str), 1)
    orig_fps = num / den if den else num

    frame_count = int(frame_count * (fps / orig_fps))

    cols = math.ceil(math.sqrt(frame_count))
    rows = math.ceil(frame_count / cols)

    print(f"🎬 {os.path.basename(input_file)}: {frame_count} frames → grid {cols}x{rows}")

    filter_chain = (
        f"fps={fps},scale={width}:-1,"
        f"colorkey={chroma}:{similarity}:{blend},format=rgba,"
        f"tile={cols}x{rows}"
    )

    cmd = [
        "ffmpeg", "-y", "-i", input_file,
        "-vf", filter_chain,
        output_file
    ]

    subprocess.run(cmd)

    if os.path.isfile(output_file):
        print(f"✅ Saved: {output_file}")
    else:
        print(f"⚠️ Failed to generate {output_file}")


def process_folder(folder, fps=12, width=512):
    """Process all MP4s in a folder."""
    files = glob.glob(os.path.join(folder, "*.mp4"))
    if not files:
        print(f"❌ No .mp4 files found in {folder}")
        return

    for f in files:
        make_spritesheet(f, fps=fps, width=width)


# --- Example usage ---
if __name__ == "__main__":
    folder_path = "C:\\Users\\arjun\\Desktop\\Anime Clciker Vids"  # change to your folder
    process_folder(folder_path, fps=24, width=512)   # UI animations
