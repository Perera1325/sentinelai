from fastapi import FastAPI, Request
from db.database import SessionLocal, TrafficLog, init_db

app = FastAPI(title="SentinelAI API Gateway")

init_db()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    response = await call_next(request)

    db = SessionLocal()
    client_ip = request.client.host
    path = request.url.path

    log = TrafficLog(ip=client_ip, path=path)
    db.add(log)
    db.commit()
    db.close()

    return response

@app.get("/")
def root():
    return {"message": "SentinelAI API Gateway Running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/logs")
def get_logs():
    db = SessionLocal()
    logs = db.query(TrafficLog).all()
    db.close()

    return [
        {"ip": l.ip, "path": l.path, "timestamp": l.timestamp}
        for l in logs
    ]
