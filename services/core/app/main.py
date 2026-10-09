from fastapi import FastAPI

app = FastAPI(title="homebase core")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
