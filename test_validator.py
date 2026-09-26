from engine.validator import validate_script


test_script = {
    "title": "Yapay Zeka ve İş Dünyası",
    "introduction": "Yapay zeka iş süreçlerinde farklı alanlarda kullanılabilir.",
    "scenes": [
        {
            "visual": "Çalışanlar bilgisayar ekranlarını inceliyor.",
            "narration": "Firma A, yapay zeka destekli sistemleri kullanıyor."
        },
        {
            "visual": "Bir sistem verileri analiz ediyor.",
            "narration": "Çalışanlar analiz sonuçlarını inceliyor."
        },
        {
            "visual": "Bir ekip toplantı gerçekleştiriyor.",
            "narration": "Ekip elde edilen bilgiler üzerinde çalışıyor."
        }
    ],
    "closing": "Yapay zeka, iş süreçlerini destekleyen araçlardan biri olabilir."
}


is_valid, errors = validate_script(test_script)

print("Gecerli mi?:", is_valid)
print("Hatalar:")

for error in errors:
    print("-", error)