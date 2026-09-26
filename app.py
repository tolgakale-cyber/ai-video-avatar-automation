import json

from engine.script_generator import generate_script
from engine.validator import validate_script
from engine.quality_checker import check_quality
from engine.script_reviser import revise_script
from engine.tts_generator import generate_speech
from engine.text_quality import check_script_text_quality

MAX_ATTEMPTS = 3


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


def main():
    print("AI Video & Avatar Automation")
    print("----------------------------")

    topic = input("Video konusu gir: ")

    print("\nAI ilk senaryoyu hazirliyor...\n")
    script = generate_script(topic)

    for attempt in range(1, MAX_ATTEMPTS + 1):
        print(f"Kontrol dongusu: {attempt}/{MAX_ATTEMPTS}\n")

        is_valid, errors = validate_script(script)

        if not is_valid:
            print("Yapisal dogrulama basarisiz:")

            for error in errors:
                print(f"- {error}")

            if attempt == MAX_ATTEMPTS:
                print("\nMaksimum duzeltme sayisina ulasildi.")
                return

            print("\nSenaryo AI tarafindan duzeltiliyor...\n")
            script = revise_script(script, errors)
            continue

        print("Yapisal dogrulama basarili.")

        # Turkce metin kalite kontrolu
        text_issues = check_script_text_quality(script)

        if text_issues:
            print("Turkce metin kalite kontrolu basarisiz:")

            for issue in text_issues:
                print(f"- {issue}")

            if attempt == MAX_ATTEMPTS:
                print("\nMaksimum duzeltme sayisina ulasildi.")
                return

            print("\nTurkce kalite sorunlari Reviser'a gonderiliyor...")
            print("Senaryo AI tarafindan duzeltiliyor...\n")

            script = revise_script(script, text_issues)
            continue

        print("AI kalite kontrolu yapiliyor...\n")

        quality = check_quality(script)

        if not quality.get("approved", False):
            issues = quality.get("issues", [])

            print("Kalite kontrolu basarisiz:")

            for issue in issues:
                print(f"- {issue}")

            if attempt == MAX_ATTEMPTS:
                print("\nMaksimum duzeltme sayisina ulasildi.")
                return

            print("\nCritic sorunlari Reviser'a gonderiliyor...")
            print("Senaryo AI tarafindan duzeltiliyor...\n")

            script = revise_script(script, issues)
            continue

        print("Senaryo tum kontrollerden basariyla gecti.\n")
        print(json.dumps(script, ensure_ascii=False, indent=2))

        create_audio_files(script)

        return


if __name__ == "__main__":
    main()