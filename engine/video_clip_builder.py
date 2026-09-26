import subprocess
from pathlib import Path


def get_duration(file_path):
    command = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(file_path)
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=True
    )

    return float(result.stdout.strip())


def create_video_clip(video_path, audio_path, output_path):
    video_path = Path(video_path)
    audio_path = Path(audio_path)
    output_path = Path(output_path)

    if not video_path.exists():
        raise FileNotFoundError(
            f"Video bulunamadi: {video_path}"
        )

    if not audio_path.exists():
        raise FileNotFoundError(
            f"Ses bulunamadi: {audio_path}"
        )

    audio_duration = get_duration(audio_path)

    print(
        f"Ses suresi: {audio_duration:.2f} saniye"
    )

    command = [
        "ffmpeg",
        "-y",

        "-stream_loop", "-1",
        "-i", str(video_path),

        "-i", str(audio_path),

        "-map", "0:v:0",
        "-map", "1:a:0",

        "-vf",
        "scale=1280:720:"
        "force_original_aspect_ratio=increase,"
        "crop=1280:720,"
        "fps=30,"
        "setpts=N/(30*TB)",

        "-af",
        "asetpts=N/SR/TB",

        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "20",
        "-pix_fmt", "yuv420p",
        "-r", "30",

        "-c:a", "aac",
        "-b:a", "128k",
        "-ar", "24000",

        "-t", str(audio_duration),

        "-movflags", "+faststart",

        str(output_path)
    ]

    subprocess.run(
        command,
        check=True
    )

    print(
        f"Video olusturuldu: {output_path}"
    )


if __name__ == "__main__":
    create_video_clip(
        "output/videos/test_video.mp4",
        "output/scene_1.mp3",
        "output/scene_1_clip.mp4"
    )