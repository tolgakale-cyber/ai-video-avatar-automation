import re


COMMON_TYPO_PATTERNS = {
    "edtiği": "ettiği",
    "edtiğini": "ettiğini",
  
    "paci": "hasta",
    "paciye": "hastaya",
    "hastanin": "hastanın",
    "yapay zekanin": "yapay zekanın",
}


def check_text_quality(text):
    issues = []

    if not isinstance(text, str):
        return ["Metin geçerli bir yazı değil."]

    clean_text = " ".join(text.split())

    if not clean_text:
        return ["Metin boş."]

    # Bilinen yazım hataları
    lowered = clean_text.lower()

    for wrong, correct in COMMON_TYPO_PATTERNS.items():
        if wrong in lowered:
            issues.append(
                f"Yazım hatası bulundu: '{wrong}' "
                f"(önerilen: '{correct}')"
            )

    # Yarım cümle kontrolü
    sentences = re.split(r"[.!?]+", clean_text)

    for sentence in sentences:
        sentence = sentence.strip()

        if not sentence:
            continue

        words = sentence.split()

        if len(words) < 3:
            issues.append(
                f"Çok kısa veya eksik cümle: '{sentence}'"
            )

    # Aynı kelimenin aşırı tekrarını kontrol et
    words = re.findall(
        r"\b[\wçğıöşüÇĞİÖŞÜ]+\b",
        lowered
    )

    if len(words) >= 12:
        for word in set(words):
            count = words.count(word)

            if count >= 5 and len(word) > 3:
                issues.append(
                    f"Aşırı kelime tekrarı: '{word}' "
                    f"({count} kez)"
                )

    return issues


def check_script_text_quality(script):
    issues = []

    if not isinstance(script, dict):
        return ["Senaryo geçerli değil."]

    texts = []

    if script.get("title"):
        texts.append(("title", script["title"]))

    if script.get("introduction"):
        texts.append(("introduction", script["introduction"]))

    for index, scene in enumerate(
        script.get("scenes", []),
        start=1
    ):
        if scene.get("visual"):
            texts.append(
                (f"scene_{index}_visual", scene["visual"])
            )

        if scene.get("narration"):
            texts.append(
                (f"scene_{index}_narration", scene["narration"])
            )

    if script.get("closing"):
        texts.append(("closing", script["closing"]))

    for field_name, text in texts:
        field_issues = check_text_quality(text)

        for issue in field_issues:
            issues.append(
                f"{field_name}: {issue}"
            )

    return issues