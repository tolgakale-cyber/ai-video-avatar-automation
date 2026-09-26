\# AI Video Automation System



Kullanıcının verdiği bir konudan başlayarak yapay zekâ destekli senaryo üretimi, kalite kontrolü, seslendirme, stok video seçimi ve final video oluşturma süreçlerini otomatikleştiren modüler Python projesi.



\## Proje Hakkında



Sistem, girilen video konusunu yapılandırılmış bir senaryoya dönüştürür. Oluşturulan içerik otomatik kalite kontrolünden geçirilir ve gerekli durumlarda yeniden düzenlenir.



Onaylanan senaryo seslendirilir, sahnelere uygun stok videolar Pexels API üzerinden alınır ve FFmpeg kullanılarak ses ile görüntü birleştirilir. Sürecin sonunda oynatılabilir bir MP4 video otomatik olarak oluşturulur.



\## Pipeline



Konu / Metin  

↓  

AI Senaryo Üretimi  

↓  

Yapısal Doğrulama  

↓  

AI Critic \& Quality Control  

↓  

AI Reviser  

↓  

TTS Seslendirme  

↓  

Pexels Video Seçimi  

↓  

FFmpeg Sahne Oluşturma  

↓  

Final MP4



\## Kullanılan Teknolojiler



\- Python

\- Ollama

\- Qwen 2.5 7B

\- Qwen 2.5 14B

\- Edge TTS

\- Pexels API

\- FFmpeg

\- JSON tabanlı yapılandırılmış senaryo sistemi

\- Git / GitHub



\## AI Kalite Kontrolü



Sistem yalnızca ilk üretilen senaryoyu kullanmaz.



Senaryo; yapı, dil kalitesi ve içerik açısından kontrol edilir. Critic tarafından sorun tespit edilirse geri bildirim Reviser modeline gönderilir ve senaryo yeniden düzenlenir.



Bu döngü, kabul edilebilir bir çıktı elde edilene veya maksimum deneme sayısına ulaşılana kadar devam eder.



\## Video Üretimi



Onaylanan senaryonun giriş, sahne ve kapanış bölümleri ayrı ayrı seslendirilir.



Her bölüm için Pexels üzerinden uygun video materyali alınır. FFmpeg ile video ve ses akışları normalize edilerek sahne klipleri oluşturulur ve son aşamada tek bir MP4 dosyasında birleştirilir.



\## Çıktı



Sistem çalıştırıldığında final video:



`output/final\_video.mp4`



olarak oluşturulur.



\## Durum



Çalışan prototip; senaryo üretimi, otomatik kalite kontrolü, revizyon, Türkçe TTS, Pexels video entegrasyonu ve final MP4 üretimini desteklemektedir.

