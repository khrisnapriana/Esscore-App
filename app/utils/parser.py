import json

def parse_key_answers(key_answers: str):
    key_answers_dict = json.loads(key_answers)
    parsed_answers = {}
    for k, v in key_answers_dict.items():
        if isinstance(v, dict) and "jawaban" in v and "bobot" in v:
            parsed_answers[str(k)] = {
                "jawaban": [ans.lower().strip() for ans in v["jawaban"]],
                "bobot": v["bobot"]
            }
        else:
            raise ValueError(f"Format input salah pada soal {k}.")
    return parsed_answers