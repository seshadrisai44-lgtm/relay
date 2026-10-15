from fastapi import FastAPI

from app.review import router as review_router

app = FastAPI(title="Project Relay")
app.include_router(review_router)

from app.form import router as form_router

app.include_router(form_router)


@app.get("/health")
def health():
    return {"status": "ok"}
