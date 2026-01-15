import re

def extract_price_from_text(text: str) -> float:

    match = re.search(r"[\d.,]+", text)
    if not match:
        raise ValueError(f"Не удалось извлечь цену из: {text}")
    return float(match.group().replace(",", "."))