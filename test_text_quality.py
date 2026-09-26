from engine.text_quality import check_script_text_quality


test_script = {
    "title": "Yapay Zeka ile Verimlilik",
    "introduction": "Yapay zekanın iş dünyasında nasıl kullanıldığını gösteriyoruz.",
    "scenes": [
        {
            "visual": "Bir çalışan yapay zekanın analiz edtiği rapora bakıyor.",
            "narration": "Yapay zeka paci için rapor hazırlıyor."
        },
        {
            "visual": "Çalışanlar bilgisayar ekranlarını inceliyor.",
            "narration": "Bu sistem verileri analiz ediyor ve sonuçları sunuyor."
        },
        {
            "visual": "Bir ekip toplantı yapıyor.",
            "narration": "Çalışanlar kararlar alıyor."
        }
    ],
    "closing": "Yapay zeka iş süreçlerini destekliyor."
}


issues = check_script_text_quality(test_script)

print("Bulunan kalite sorunlari:")

if not issues:
    print("Sorun bulunamadi.")
else:
    for issue in issues:
        print("-", issue)