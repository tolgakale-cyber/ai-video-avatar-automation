import json
import subprocess
from pathlib import Path

from engine.script_generator import generate_script
from engine.validator import validate_script
from engine.quality_checker import check_quality
from engine.script_reviser import revise_script
from engine.tts_generator import generate_speech
from engine.text_quality import check_script_text_quality
from engine.video_generator import search_and_download_video
from engine.video_clip_builder import create_video_clip


MAX_ATTEMPTS = 5


def get_audio_duration(audio_path):
    command = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(audio_path)
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=True
    )

    return float(result.stdout.strip())


def create_audio_files(script):
    print("\nSeslendirmeler olusturuluyor...\n")

    generate_speech(
        script["introduction"],
        "output/introduction.mp3"
    )

    for index, scene in enumerate(script["scenes"], start=1):
        generate_speech(
            scene["narration"],
            f"output/scene_{index}.mp3"
        )

    generate_speech(
        script["closing"],
        "output/closing.mp3"
    )

    print("Seslendirmeler tamamlandi:")
    print("- output/introduction.mp3")
    print("- output/scene_1.mp3")
    print("- output/scene_2.mp3")
    print("- output/scene_3.mp3")
    print("- output/closing.mp3")


def create_video_section(visual, audio_path, name):
    print(f"\n{name} videosu olusturuluyor...")
    print(f"Visual: {visual}")

    audio_duration = get_audio_duration(audio_path)

    print(
        f"Ses suresi: {audio_duration:.2f} saniye"
    )

    min_duration = max(
        20,
        int(audio_duration) + 2
    )

    print(
        f"Pexels icin minimum video suresi: "
        f"{min_duration} saniye"
    )

    source_video = search_and_download_video(
        visual,
        f"{name}_source.mp4",
        min_duration=min_duration
    )

    output_path = Path("output/videos") / f"{name}.mp4"

    create_video_clip(
        source_video,
        audio_path,
        output_path
    )

    print(
        f"{name} sahnesi hazir: {output_path}"
    )

    return output_path


def create_video_files(script):

    print("\nGorsel videolar ve sahneler olusturuluyor...\n")

    video_dir = Path("output/videos")
    video_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    # Introduction
    create_video_section(
        "professional technology introduction",
        "output/introduction.mp3",
        "introduction"
    )

    # Scenes
    for index, scene in enumerate(
        script["scenes"],
        start=1
    ):
        create_video_section(
            scene["visual"],
            f"output/scene_{index}.mp3",
            f"scene_{index}"
        )

    # Closing
    create_video_section(
        "professional technology closing",
        "output/closing.mp3",
        "closing"
    )

    print("\nTum sahne videolari basariyla olusturuldu.")

    print("\nOlusturulan dosyalar:")

    print("- output/videos/introduction.mp4")
    print("- output/videos/scene_1.mp4")
    print("- output/videos/scene_2.mp4")
    print("- output/videos/scene_3.mp4")
    print("- output/videos/closing.mp4")

def create_final_video():
    video_dir = Path("output/videos")
    concat_file = video_dir / "concat.txt"
    final_output = Path("output/final_video.mp4")

    video_files = [
        "introduction.mp4",
        "scene_1.mp4",
        "scene_2.mp4",
        "scene_3.mp4",
        "closing.mp4"
    ]

    concat_content = "\n".join(
        f"file '{filename}'"
        for filename in video_files
    )

    concat_file.write_text(
        concat_content,
        encoding="ascii"
    )

    print("\nFinal video birlestiriliyor...\n")

    command = [
        "ffmpeg",
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_file),
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "20",
        "-c:a", "aac",
        "-b:a", "128k",
        "-ar", "24000",
        "-movflags", "+faststart",
        str(final_output)
    ]

    subprocess.run(
        command,
        check=True
    )

    print(
        f"\nFinal video hazir: {final_output}"
    )
def main():
    print("AI Video & Avatar Automation")
    print("----------------------------")

    topic = input("Video konusu gir: ")

    print("\nAI ilk senaryoyu hazirliyor...\n")
    script = generate_script(topic)

    for attempt in range(
        1,
        MAX_ATTEMPTS + 1
    ):
        print(
            f"Kontrol dongusu: "
            f"{attempt}/{MAX_ATTEMPTS}\n"
        )

        is_valid, errors = validate_script(
            script
        )

        if not is_valid:
            print(
                "Yapisal dogrulama basarisiz:"
            )

            for error in errors:
                print(f"- {error}")

            if attempt == MAX_ATTEMPTS:
                print(
                    "\nMaksimum duzeltme "
                    "sayisina ulasildi."
                )
                return

            print(
                "\nSenaryo AI tarafindan "
                "duzeltiliyor...\n"
            )

            script = revise_script(
                script,
                errors
            )

            continue

        print(
            "Yapisal dogrulama basarili."
        )

        # Turkce metin kalite kontrolu
        text_issues = check_script_text_quality(
            script
        )

        if text_issues:
            print(
                "Turkce metin kalite kontrolu "
                "basarisiz:"
            )

            for issue in text_issues:
                print(f"- {issue}")

            if attempt == MAX_ATTEMPTS:
                print(
                    "\nMaksimum duzeltme "
                    "sayisina ulasildi."
                )
                return

            print(
                "\nTurkce kalite sorunlari "
                "Reviser'a gonderiliyor..."
            )

            print(
                "Senaryo AI tarafindan "
                "duzeltiliyor...\n"
            )

            script = revise_script(
                script,
                text_issues
            )

            continue

        print(
            "AI kalite kontrolu yapiliyor...\n"
        )

        quality = check_quality(script)

        if not quality.get(
            "approved",
            False
        ):
            issues = quality.get(
                "issues",
                []
            )

            print(
                "Kalite kontrolu basarisiz:"
            )

            for issue in issues:
                print(f"- {issue}")

            if attempt == MAX_ATTEMPTS:
                print(
                    "\nMaksimum duzeltme "
                    "sayisina ulasildi."
                )
                return

            print(
                "\nCritic sorunlari "
                "Reviser'a gonderiliyor..."
            )

            print(
                "Senaryo AI tarafindan "
                "duzeltiliyor...\n"
            )

            script = revise_script(
                script,
                issues
            )

            continue

        print(
            "Senaryo tum kontrollerden "
            "basariyla gecti.\n"
        )

        print(
            json.dumps(
                script,
                ensure_ascii=False,
                indent=2
            )
        )

        # Sesleri olustur
        create_audio_files(script)

        # Pexels videolari + sesleri olustur
        create_video_files(script)
        # Final videoyu birlestir
        create_final_video()
        print(
            "\nVideo sahneleri basariyla "
            "olusturuldu."
        )

        return


if __name__ == "__main__":
    main()