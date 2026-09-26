import json

from engine.script_generator import generate_script
from engine.validator import validate_script
from engine.quality_checker import check_quality


MAX_ATTEMPTS = 3


def main():
    print("AI Video & Avatar Automation")
    print("----------------------------")

    topic = input("Video konusu gir: ")

    feedback = None

    for attempt in range(1, MAX_ATTEMPTS + 1):
        print(f"\nAI senaryoyu hazirliyor... ({attempt}/{MAX_ATTEMPTS})\n")

        script = generate_script(topic, feedback)

        is_valid, errors = validate_script(script)

        if not is_valid:
            print("Yapisal dogrulama basarisiz:")

            for error in errors:
                print(f"- {error}")

            feedback = "\n".join(errors)

            if attempt < MAX_ATTEMPTS:
                print("\nHatalar AI'a geri gonderiliyor. Yeniden deneniyor...")
                continue

            print("\nMaksimum deneme sayisina ulasildi.")
            return

        print("Yapisal dogrulama basarili.")
        print("AI kalite kontrolu yapiliyor...\n")

        quality = check_quality(script)

        if not quality.get("approved", False):
            issues = quality.get("issues", [])

            print("Kalite kontrolu basarisiz:")

            for issue in issues:
                print(f"- {issue}")

            feedback = "\n".join(issues)

            if attempt < MAX_ATTEMPTS:
                print("\nKalite sorunlari AI'a geri gonderiliyor. Yeniden deneniyor...")
                continue

            print("\nMaksimum deneme sayisina ulasildi.")
            return

        print("Senaryo tum kontrollerden basariyla gecti.\n")
        print(json.dumps(script, ensure_ascii=False, indent=2))
        return


if __name__ == "__main__":
    main()