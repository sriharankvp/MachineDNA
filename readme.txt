# 🧬 MachineDNA — Detecting the Change Before the Failure

> **Machine health monitoring and predictive-maintenance prototype for industrial centrifugal pumps.**

### Team NovaCircuit

**Hackulus '26 — IoT Track**

---

## 🚨 The Problem

Industrial machines often do not fail suddenly.

Before a major failure, a machine may gradually change its normal behaviour:

- Temperature slowly increases
- Vibration begins to rise
- Pressure starts to fall
- Flow rate decreases
- Motor current increases

The machine may still appear to be operating normally during the early stages of this degradation.

Traditional threshold-based monitoring mainly asks:

> **"Has the machine crossed a dangerous limit?"**

But by the time a critical threshold is crossed, valuable time for preventive maintenance may already have been lost.

### Our question is different:

> **"Is the machine becoming abnormal?"**

That is the problem MachineDNA is designed to address.

---

# 💡 Our Solution

**MachineDNA** is an explainable machine-health monitoring and predictive-maintenance prototype that learns the normal behavioural pattern of a specific machine and monitors how that behaviour changes over time.

For our prototype, we selected:

### 🏭 Asset: PUMP-001
### ⚙️ Machine: Industrial Centrifugal Pump

MachineDNA establishes a **machine-specific baseline**, or behavioural fingerprint, using multiple operating parameters.

New telemetry is continuously compared against this baseline to identify progressive behavioural drift.

The system converts this analysis into:

- Machine Health Score
- Drift Debt
- Maintenance Risk
- Parameter-wise drift
- Explainable alerts
- Maintenance recommendations

---

# 🧠 Core Idea

A machine has its own normal behavioural fingerprint.

For example, a healthy pump may normally operate around:

| Parameter | Healthy Baseline |
|---|---:|
| 🌡️ Temperature | 64.9 °C |
| 📳 Vibration | 1.44 mm/s |
| 💧 Pressure | 4.71 bar |
| 🌊 Flow | 95.7 L/min |
| ⚡ Motor Current | 7.27 A |

A single value changing slightly may not necessarily indicate a failure.

However, when **multiple parameters gradually move away from the machine's baseline in a consistent direction**, the combined behaviour becomes meaningful.

MachineDNA focuses on this behavioural change.

---

# 🚀 Key Innovation — Drift Debt

## What is Drift Debt?

**Drift Debt** is our concept for representing the accumulated behavioural deviation of a machine from its normal baseline.

Instead of treating every measurement as an isolated event, MachineDNA considers the overall deviation across monitored parameters.

The concept considers:

- Magnitude of deviation
- Direction of deviation
- Multiple parameters drifting together
- Progressive change from the learned baseline

### Simple idea

```text
Small deviation
      ↓
Persistent deviation
      ↓
Multiple parameters drift
      ↓
Drift Debt increases
      ↓
Machine Health decreases
      ↓
Maintenance Risk increases
````

The machine does not need to suddenly cross a catastrophic threshold for the system to recognize that its behaviour is changing.

---

# 🎯 What Makes MachineDNA Different?

Traditional threshold monitoring:

```text
Temperature > Limit?
        ↓
      ALERT
```

MachineDNA:

```text
How does the machine normally behave?
        ↓
Is its behaviour changing?
        ↓
Are multiple parameters drifting?
        ↓
How significant is the accumulated drift?
        ↓
What is the machine's current health?
        ↓
