import json
import urllib.request


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:7b"


def generate_script(topic):
    prompt = f"""
Sen profesyonel bir kurumsal video senaryo yazarısın.

KONU:
{topic}

Yaklaşık 60-90 saniyelik profesyonel bir Türkçe video senaryosu hazırla.

KURALLAR:
- Doğal, akıcı ve doğru Türkçe kullan.
- Tam olarak 3 sahne oluştur.
- [Adınız], [Firma Adı] veya başka yer tutucular kullanma.
- Kaynak verilmemiş yüzdeler, istatistikler, şirket isimleri veya araştırma sonuçları UYDURMA.
- Doğrulanmamış kesin sayısal iddialarda bulunma.
- Gereksiz tekrar yapma.
- Görsel açıklamaları kısa ve video üretimine uygun yaz.
- Seslendirme metinleri profesyonel ve doğal olsun.
- Markdown kullanma.
- Yalnızca geçerli JSON döndür.
- JSON dışında hiçbir açıklama yazma.

JSON FORMATI:

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
            "temperature": 0.2
        }
    }

    request = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )

    with urllib.request.urlopen(request) as response:
        result = json.loads(response.read().decode("utf-8"))

    script = json.loads(result["response"])

    return script