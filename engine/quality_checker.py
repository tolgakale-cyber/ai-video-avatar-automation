import json
import urllib.request


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:14b"


def check_quality(script):
    script_json = json.dumps(
        script,
        ensure_ascii=False,
        indent=2
    )

    prompt = f"""
Sen katı ama adil bir Türkçe video metni editörüsün.

Aşağıdaki kısa kurumsal video senaryosunu incele:

{script_json}

Senaryoyu değerlendirirken TEK SEFERDE genel bir izlenim verme.

Önce aşağıdaki alanların HER BİRİNİ ayrı ayrı kontrol et:

1. title
2. introduction
3. scene 1 visual
4. scene 1 narration
5. scene 2 visual
6. scene 2 narration
7. scene 3 visual
8. scene 3 narration
9. closing

HER ALANDA ŞUNLARI KONTROL ET:

- Cümle Türkçe dil bilgisine uygun mu?
- Cümle doğal bir Türkçe ile yazılmış mı?
- Anlam açık mı?
- Kelimeler yanlış veya garip şekilde kullanılmış mı?
- Cümle yarım veya bozuk mu?
- Özne, yüklem ve ekler birbiriyle uyumlu mu?

ÖRNEK OLARAK ŞU TÜR CÜMLELER MUTLAKA HATA SAYILMALIDIR:

"Bu işlerin yapay zekanın desteklemesiyle nasıl daha verimli hale gelmesi?"

Bu bozuk bir Türkçe cümledir ve REDDEDİLMELİDİR.

"Bu, iş dünyasının geleceğinin nasıl şekillendiği bir göstergesidir."

Bu doğal ve doğru kurulmuş bir Türkçe cümle değildir ve REDDEDİLMELİDİR.

BUNLARIN DIŞINDA ŞUNLARI DA KONTROL ET:

- Giriş, sahneler ve kapanış arasında belirgin tekrar.
- Görsel ile seslendirme arasında ciddi uyumsuzluk.
- Konu dışına çıkan ifadeler.
- Kendi içinde çelişen anlatım.
- Uydurulmuş şirket, kişi, araştırma, yüzde veya istatistik.
- Köşeli parantezli yer tutucular.
- Profesyonel bir videoda açıkça kötü görünecek ifadeler.

ANCAK ŞUNLARI HATA SAYMA:

- Görsel açıklamasının daha ayrıntılı yazılabilecek olması.
- Küçük stil tercihleri.
- Aynı fikrin farklı kelimelerle doğal biçimde desteklenmesi.
- Zorunlu olmayan ayrıntıların bulunmaması.
- Senaryonun sinematik veya kusursuz olmaması.

ÇOK ÖNEMLİ:

Bir alanın Türkçesi bozuksa, senaryonun genel anlamı anlaşılabiliyor olsa bile
"approved": true verme.

Önce tüm alanları tek tek zihninde kontrol et.
Sonra yalnızca nihai JSON sonucunu döndür.

Senaryoyu yeniden yazma.
JSON dışında hiçbir açıklama yazma.

Sorun varsa:

{{
  "approved": false,
  "issues": [
    "Sorunun bulunduğu alan ve kısa açıklaması"
  ]
}}

Gerçekten önemli hiçbir sorun yoksa:

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