What maintenance action should be considered?
```

### Our key statement:

> **MachineDNA doesn't just detect abnormal machines — it detects machines becoming abnormal.**

---

# ⚙️ Machine Parameters

MachineDNA monitors five parameters for the centrifugal pump.

| Parameter       | What it represents                | Example degradation behaviour |
| --------------- | --------------------------------- | ----------------------------- |
| 🌡️ Temperature | Motor / machine thermal behaviour | Increasing                    |
| 📳 Vibration    | Mechanical behaviour              | Increasing                    |
| 💧 Pressure     | Hydraulic performance             | Decreasing                    |
| 🌊 Flow Rate    | Pump output                       | Decreasing                    |
| ⚡ Motor Current | Electrical load                   | Increasing                    |

Monitoring multiple parameters together allows the system to identify behavioural patterns rather than relying on a single measurement.

---

# 🔄 System Architecture

```text
┌───────────────────────────┐
│      Pump Telemetry       │
│ Temperature / Vibration   │
│ Pressure / Flow / Current │
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│     Arduino Edge Node     │
│       PUMP-001            │
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│      Data Ingestion       │
│      Telemetry Stream     │
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│     Machine Baseline      │
│    Machine Behaviour      │
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│      MachineDNA Engine    │
│   Behavioural Comparison  │
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│   Drift & Anomaly Engine  │
│       Drift Debt          │
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│    Health & Risk Engine   │
│ Health Score + Risk Level │
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│   Explanation Engine      │
│   Reason + Recommendation │
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│      Streamlit Dashboard  │
│ Health → Risk → Reason    │
│ → Action                  │
└───────────────────────────┘
```

---

# 🧪 Prototype Implementation

The current prototype demonstrates the complete workflow using:

### IoT / Edge Layer

* Arduino UNO
* Wokwi
* Simulated sensor inputs
* Serial telemetry output

### Analytics Layer

* Python
* Pandas
* NumPy
* Behavioural baseline comparison
* Drift analysis

### Visualization Layer

* Streamlit
* Plotly

The physical sensor layer is simulated using Wokwi because the prototype is being demonstrated within the hackathon environment.

The Arduino interface is designed so that the simulated inputs can later be replaced with real machine sensors.

---

# 🔌 Wokwi IoT Prototype

The Wokwi prototype represents the edge acquisition layer of MachineDNA.

Five potentiometers are used to simulate machine parameters:

```text
Potentiometer 1 → Temperature
Potentiometer 2 → Vibration
Potentiometer 3 → Pressure
Potentiometer 4 → Flow
Potentiometer 5 → Motor Current
```

### Arduino Analog Inputs

```text
A0 → Temperature
A1 → Vibration
A2 → Pressure
A3 → Flow
A4 → Motor Current
```

The Arduino converts the simulated sensor values into engineering-style telemetry.

---

# 📡 Telemetry Format

The Arduino also generates a machine-readable telemetry packet.

Format:

```text
DATA,Temperature,Vibration,Pressure,Flow,Current
```

Example:

```text
DATA,67.9,1.81,4.43,92.9,7.86
```

This represents:

```text
Temperature  = 67.9 °C
Vibration    = 1.81 mm/s
Pressure     = 4.43 bar
Flow         = 92.9 L/min
Current      = 7.86 A
```

The same telemetry structure can be used as the interface between the edge device and the analytics layer.

---

# 🖥️ MachineDNA Dashboard

The Streamlit dashboard visualizes the machine's current behavioural condition.

The dashboard provides:

### 📊 Machine Health

A health score representing the current deviation from the machine baseline.

### 📈 Drift Debt

A representation of accumulated behavioural deviation.

### ⚠️ Maintenance Risk

The current risk classification based on machine health.

### 📡 Live Telemetry

Current values for:

* Temperature
* Vibration
* Pressure
* Flow
* Current

### 📉 Parameter Drift Analysis

Each parameter is compared with its baseline to show:

* Baseline value
* Current value
* Percentage change
* Drift status

### 🔧 Maintenance Recommendation

The dashboard provides an explanation and suggested maintenance priority based on the detected machine condition.

---

# 🚦 Machine Health States

MachineDNA demonstrates four progressive states.

## 🟢 Healthy

The machine is operating close to its learned behavioural baseline.

**System response:**

> Continue normal operation and monitoring.

---

## 🟡 Early Drift

The machine is beginning to move away from its normal behavioural fingerprint.

**System response:**

> Increase monitoring and inspect during the next suitable maintenance window.

---

## 🟠 Degrading

Multiple parameters are showing progressive behavioural drift.

**System response:**

> Schedule preventive maintenance and inspect mechanical and hydraulic performance.

---

## 🔴 Critical

Significant behavioural degradation has been detected.

**System response:**

> Prioritize maintenance inspection before continued operation causes further degradation.

---

# 📊 Example Degradation

### Healthy

```text
Temperature : 64.9 °C
Vibration   : 1.44 mm/s
Pressure    : 4.71 bar
Flow        : 95.7 L/min
Current     : 7.27 A
```

### Critical Demonstration State

```text
Temperature : 67.9 °C
Vibration   : 1.81 mm/s
Pressure    : 4.43 bar
Flow        : 92.9 L/min
Current     : 7.86 A
```

The critical demonstration state shows all five monitored parameters moving away from the healthy baseline.

---

# 🧮 Drift Analysis

For each parameter, MachineDNA compares the current value with the machine baseline.

A normalized deviation can be represented as:

```text
Deviation = |Current − Baseline| / Baseline
```

The combined deviation across monitored parameters contributes to the Drift Debt.

The prototype then converts the resulting drift into a machine health representation.

> The current prototype demonstrates behavioural degradation analysis rather than claiming an exact failure timestamp.

---

# 🤖 AI / ML Extension

The current prototype focuses on demonstrating the **MachineDNA behavioural-analysis pipeline**.

The architecture can be extended with machine-learning techniques such as:

* Isolation Forest for anomaly detection
* EWMA for behavioural trend monitoring
* Time-series analysis
* Machine-specific historical models
* Failure-history based risk models

These methods require sufficiently representative historical machine data.

Therefore, the prototype does **not** claim an exact failure prediction time without real historical failure datasets.

---

# 🌐 IoT Deployment Architecture

The current Wokwi prototype demonstrates the edge acquisition layer.

A real-world deployment can replace the simulated inputs with physical sensors.

Future deployment:

```text
Industrial Pump
      ↓
