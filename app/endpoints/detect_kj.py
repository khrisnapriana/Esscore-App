from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import numpy as np
import cv2 as cv
from app.services.ocr import ocr_kj
from app.utils.logger import log_memory_usage, logger

router = APIRouter()

@router.post("/kj")
async def detect_keys(file: UploadFile = File(...)):
    log_memory_usage()

    if not file.content_type.startswith("image/"):
        return JSONResponse(content={"error": "File yang diunggah bukan gambar."}, status_code=400)

    contents = await file.read()
    image = cv.imdecode(np.frombuffer(contents, np.uint8), cv.IMREAD_COLOR)

    if image is None:
        return JSONResponse(content={"error": "Gambar tidak valid."}, status_code=400)

    detected_text = ocr_kj(image)

    if not detected_text:
        return {"message": "Tidak ada teks yang terdeteksi."}

    processed_results = {str(i+1): [word.strip() for word in line.split(", ")] for i, line in enumerate(detected_text)}
    logger.info(f"Kunci jawaban yang terdeteksi OCR: {processed_results}")

    return {"detected_text": processed_results}