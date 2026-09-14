from fastapi import FastAPI
from pydantic import BaseModel

from database import initialize_database, get_connection
from machinedna_engine import analyze_machine


app = FastAPI(
    title="MachineDNA API",
    description="Machine health monitoring and predictive maintenance API",
    version="1.0.0"
)


@app.on_event("startup")
def startup():
    initialize_database()


class Telemetry(BaseModel):
    machine_id: str
    temperature: float
    vibration: float
    pressure: float
    flow: float
    current: float


@app.get("/")
def root():
    return {
        "project": "MachineDNA",
        "asset": "PUMP-001",
        "machine": "Industrial Centrifugal Pump",
        "status": "online"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "MachineDNA Backend"
    }


@app.post("/api/telemetry")
def receive_telemetry(data: Telemetry):

    connection = get_connection()

    connection.execute(
        """
        INSERT INTO telemetry
        (
            machine_id,
            temperature,
            vibration,
            pressure,
            flow,
            current
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            data.machine_id,
            data.temperature,
            data.vibration,
            data.pressure,
            data.flow,
            data.current
        )
    )

    connection.commit()
    connection.close()

    return {
        "status": "success",
        "message": "Telemetry stored successfully",
        "machine_id": data.machine_id
    }


@app.get("/api/analyze/{machine_id}")
def analyze_latest_machine(machine_id: str):

    connection = get_connection()

    rows = connection.execute(
        """
        SELECT
            machine_id,
            timestamp,
            temperature,
            vibration,
            pressure,
            flow,
            current
        FROM telemetry
        WHERE machine_id = ?
        ORDER BY id DESC
        LIMIT 10
        """,
        (machine_id,)
    ).fetchall()

    connection.close()

    if not rows:
        return {
            "status": "error",
            "message": f"No telemetry found for {machine_id}"
        }

    telemetry_history = []

    for row in rows:
        telemetry_history.append({
            "timestamp": row["timestamp"],
            "temperature": row["temperature"],
            "vibration": row["vibration"],
            "pressure": row["pressure"],
            "flow": row["flow"],
            "current": row["current"]
        })

    result = analyze_machine(
        machine_id,
        telemetry_history
    )

    return result


@app.get("/api/history/{machine_id}")
def get_machine_history(machine_id: str):

    connection = get_connection()

    rows = connection.execute(
        """
        SELECT
            id,
            machine_id,
            timestamp,
            temperature,
            vibration,
            pressure,
            flow,
            current
        FROM telemetry
        WHERE machine_id = ?
        ORDER BY id ASC
        LIMIT 50
        """,
        (machine_id,)
    ).fetchall()

    connection.close()

    history = []

    for row in rows:
        history.append({
            "id": row["id"],
            "machine_id": row["machine_id"],
            "timestamp": row["timestamp"],
            "temperature": row["temperature"],
            "vibration": row["vibration"],
            "pressure": row["pressure"],
            "flow": row["flow"],
            "current": row["current"]
        })

    return {
        "machine_id": machine_id,
        "count": len(history),
        "history": history
    }