Physical Sensors
      ↓
Arduino / Raspberry Pi
      ↓
MQTT / REST API
      ↓
MachineDNA Backend
      ↓
Database
      ↓
Drift & Anomaly Engine
      ↓
Health & Risk Engine
      ↓
Web Dashboard
```

The same telemetry structure can be maintained between the edge and analytics layers.

---

# 🗄️ Data Architecture

The planned backend can store:

```text
Machine ID
Timestamp
Temperature
Vibration
Pressure
Flow
Motor Current
Health Score
Drift Debt
Risk Level
Maintenance Status
```

A machine-specific history allows the system to continuously improve its understanding of normal behaviour.

---

# 🛠️ Technology Stack

## Edge / IoT

* Arduino UNO
* Wokwi
* Raspberry Pi compatible architecture
* MQTT / API-ready telemetry interface

## Programming

* Python
* C/C++ for Arduino

## Data Processing

* Pandas
* NumPy

## Machine Learning / Analytics

* Scikit-learn
* Isolation Forest
* EWMA
* Trend analysis

## Dashboard

* Streamlit
* Plotly

## Database

* SQLite
* PostgreSQL

---

# 📁 Repository Structure

```text
MachineDNA/
│
├── app.py
├── requirements.txt
├── README.md
│
├── wokwi/
│   ├── diagram.json
│   └── sketch.ino
│
└── screenshots/
    ├── healthy.png
    ├── early_drift.png
    ├── degrading.png
    └── critical.png
```

---

# 🚀 Getting Started

## 1. Clone the repository

```bash
git clone https://github.com/sriharankvp/MachineDNA.git
```

## 2. Enter the project directory

```bash
cd MachineDNA
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Run the dashboard

```bash
python -m streamlit run app.py
```

The Streamlit dashboard will open in your browser.

---

# 📡 Wokwi Setup

Open the Wokwi project containing:

```text
Arduino UNO
+
5 simulated sensor inputs
```

Run the Arduino simulation and observe the serial telemetry.

Example:

```text
======================================
       PUMP-001 LIVE TELEMETRY
       Industrial Centrifugal Pump
======================================

Motor Temperature : 67.9 °C
Pump Vibration    : 1.81 mm/s
Discharge Pressure: 4.43 bar
Flow Rate         : 92.9 L/min
Motor Current     : 7.86 A

STATUS            : CRITICAL
Multiple pump parameters deviating.

Drift Indicators  : 5/5

DATA,67.9,1.81,4.43,92.9,7.86
```

---

# 🧩 Current Prototype vs Future Deployment

