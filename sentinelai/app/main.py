from fastapi import FastAPI, Request
from db.database import SessionLocal, TrafficLog, Alert, init_db
from datetime import datetime, timedelta
from sqlalchemy import func

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

@app.get("/alerts")
def get_alerts():
    db = SessionLocal()
    alerts = db.query(Alert).all()
    db.close()

    return [
        {"ip": a.ip, "reason": a.reason, "timestamp": a.timestamp}
        for a in alerts
    ]

@app.get("/detect")
def detect_attacks():
    db = SessionLocal()

    one_minute_ago = datetime.utcnow() - timedelta(minutes=1)

    results = (
        db.query(TrafficLog.ip, func.count(TrafficLog.id).label("count"))
        .filter(TrafficLog.timestamp >= one_minute_ago)
        .group_by(TrafficLog.ip)
        .all()
    )

    flagged = []

    for ip, count in results:
        if count > 10:
            alert = Alert(ip=ip, reason="High request rate")
            db.add(alert)
            flagged.append(ip)

    db.commit()
    db.close()

    return {"flagged_ips": flagged}
