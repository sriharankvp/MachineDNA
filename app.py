import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="MachineDNA - Pump",
    page_icon="⚙️",
    layout="wide"
)

st.title("⚙️ MachineDNA — Pump Predictive Maintenance")
st.caption("Detecting the change before the failure")
st.subheader("📡 IoT Telemetry Input")

telemetry_input = st.text_input(
    "Paste Wokwi DATA packet",
    value="DATA,67.9,1.81,4.43,92.9,7.86"
)

if telemetry_input.startswith("DATA,"):

    try:
        values = telemetry_input.split(",")

        if len(values) == 6:

            live_temperature = float(values[1])
            live_vibration = float(values[2])
            live_pressure = float(values[3])
            live_flow = float(values[4])
            live_current = float(values[5])

            st.success("✅ Wokwi telemetry packet accepted")

            st.write(
                f"Temperature: {live_temperature} °C | "
                f"Vibration: {live_vibration} mm/s | "
                f"Pressure: {live_pressure} bar | "
                f"Flow: {live_flow} L/min | "
                f"Current: {live_current} A"
            )

        else:
            st.warning("Invalid telemetry packet.")

    except ValueError:
        st.error("Could not read telemetry values.")
# --------------------------------------------------
# PUMP BASELINE — YOUR WOKWI HEALTHY VALUES
# --------------------------------------------------

baseline = {
    "Temperature": 64.9,
    "Vibration": 1.44,
    "Pressure": 4.71,
    "Flow": 95.7,
    "Current": 7.27
}

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "stage" not in st.session_state:
    st.session_state.stage = 0

# --------------------------------------------------
# SIMULATION BUTTONS
# --------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🟢 Healthy"):
        st.session_state.stage = 0

with col2:
    if st.button("🟡 Early Drift"):
        st.session_state.stage = 1

with col3:
    if st.button("🟠 Degrading"):
        st.session_state.stage = 2

with col4:
    if st.button("🔴 Critical"):
        st.session_state.stage = 3


# --------------------------------------------------
# SIMULATED PUMP STATES
# --------------------------------------------------

states = [

    {
        "Temperature": 64.9,
        "Vibration": 1.44,
        "Pressure": 4.71,
        "Flow": 95.7,
        "Current": 7.27
    },

    {
        "Temperature": 66.0,
        "Vibration": 1.58,
        "Pressure": 4.62,
        "Flow": 94.8,
        "Current": 7.45
    },

    {
        "Temperature": 67.1,
        "Vibration": 1.70,
        "Pressure": 4.52,
        "Flow": 93.8,
        "Current": 7.65
    },

    {
        "Temperature": 67.9,
        "Vibration": 1.81,
        "Pressure": 4.43,
        "Flow": 92.9,
        "Current": 7.86
    }
]

current = states[st.session_state.stage]

# --------------------------------------------------
# DRIFT CALCULATION
# --------------------------------------------------

drifts = []

for parameter in baseline:

    difference = abs(
        current[parameter] - baseline[parameter]
    )

    normal = baseline[parameter]

    drift = difference / normal

    drifts.append(drift)

average_drift = sum(drifts) / len(drifts)

drift_debt = min(
    100,
    average_drift * 100 * 5
)

health = max(
    0,
    100 - drift_debt
)

# Risk
if health >= 80:
    risk = "LOW"
elif health >= 60:
    risk = "MEDIUM"
else:
    risk = "HIGH"


# --------------------------------------------------
# MACHINE STATUS
# --------------------------------------------------

if st.session_state.stage == 0:
    status = "🟢 HEALTHY"

elif st.session_state.stage == 1:
    status = "🟡 EARLY DRIFT"

elif st.session_state.stage == 2:
    status = "🟠 DEGRADING"

else:
    status = "🔴 CRITICAL"


# --------------------------------------------------
# TOP METRICS
# --------------------------------------------------

st.subheader("PUMP-001 — Industrial Centrifugal Pump")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Machine Health",
    f"{health:.0f}%"
)

c2.metric(
    "Drift Debt",
    f"{drift_debt:.0f}/100"
)

c3.metric(
    "Failure Risk",
    risk
)

c4.metric(
    "Machine Status",
    status
)

st.divider()


# --------------------------------------------------
# LIVE TELEMETRY TABLE
# --------------------------------------------------

st.subheader("📡 Live Pump Telemetry")

data = pd.DataFrame({
    "Parameter": list(baseline.keys()),
    "Baseline": list(baseline.values()),
    "Current": list(current.values())
})

st.dataframe(
    data,
    use_container_width=True,
    hide_index=True
)


# --------------------------------------------------
# GRAPHS
# --------------------------------------------------

