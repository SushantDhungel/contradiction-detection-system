from fastapi import FastAPI

description = """
Healthcare Self-Report vs Metrics API

* **Patient-reported symptoms** (text input)

* **Clinical features** (cholesterol, BP, age)

Your AI detects mismatch risk.
"""
app = FastAPI(
    title="Contradiction-Detection-System-API", description=description, version="0.0.1"
)


@app.get("/")
def main():
    return {"message": "🚀🚀🚀API is running🚀🚀🚀"}
