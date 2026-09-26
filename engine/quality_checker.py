import json
import urllib.request


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:7b"


def check_quality(script):
    script_json = json.dumps(
        script,
        ensure_ascii=False,
        indent=2
    )

    prompt = f"""
Sen katı ve detaycı bir Türkçe kurumsal video editörüsün.
Görevin senaryoyu onaylamak değil, gerçek kalite sorunlarını bulmaktır.

Aşağıdaki senaryoyu dikkatlice incele:

{script_json}

Aşağıdaki durumlardan HERHANGİ BİRİ varsa senaryoyu REDDET:

1. Yazım veya dil bilgisi hatası.
2. Doğal olmayan, bozuk veya anlamsız Türkçe.
3. Giriş, sahneler veya kapanış arasında belirgin tekrar.
4. Profesyonel kurumsal anlatıma uymayan ifadeler.
5. Görsel açıklamasında belirsiz veya anlamsız ifade.
6. Seslendirme metninde yapay veya kötü kurulmuş cümle.
7. [Adınız], [Firma Adı] gibi yer tutucular.
8. Kaynağı olmayan kesin yüzde, istatistik veya şirket iddiası.
9. Videonun sonunda "bu videoyu izleyin" gibi bağlama uymayan çağrı.
10. Anlatımın konu dışına çıkması veya kendi içinde çelişmesi.

ÖNEMLİ:
- Küçük görünen dil hatalarını bile görmezden gelme.
- Şüpheli bir cümle varsa onay vermek yerine sorun olarak bildir.
- "approved": true yalnızca senaryo gerçekten temiz,
  doğal, tutarlı ve profesyonelse kullanılmalı.
- Sorunları Türkçe ve kısa şekilde açıkla.
- Senaryoyu yeniden yazma.
- Yalnızca geçerli JSON döndür.
- JSON dışında hiçbir metin yazma.

ÇIKTI FORMATI:

{{
  "approved": false,
  "issues": [
    "Tespit edilen sorun 1",
    "Tespit edilen sorun 2"
  ]
}}

Hiçbir sorun yoksa:

{{
  "approved": true,
  "issues": []
}}
"""

    data = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "options": {
            "temperature": 0.0
        }
    }

    request = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )

    with urllib.request.urlopen(request) as response:
        result = json.loads(response.read().decode("utf-8"))

    return json.loads(result["response"])