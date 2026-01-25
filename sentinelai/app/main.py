from fastapi import FastAPI

app = FastAPI(title="SentinelAI API Gateway")

@app.get("/")
def root():
    return {"message": "SentinelAI API Gateway Running"}

@app.get("/health")
def health():
    return {"status": "healthy"}
