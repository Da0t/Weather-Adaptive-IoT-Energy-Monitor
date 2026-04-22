# Weather-Adaptive IoT Energy Monitor

## Overview

Weather-Adaptive IoT Energy Monitor is a real-time embedded + cloud system built using an ESP32, Supabase, and Streamlit.

The current prototype focuses on a fan as the case-study device. It streams indoor temperature, mode, and estimated power telemetry from an ESP32 to Supabase, then layers live weather context and energy comparison logic into a Streamlit dashboard.

> Note: Multi-device support is not yet implemented. Generalizing the system beyond the current fan-focused build is a planned extension.

---

## System Architecture

### ESP32 (Edge Device)
- Reads ambient temperature (°C)
- Assigns operating mode (OFF / LOW / MEDIUM / HIGH) from fixed temperature bands
- Maps the mode to an estimated power value (W)
- Streams telemetry to Supabase every 10 seconds

### Supabase (Cloud Layer)
- Stores time-series telemetry (`fan_readings`)
- Serves as the backend data source for the analytics dashboard

### Streamlit Dashboard (Analytics + Visualization)
- Polls Supabase in real time
- Fetches current and peak outdoor temperature from Open-Meteo
- Computes dashboard-side weather comparison thresholds
- Computes time-weighted energy usage (kWh)
- Compares adaptive usage against a fixed-watt baseline
- Estimates energy savings and cost impact in dollars
- Displays mode distribution, weather thresholds, and projected savings

## Weather-Adaptive Logic

In the current prototype, weather-aware comparison logic is calculated in the Streamlit dashboard using Open-Meteo:

- MED threshold = current outdoor temperature (°F)
- HIGH threshold = daily peak temperature − 1°F
- Minimum separation enforced between MED and HIGH thresholds

The ESP32 firmware currently uses fixed indoor temperature bands to assign mode and estimated power, while the dashboard uses live outdoor weather to contextualize the telemetry and compare it against a more adaptive reference.

> Note: Direct hardware actuation and true edge-side weather control are planned future extensions.

---

## Key Features

- Real-time ESP32 telemetry streaming
- Dashboard-side weather context and threshold comparison
- Time-weighted energy integration (kWh)
- Baseline vs adaptive energy comparison
- Cost and savings estimation
- Dark-mode interactive dashboard with demo mode
- Scalable fan count simulation (1–10 devices)
- Preset electricity market rates (US, UK, EU, Australia, Japan)

---

## Tech Stack

- ESP32 (C++)
- Supabase (PostgreSQL backend)
- Streamlit (Python dashboard)
- Open-Meteo API (weather data)
- Plotly (dashboard visualization)

---

## Potential Future Improvements

- Generalize to any device — swap fan for AC unit, heater, pump, etc.
- Direct hardware actuation via PWM or relay
- Hysteresis-based control stabilization
- Multi-device tracking in a single dashboard
- Historical aggregation (daily / weekly / monthly)
- CO2 emissions estimation
- Cloud deployment of the dashboard
