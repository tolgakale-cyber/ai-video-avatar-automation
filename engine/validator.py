import re


def validate_script(script):
    errors = []

    if not isinstance(script, dict):
        return False, ["Senaryo geçerli bir JSON nesnesi değil."]

    if not script.get("title"):
        errors.append("Başlık eksik.")

    if not script.get("introduction"):
        errors.append("Giriş metni eksik.")

    scenes = script.get("scenes")

    if not isinstance(scenes, list):
        errors.append("Sahneler bulunamadı.")
    elif len(scenes) != 3:
        errors.append("Senaryo tam olarak 3 sahne içermeli.")
    else:
        for index, scene in enumerate(scenes, start=1):
            if not isinstance(scene, dict):
                errors.append(f"Sahne {index}: Geçerli bir nesne değil.")
                continue

            if not scene.get("visual"):
                errors.append(f"Sahne {index}: Görsel açıklaması eksik.")

            if not scene.get("narration"):
                errors.append(f"Sahne {index}: Seslendirme metni eksik.")

    if not script.get("closing"):
        errors.append("Kapanış metni eksik.")

    # Tüm senaryoyu metne çevir
    full_text = str(script)

    # Yasaklı yer tutucuları kontrol et
    forbidden_placeholders = [
        "[Adınız]",
        "[Firma Adı]",
        "[Şirket Adı]",
        "[Marka Adı]"
    ]

    for placeholder in forbidden_placeholders:
        if placeholder.lower() in full_text.lower():
            errors.append(
                f"Yasaklı yer tutucu bulundu: {placeholder}"
            )

    # Kaynaksız yüzde iddialarını kontrol et
    percentage_pattern = r"%\s*\d+(?:[.,]\d+)?|\d+(?:[.,]\d+)?\s*%"

    percentages = re.findall(percentage_pattern, full_text)

    if percentages:
        unique_percentages = list(dict.fromkeys(percentages))

        errors.append(
            "Kaynaksız yüzde veya istatistiksel iddia bulundu: "
            + ", ".join(unique_percentages)
        )

    return len(errors) == 0, errors