| Feature            | Current Prototype      | Future Deployment                             |
| ------------------ | ---------------------- | --------------------------------------------- |
| Machine            | Centrifugal Pump       | Multiple machine types                        |
| Sensor layer       | Wokwi simulation       | Physical sensors                              |
| Edge device        | Arduino UNO            | Arduino / Raspberry Pi                        |
| Telemetry          | Serial / input packet  | MQTT / API                                    |
| Baseline           | Prototype baseline     | Learned historical baseline                   |
| Drift analysis     | Implemented            | Continuous time-series analysis               |
| Dashboard          | Streamlit              | Production web dashboard                      |
| Database           | Prototype architecture | PostgreSQL / industrial data store            |
| ML                 | Architecture-ready     | Trained using real machine data               |
| Failure prediction | Risk estimation        | Future RUL modelling with historical failures |

---

# 🎯 Expected Impact

MachineDNA aims to help maintenance teams move from:

```text
Reactive Maintenance
        ↓
Failure Happens
        ↓
Machine Downtime
```

towards:

```text
Continuous Monitoring
        ↓
Behavioural Drift Detection
        ↓
Maintenance Risk
        ↓
Preventive Action
        ↓
Reduced Unexpected Downtime
```

Potential benefits include:

* Earlier identification of machine degradation
* Better maintenance prioritization
* Reduced unexpected downtime
* Explainable machine-health information
* Machine-specific monitoring
* Scalable monitoring across multiple assets

---

# 🔐 Explainability

MachineDNA does not only display:

> **"Machine unhealthy."**

It also attempts to answer:

> **"Why is the machine becoming unhealthy?"**

For example:

```text
Temperature ↑
Vibration   ↑
Pressure    ↓
Flow        ↓
Current     ↑
      ↓
Progressive behavioural drift
      ↓
Higher maintenance risk
```

This gives maintenance personnel evidence behind the alert rather than only a generic warning.

---

# 🧠 Why Machine-Specific Baselines?

Different machines can have different normal operating characteristics.

A single universal threshold may not accurately represent every machine.

MachineDNA therefore uses the concept of a **machine-specific behavioural fingerprint**.

```text
Machine A → Baseline A
Machine B → Baseline B
Machine C → Baseline C
```

This allows future expansion toward monitoring different assets with machine-specific models and operating profiles.

---

# 🔮 Future Scope

### 1. Physical Sensor Integration

Replace Wokwi simulation with real industrial sensors.

### 2. Edge Processing

Use Raspberry Pi or an industrial gateway for local preprocessing.

### 3. Cloud / Server Connectivity

Transmit telemetry using MQTT or REST APIs.

### 4. Historical Machine Database

Store long-term telemetry and maintenance records.

### 5. Machine Learning

Train anomaly and degradation models using real machine data.

### 6. Remaining Useful Life

With sufficient historical failure data, the system could be extended toward Remaining Useful Life (RUL) estimation.

### 7. Multi-Machine Monitoring

Extend MachineDNA from one centrifugal pump to multiple industrial assets.

### 8. Automated Maintenance Workflow

Future versions can integrate maintenance-management systems to automatically create inspection or maintenance tasks.

---

# 👥 Team NovaCircuit

| Member             | Role               |
| ------------------ | ------------------ |
| **Sri Haran B**    | Team Lead / ML     |
| **M Pavithra**     | IoT / Edge         |
| **Nishant P**      | Backend / Database |
| **Subaharini S C** | Frontend           |

---

# 🏆 Hackathon

**Hackulus '26**

**Track:** IoT

**Problem Focus:** Detecting progressive machine degradation before critical failure.

**Selected Machine:** Industrial Centrifugal Pump — PUMP-001

---

# 📌 Key Takeaway

Industrial machines often provide warning signals before a critical failure.

The challenge is recognizing those signals early enough.

MachineDNA builds a behavioural fingerprint of the machine, monitors how that fingerprint changes, accumulates the deviation as **Drift Debt**, and converts the analysis into an understandable machine-health and maintenance signal.

> ## **"We don't just ask whether the machine is abnormal. We ask whether it is becoming abnormal."**

---

# ❤️ Built by Team NovaCircuit

**MachineDNA — Detecting the Change Before the Failure**

> **MachineDNA turns raw telemetry into an early, explainable signal — so maintenance happens before failure, not after.**
