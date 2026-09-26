from engine.quality_checker import check_quality


test_script = {
    "title": "Yapay Zeka ile Verimlilik",
    "introduction": "Günlük hayatta yapay zeka ne kadar yaygın ve faydalı olduğunu keşfedin.",
    "scenes": [
        {
            "visual": "Bir ofiste çalışanlar yapay zeka destekli bir uygulama kullanıyor.",
            "narration": "Yapay zekanın analiz ettiği veriler iş süreçlerini hızlandırıyor."
        },
        {
            "visual": "Bir ekip bilgisayar ekranındaki raporları inceliyor.",
            "narration": "Çalışanlar raporları inceleyerek daha hızlı kararlar alıyor."
        },
        {
            "visual": "Bir hastanede doktor yapay zeka destekli bir sistemi kullanıyor.",
            "narration": "Yapay zeka hastaların bilgilerini düzenlemeye yardımcı oluyor."
        }
    ],
    "closing": "Yapay zeka günlük hayatta birçok alanda kullanılabiliyor."
}


result = check_quality(test_script)

print("Critic sonucu:")
print(result)