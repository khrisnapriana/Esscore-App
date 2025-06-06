import easyocr
from app.utils.merger import merge_words_kj, merge_words_scoring

reader = easyocr.Reader(['id'], gpu=False, model_storage_directory="model")

def ocr_kj(image):
    results = reader.readtext(image, detail=1)
    if not results:
        return []
    results = sorted(results, key=lambda x: x[0][0][1])
    return merge_words_kj(results)

def ocr_skor(image):
    results = reader.readtext(image, detail=1)
    if not results:
        return []
    results = sorted(results, key=lambda x: x[0][0][1])
    return merge_words_scoring(results)