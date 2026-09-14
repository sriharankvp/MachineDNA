# --------------------------------------------------
# MachineDNA Analysis Engine
# --------------------------------------------------

BASELINES = {
    "PUMP-001": {
        "temperature": 64.9,
        "vibration": 1.44,
        "pressure": 4.71,
        "flow": 95.7,
        "current": 7.27
    }
}


# --------------------------------------------------
# Analyze Machine Behaviour
# --------------------------------------------------

def analyze_machine(machine_id, telemetry_history):

    if machine_id not in BASELINES:
        return {
            "status": "error",
            "message": f"No baseline available for {machine_id}"
        }

    baseline = BASELINES[machine_id]

    if not telemetry_history:
        return {
            "status": "error",
            "message": "No telemetry available"
        }

    # Latest reading
    current = telemetry_history[0]

    # --------------------------------------------------
    # Current Parameter Drift
    # --------------------------------------------------

    drift = {}

    for parameter in baseline:

        baseline_value = baseline[parameter]
        current_value = current[parameter]

        if baseline_value == 0:
            drift_percentage = 0
        else:
            drift_percentage = (
                abs(current_value - baseline_value)
                / baseline_value
            ) * 100

        drift[parameter] = round(drift_percentage, 2)

    average_drift = sum(drift.values()) / len(drift)

    # --------------------------------------------------
    # Detect abnormal parameters
    # --------------------------------------------------

    abnormal_parameters = []

    if current["temperature"] > baseline["temperature"]:
        abnormal_parameters.append("Temperature")

    if current["vibration"] > baseline["vibration"]:
        abnormal_parameters.append("Vibration")

    if current["pressure"] < baseline["pressure"]:
        abnormal_parameters.append("Pressure")

    if current["flow"] < baseline["flow"]:
        abnormal_parameters.append("Flow")

    if current["current"] > baseline["current"]:
        abnormal_parameters.append("Current")

    # --------------------------------------------------
    # Persistence
    # --------------------------------------------------

    abnormal_readings = 0

    for reading in telemetry_history:

        abnormal = False

        if reading["temperature"] > baseline["temperature"]:
            abnormal = True

        if reading["vibration"] > baseline["vibration"]:
            abnormal = True

        if reading["pressure"] < baseline["pressure"]:
            abnormal = True

        if reading["flow"] < baseline["flow"]:
            abnormal = True

        if reading["current"] > baseline["current"]:
            abnormal = True

        if abnormal:
            abnormal_readings += 1

    total_readings = len(telemetry_history)

    persistence = abnormal_readings / total_readings

    # --------------------------------------------------
    # Drift Debt
    # --------------------------------------------------

    base_debt = average_drift * 5

    persistence_bonus = persistence * 10

    drift_debt = min(
        100,
        base_debt + persistence_bonus
    )

    # --------------------------------------------------
    # Machine Health Score
    # --------------------------------------------------

    health_score = max(
        0,
        100 - drift_debt
    )

    health_score = round(health_score, 1)
    drift_debt = round(drift_debt, 1)
    average_drift = round(average_drift, 2)
    persistence = round(persistence * 100, 1)

    # --------------------------------------------------
    # Risk Classification
    # --------------------------------------------------

    if health_score >= 80:

        risk = "LOW"
        status = "HEALTHY"

    elif health_score >= 60:

        risk = "MEDIUM"
        status = "EARLY DRIFT"

    elif health_score >= 40:

        risk = "HIGH"
        status = "DEGRADING"

    else:

        risk = "HIGH"
        status = "CRITICAL"

    # --------------------------------------------------
    # Explanation
    # --------------------------------------------------

    if status == "HEALTHY":

        explanation = (
            "Pump behaviour is within its learned baseline. "
            "No significant persistent behavioural drift detected."
        )

        recommendation = (
            "Continue normal operation and routine monitoring."
        )

    elif status == "EARLY DRIFT":

        explanation = (
            "Early behavioural drift detected. "
            "The pump is beginning to move away from its normal "
            "behavioural fingerprint."
        )

        recommendation = (
            "Increase monitoring and inspect the pump during the "
            "next planned maintenance window."
        )

    elif status == "DEGRADING":

        explanation = (
            "Progressive degradation detected. Multiple parameters "
            "are moving away from the pump's normal fingerprint, "
            "and abnormal behaviour is persisting over recent readings."
        )

        recommendation = (
            "Schedule preventive maintenance and inspect vibration, "
            "bearing condition, hydraulic performance and motor loading."
        )

    else:

        explanation = (
            "Significant behavioural degradation detected. "
            "Persistent abnormal behaviour indicates elevated "
            "maintenance risk."
        )

        recommendation = (
            "Schedule maintenance immediately and investigate the "
            "pump before continued operation causes further degradation."
        )

    # --------------------------------------------------
    # Return Result
    # --------------------------------------------------

    return {
        "machine_id": machine_id,
        "status": status,
        "health_score": health_score,
        "risk": risk,
        "average_drift_percent": average_drift,
        "drift_debt": drift_debt,
        "persistence_percent": persistence,
        "parameter_drift_percent": drift,
        "abnormal_parameters": abnormal_parameters,
        "explanation": explanation,
        "recommendation": recommendation
    }