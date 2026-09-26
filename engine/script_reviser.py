import json
import urllib.request


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:7b"


def revise_script(script, issues):
    script_json = json.dumps(
        script,
        ensure_ascii=False,
        indent=2
    )

    issues_text = "\n".join(
        f"- {issue}" for issue in issues
    )

    prompt = f"""
Sen profesyonel bir Türkçe video senaryosu editörüsün.

Aşağıdaki mevcut senaryoyu incele:

{script_json}

Kalite kontrolünde şu sorunlar tespit edildi:

{issues_text}

GÖREVİN:
Mevcut senaryoyu sıfırdan değiştirmek yerine,
tespit edilen sorunları düzelterek daha doğal,
akıcı ve profesyonel hale getir.

KURALLAR:
- Konuyu ve ana fikri koru.
- Tam olarak 3 sahne kullan.
- Yazım ve dil bilgisi hatalarını düzelt.
- Doğal olmayan Türkçe ifadeleri düzelt.
- Gereksiz tekrarları kaldır.
- Görsel ve seslendirme metinlerini birbirinin kopyası yapma.
- Köşeli parantezli yer tutucular kullanma.
- Şirket, kişi, yüzde veya istatistik uydurma.
- Kaynaksız kesin sayısal iddialar ekleme.
- Kapanışı doğal ve profesyonel hale getir.
- Yalnızca geçerli JSON döndür.
- JSON dışında hiçbir açıklama yazma.

Aynı JSON yapısını koru:

{{
  "title": "Video başlığı",
  "introduction": "Kısa giriş anlatımı",
  "scenes": [
    {{
      "visual": "Sahne 1 görsel açıklaması",
      "narration": "Sahne 1 seslendirme metni"
    }},
    {{
      "visual": "Sahne 2 görsel açıklaması",
      "narration": "Sahne 2 seslendirme metni"
    }},
    {{
      "visual": "Sahne 3 görsel açıklaması",
      "narration": "Sahne 3 seslendirme metni"
    }}
  ],
  "closing": "Kısa ve güçlü kapanış anlatımı"
}}
"""

    data = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "options": {
            "temperature": 0.1
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