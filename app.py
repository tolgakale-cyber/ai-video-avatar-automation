import json

from engine.script_generator import generate_script
from engine.validator import validate_script


def main():
    print("AI Video & Avatar Automation")
    print("----------------------------")

    topic = input("Video konusu gir: ")

    print("\nAI senaryoyu hazirliyor...\n")

    script = generate_script(topic)

    is_valid, errors = validate_script(script)

    if not is_valid:
        print("Senaryo dogrulamadan gecemedi:\n")

        for error in errors:
            print(f"- {error}")

        return

    print("Senaryo dogrulamadan basariyla gecti.\n")
    print(json.dumps(script, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()