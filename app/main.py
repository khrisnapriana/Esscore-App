from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.endpoints import detect_kj, evaluate_score

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(detect_kj.router)
app.include_router(evaluate_score.router)

@app.get("/")
def test():
    return {"message": "API berhasil"}