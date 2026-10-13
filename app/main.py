from fastapi import FastAPI

app = FastAPI(title="Project Relay")


@app.get("/health")
def health():
    return {"status": "ok"}
