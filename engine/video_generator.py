import os
from pathlib import Path

import requests


PEXELS_VIDEO_URL = "https://api.pexels.com/videos/search"
OUTPUT_DIR = Path("output/videos")


def search_and_download_video(query, filename, min_duration=20):
    api_key = os.getenv("PEXELS_API_KEY")

    if not api_key:
        raise RuntimeError("PEXELS_API_KEY bulunamadi.")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    headers = {
        "Authorization": api_key
    }

    params = {
        "query": query,
        "per_page": 15,
        "orientation": "landscape",
        "size": "medium"
    }

    response = requests.get(
        PEXELS_VIDEO_URL,
        headers=headers,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    videos = data.get("videos", [])

    if not videos:
        raise RuntimeError(
            f"Pexels video bulamadi: {query}"
        )

    # Önce ses süresine yetecek kadar uzun videoları tercih et.
    suitable_videos = [
        video
        for video in videos
        if video.get("duration", 0) >= min_duration
    ]

    # Yeterince uzun video yoksa mevcut videolar arasından devam et.
    candidates = suitable_videos or videos

    # En uzun videoyu tercih et.
    selected_video = max(
        candidates,
        key=lambda video: video.get("duration", 0)
    )

    video_files = selected_video.get("video_files", [])

    if not video_files:
        raise RuntimeError(
            "Pexels video dosyasi bulunamadi."
        )

    mp4_files = [
        file
        for file in video_files
        if file.get("file_type") == "video/mp4"
    ]

    if not mp4_files:
        raise RuntimeError(
            "Pexels MP4 video dosyasi bulunamadi."
        )

    # 1280x720'ye en yakin dosyayi sec.
    selected_file = sorted(
        mp4_files,
        key=lambda file: (
            abs((file.get("width") or 0) - 1280),
            abs((file.get("height") or 0) - 720)
        )
    )[0]

    video_url = selected_file["link"]

    video_response = requests.get(
        video_url,
        timeout=60
    )

    video_response.raise_for_status()

    output_path = OUTPUT_DIR / filename

    output_path.write_bytes(
        video_response.content
    )

    print(
        f"Video indirildi: {output_path} "
        f"(Pexels ID: {selected_video['id']}, "
        f"sure: {selected_video.get('duration', 0)} sn)"
    )

    return output_path


if __name__ == "__main__":
    search_and_download_video(
        "modern office employees working with computers",
        "test_long_video.mp4",
        min_duration=20
    )