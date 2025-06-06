from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
import numpy as np
import cv2 as cv
from app.utils.logger import log_memory_usage, logger
from app.utils.parser import parse_key_answers
from app.services.scoring import evaluate_answers

router = APIRouter()

@router.post("/skor")
async def evaluate(file: UploadFile = File(...), key_answers: str = Form(...)):
    log_memory_usage()
    try:
        key_answers_dict = parse_key_answers(key_answers)

        contents = await file.read()
        image = cv.imdecode(np.frombuffer(contents, np.uint8), cv.IMREAD_COLOR)

        if image is None:
            return JSONResponse(content={"error": "Gambar tidak valid."}, status_code=400)

        results, total_nilai = evaluate_answers(image, key_answers_dict)

        return {"results": results, "total_nilai": total_nilai}

    except Exception as e:
        logger.exception(f"Terjadi kesalahan: {e}")
        return JSONResponse(content={"error": "Kesalahan internal server."}, status_code=500)