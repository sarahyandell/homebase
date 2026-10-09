from fastapi import FastAPI

from app.tasks.api import router as tasks_router

app = FastAPI(title="homebase core")
app.include_router(tasks_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
