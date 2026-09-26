from engine.quality_checker import check_quality


bad_script = {
    "title": "Yapay Zeka ve İş Dünyası",
    "introduction": "Yapay zekanın iş dünyasında nasıl daha verimli hale gelmesi?",
    "scenes": [
        {
            "visual": "Çalışanlar bilgisayar kullanıyor.",
            "narration": "Çalışma zorunluluğu, zaman yönetimi ve verimlilik arasındaki döngü."
        },
        {
            "visual": "Yapay zeka sistemi verileri analiz ediyor.",
            "narration": "Örneğin, yapay zekanın verileri analiz etmesi ve raporlar oluşturması."
        },
        {
            "visual": "Çalışanlar raporlara bakıyor.",
            "narration": "Yapay zeka ile işler daha iyi olması ve çalışanların daha hızlı karar vermesi."
        }
    ],
    "closing": "Bu, iş dünyasının geleceğinin nasıl şekillendiği bir göstergesidir."
}


result = check_quality(bad_script)

print("Critic sonucu:")
print(result)