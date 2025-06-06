import re
import Levenshtein

def clean_text(text):
    return re.sub(r'[^a-zA-Z0-9-+xX]', '', text)

def levenshtein_dis(a: str, b: str) -> float:
    distance = Levenshtein.distance(a, b)
    max_len = max(len(a), len(b))
    return 1 - (distance / max_len) if max_len else 0

def corrected_answer(ocr_word, possible_answers, threshold=0.4):
    best_match = ocr_word
    highest = 0
    for ans in possible_answers:
        sim = levenshtein_dis(ocr_word, ans)
        if sim > highest and sim >= threshold:
            best_match = ans
            highest = sim
    return best_match