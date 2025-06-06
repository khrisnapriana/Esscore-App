from app.services.ocr import ocr_skor
from app.utils.similarity import clean_text, levenshtein_dis, corrected_answer
from fastapi import HTTPException
from app.utils.logger import logger

def evaluate_answers(image, key_answers):
    student_answers = ocr_skor(image)
    if not student_answers:
        return [], 0
    if len(student_answers) != len(key_answers):
        raise HTTPException(status_code=400, detail=f"Jumlah jawaban siswa ({len(student_answers)}) tidak sama dengan jumlah kunci jawaban ({len(key_answers)}).")

    results = []
    total_skor = 0
    total_bobot = sum(v["bobot"] for v in key_answers.values())

    for i, (student_answer, conf_score) in enumerate(student_answers):
        question_num = str(i + 1)
        student_answer = clean_text(student_answer).lower()
        result = "Salah"
        skor = 0

        if question_num in key_answers:
            possible_answers = key_answers[question_num]["jawaban"]
            bobot = key_answers[question_num]["bobot"]

            similarity_raw = max([levenshtein_dis(student_answer, ans) for ans in possible_answers] or [0])
            corrected = corrected_answer(student_answer, possible_answers)
            similarity_final = max([levenshtein_dis(corrected, ans) for ans in possible_answers] or [0])

            if similarity_final == 1:
                result = "Benar"
                skor = int(bobot)

            total_skor += skor

            results.append({
                "Soal": question_num,
                "Jawaban Siswa (OCR)": student_answer,
                "Confident Score": conf_score,
                "Jawaban Siswa (Dikoreksi)": corrected,
                "Kunci Jawaban": possible_answers,
                "Similarity Raw": similarity_raw,
                "Similarity Final": similarity_final,
                "Hasil": result,
                "Bobot": bobot,
                "Skor": skor
            })

            logger.info(f"Soal {question_num} | Jawaban: {student_answer} | Kunci: {possible_answers} | Similarity: {similarity_raw:.2f} | Hasil: {result} | Skor: {skor}")

    total_nilai = (total_skor / total_bobot) * 100 if total_bobot > 0 else 0
    return results, round(total_nilai, 2)