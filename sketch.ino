// ============================================================
// MachineDNA - Pump IoT Edge Node
// Asset: PUMP-001
// Machine: Industrial Centrifugal Pump
// ============================================================

// Sensor input pins
const int TEMP_PIN = A0;
const int VIBRATION_PIN = A1;
const int PRESSURE_PIN = A2;
const int FLOW_PIN = A3;
const int CURRENT_PIN = A4;


void setup() {

  Serial.begin(9600);

  Serial.println();
  Serial.println("======================================");
  Serial.println("   MachineDNA - Pump IoT Edge Node");
  Serial.println("   Asset   : PUMP-001");
  Serial.println("   Machine : Centrifugal Pump");
  Serial.println("======================================");

  delay(1000);
}


void loop() {

  // ----------------------------------------------------------
  // 1. READ SENSOR INPUTS
  // ----------------------------------------------------------

  int tempRaw = analogRead(TEMP_PIN);
  int vibrationRaw = analogRead(VIBRATION_PIN);
  int pressureRaw = analogRead(PRESSURE_PIN);
  int flowRaw = analogRead(FLOW_PIN);
  int currentRaw = analogRead(CURRENT_PIN);


  // ----------------------------------------------------------
  // 2. CONVERT RAW ADC VALUES TO ENGINEERING VALUES
  // ----------------------------------------------------------

  float temperature =
    55.0 + (tempRaw / 1023.0) * 25.0;

  float vibration =
    0.8 + (vibrationRaw / 1023.0) * 1.7;

  float pressure =
    4.2 + (pressureRaw / 1023.0) * 0.9;

  float flow =
    90.0 + (flowRaw / 1023.0) * 15.0;

  float current =
    6.5 + (currentRaw / 1023.0) * 2.0;


  // ----------------------------------------------------------
  // 3. DISPLAY LIVE MACHINE TELEMETRY
  // ----------------------------------------------------------

  Serial.println();
  Serial.println("======================================");
  Serial.println("       PUMP-001 LIVE TELEMETRY");
  Serial.println("       Industrial Centrifugal Pump");
  Serial.println("======================================");


  Serial.print("Motor Temperature : ");
  Serial.print(temperature, 1);
  Serial.println(" °C");


  Serial.print("Pump Vibration    : ");
  Serial.print(vibration, 2);
  Serial.println(" mm/s");


  Serial.print("Discharge Pressure: ");
  Serial.print(pressure, 2);
  Serial.println(" bar");


  Serial.print("Flow Rate         : ");
  Serial.print(flow, 1);
  Serial.println(" L/min");


  Serial.print("Motor Current     : ");
  Serial.print(current, 2);
  Serial.println(" A");


  Serial.println("--------------------------------------");


  // ----------------------------------------------------------
  // 4. BASIC MACHINE STATUS
  // ----------------------------------------------------------

  bool warning = false;

int driftCount = 0;

if (temperature > 67)
  driftCount++;

if (vibration > 1.8)
  driftCount++;

if (pressure < 4.5)
  driftCount++;

if (flow < 94)
  driftCount++;

if (current > 7.8)
  driftCount++;


if (driftCount == 0) {

  Serial.println("STATUS            : NORMAL");
  Serial.println("Pump operating within baseline.");

}
else if (driftCount <= 2) {

  Serial.println("STATUS            : DEGRADING");
  Serial.println("Progressive behavioural drift detected.");

}
else {

  Serial.println("STATUS            : CRITICAL");
  Serial.println("Multiple pump parameters deviating.");
}

Serial.print("Drift Indicators  : ");
Serial.print(driftCount);
Serial.println("/5");

  Serial.println("======================================");
Serial.print("DATA,");
Serial.print(temperature, 1);
Serial.print(",");
Serial.print(vibration, 2);
Serial.print(",");
Serial.print(pressure, 2);
Serial.print(",");
Serial.print(flow, 1);
Serial.print(",");
Serial.println(current, 2);

  // Wait one second before next telemetry reading
  delay(1000);
}