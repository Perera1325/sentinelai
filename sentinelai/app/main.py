from fastapi import FastAPI, Request
from db.database import SessionLocal, TrafficLog, Alert, init_db
from datetime import datetime, timedelta
from sqlalchemy import func
import joblib
import pandas as pd

app = FastAPI(title="SentinelAI API Gateway")

# Initialize DB
init_db()

# --------------------------------------------------
# Middleware: Log every request
# --------------------------------------------------
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


# --------------------------------------------------
# Basic endpoints
# --------------------------------------------------
@app.get("/")
def root():
    return {"message": "SentinelAI API Gateway Running"}

@app.get("/health")
def health():
    return {"status": "healthy"}


# --------------------------------------------------
# View traffic logs
# --------------------------------------------------
@app.get("/logs")
def get_logs():
    db = SessionLocal()
    logs = db.query(TrafficLog).all()
    db.close()

    return [
        {"ip": l.ip, "path": l.path, "timestamp": l.timestamp}
        for l in logs
    ]


# --------------------------------------------------
# Rule-based detection (rate abuse)
# --------------------------------------------------
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


# --------------------------------------------------
# View alerts
# --------------------------------------------------
@app.get("/alerts")
def get_alerts():
    db = SessionLocal()
    alerts = db.query(Alert).all()
    db.close()

    return [
        {"ip": a.ip, "reason": a.reason, "timestamp": a.timestamp}
        for a in alerts
    ]


# --------------------------------------------------
# ML-based detection
# --------------------------------------------------
@app.get("/ml-detect")
def ml_detect():
    model = joblib.load("ml/model.joblib")

    db = SessionLocal()
    logs = db.query(TrafficLog).all()
    db.close()

    if not logs:
        return {"message": "No logs"}

    data = [{"ip": l.ip, "timestamp": l.timestamp} for l in logs]
    df = pd.DataFrame(data)

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["minute"] = df["timestamp"].dt.floor("min")

    counts = df.groupby(["ip", "minute"]).size().reset_index(name="count")

    X = counts[["count"]]
    preds = model.predict(X)

    results = []

    for i, row in counts.iterrows():
        results.append({
            "ip": row["ip"],
            "count": int(row["count"]),
            "attack": bool(preds[i])
        })

    return results


# --------------------------------------------------
# GenAI-style explanation endpoint
# --------------------------------------------------
@app.get("/explain")
def explain_attacks():
    model = joblib.load("ml/model.joblib")

    db = SessionLocal()
    logs = db.query(TrafficLog).all()
    db.close()

    if not logs:
        return {"message": "No traffic data available"}

    data = [{"ip": l.ip, "timestamp": l.timestamp} for l in logs]
    df = pd.DataFrame(data)

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["minute"] = df["timestamp"].dt.floor("min")

    counts = df.groupby(["ip", "minute"]).size().reset_index(name="count")

    X = counts[["count"]]
    preds = model.predict(X)

    explanations = []

    for i, row in counts.iterrows():
        if preds[i]:
            explanations.append({
                "ip": row["ip"],
                "explanation":
                f"IP {row['ip']} generated {int(row['count'])} requests in one minute, exceeding normal limits. This indicates possible brute-force, bot activity, or API abuse."
            })

    if not explanations:
        return {"message": "No attacks detected"}

    return explanations
