from engine.tts_generator import generate_speech


text = (
    "Merhaba. Bu, yapay zeka destekli video otomasyon "
    "sisteminin ilk seslendirme testidir."
)

output_path = "output/test_voice.mp3"

print("Seslendirme olusturuluyor...")

generate_speech(text, output_path)

print(f"Seslendirme tamamlandi: {output_path}")