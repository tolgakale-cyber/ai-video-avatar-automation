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
            if not scene.get("visual"):
                errors.append(f"Sahne {index}: Görsel açıklaması eksik.")

            if not scene.get("narration"):
                errors.append(f"Sahne {index}: Seslendirme metni eksik.")

    if not script.get("closing"):
        errors.append("Kapanış metni eksik.")

    # Tüm senaryoyu metne çevirerek yasaklı ifadeleri kontrol et
    full_text = str(script)

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

    return len(errors) == 0, errors