st.subheader("📈 Machine Behaviour")

chart_col1, chart_col2 = st.columns(2)

parameters = list(baseline.keys())

# Temperature
with chart_col1:

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=["Baseline", "Current"],
            y=[
                baseline["Temperature"],
                current["Temperature"]
            ],
            name="Temperature"
        )
    )

    fig.update_layout(
        title="Motor Temperature (°C)",
        height=300
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# Vibration
with chart_col2:

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=["Baseline", "Current"],
            y=[
                baseline["Vibration"],
                current["Vibration"]
            ],
            name="Vibration"
        )
    )

    fig.update_layout(
        title="Pump Vibration (mm/s)",
        height=300
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


chart_col3, chart_col4 = st.columns(2)

# Pressure
with chart_col3:

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=["Baseline", "Current"],
            y=[
                baseline["Pressure"],
                current["Pressure"]
            ],
            name="Pressure"
        )
    )

    fig.update_layout(
        title="Discharge Pressure (bar)",
        height=300
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# Flow
with chart_col4:

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=["Baseline", "Current"],
            y=[
                baseline["Flow"],
                current["Flow"]
            ],
            name="Flow Rate"
        )
    )

    fig.update_layout(
        title="Flow Rate (L/min)",
        height=300
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# --------------------------------------------------
# DEGRADATION TIMELINE
# --------------------------------------------------

st.divider()

st.subheader("📉 MachineDNA Degradation Timeline")

timeline_health = [
    96,
    82,
    68,
    52
]

timeline_drift = [
    4,
    18,
    32,
    48
]

timeline_labels = [
    "Healthy",
    "Early Drift",
    "Degrading",
    "Critical"
]

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=timeline_labels,
        y=timeline_health,
        mode="lines+markers",
        name="Machine Health"
    )
)

fig.update_layout(
    title="Machine Health as Behaviour Drifts",
    xaxis_title="Machine Condition",
    yaxis_title="Health (%)",
    yaxis=dict(range=[0, 100]),
    height=350
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.caption(
    "MachineDNA tracks progressive behavioural drift instead of waiting "
    "for a sudden failure condition."
)
# --------------------------------------------------
# EXPLANATION
# --------------------------------------------------

st.divider()

# --------------------------------------------------
# PARAMETER DRIFT ANALYSIS
# --------------------------------------------------

st.subheader("🔍 Parameter Drift Analysis")

drift_rows = []

for parameter in baseline:

    base = baseline[parameter]
    now = current[parameter]

    change = ((now - base) / base) * 100

    # Pressure and Flow are healthier when they are higher,
    # while Temperature, Vibration and Current are healthier
    # when they are lower.
    if parameter in ["Pressure", "Flow"]:
        abnormal = now < base
    else:
        abnormal = now > base

    drift_rows.append({
        "Parameter": parameter,
        "Baseline": round(base, 2),
        "Current": round(now, 2),
        "Change": f"{change:+.1f}%",
        "Drift": "⚠️ Drifting" if abnormal else "✓ Normal"
    })

drift_df = pd.DataFrame(drift_rows)

st.dataframe(
    drift_df,
    use_container_width=True,
    hide_index=True
)
st.subheader("🧠 MachineDNA Analysis")

if st.session_state.stage == 0:

    st.success(
        "Pump behaviour is within its learned baseline."
    )

elif st.session_state.stage == 1:

    st.warning(
        "Early behavioural drift detected. "
        "The pump is beginning to move away from its normal fingerprint."
    )

elif st.session_state.stage == 2:

    st.warning(
        "Progressive degradation detected. "
        "Multiple parameters are drifting together."
    )

else:

    st.error(
        "Significant behavioural degradation detected. "
        "Maintenance should be scheduled before failure."
    )


st.info(
    "MachineDNA does not only ask whether a parameter crossed "
    "a fixed threshold. It compares the machine's current behaviour "
    "with its own baseline and measures progressive drift."
)


# --------------------------------------------------
# RECOMMENDATION
# --------------------------------------------------

st.subheader("🔧 Recommended Action")

if st.session_state.stage == 0:

    st.write(
        "Continue normal operation and monitor telemetry."
    )

elif st.session_state.stage == 1:

    st.write(
        "Increase monitoring frequency and inspect the pump "
        "during the next maintenance window."
    )

elif st.session_state.stage == 2:

    st.write(
        "Schedule preventive maintenance and inspect vibration, "
        "bearing condition and hydraulic performance."
    )

else:

    st.write(
        "Schedule maintenance immediately and inspect the pump "
        "before continued operation causes further degradation."
    )


st.caption(
    "MachineDNA turns raw telemetry into an early, explainable signal — "
    "so maintenance happens before failure, not after."
)