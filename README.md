# smart-fan-energy-watch

## Overview

Smart Fan Energy Watch is a real-time IoT energy monitoring system built with an ESP32, Supabase, and Streamlit.

The system measures temperature and power usage of a USB desk fan, streams data to the cloud, and visualizes energy consumption, cost impact, and smart-control performance in a live dashboard.

This project demonstrates end-to-end IoT architecture, real-time analytics, and adaptive control logic.

---

## System Architecture

### ESP32 (Edge Device)
- Reads ambient temperature (°C)
- Measures USB fan power draw (W)
- Sends readings to Supabase in real time

### Supabase (Cloud Database)
- Stores time-series data (`fan_readings`)
- Serves as the central data layer

### Streamlit Dashboard (Analytics Layer)
- Polls Supabase live
- Computes energy usage over time
- Compares baseline vs smart usage
- Estimates cost savings
- Displays time-weighted mode breakdown
- Integrates live weather data for adaptive thresholds

---

## What We Measure

- Ambient temperature (°C)
- Power consumption (W)
- Fan mode (LOW / MED / HIGH)
- Timestamp (America/Los_Angeles)

---

## What We Compute

- Energy usage (kWh) from real-time power data
- Baseline energy (constant HIGH mode assumption)
- Energy saved (kWh and %)
- Estimated cost used and cost saved
- Time-weighted distribution of fan modes
- Weather-based dynamic temperature thresholds

---

## Weather-Aware Smart Logic

Using the Open-Meteo API:

- MED threshold = current outdoor temperature (°F)
- HIGH threshold = daily peak temperature − 1°F
- Enforces minimum separation between MED and HIGH thresholds

This enables adaptive control behavior based on real-world weather conditions.

---

## Key Features

- Real-time Supabase integration
- Time-weighted energy integration (irregular sampling safe)
- Live dashboard auto-refresh
- Cost and savings estimation
- Weather-adaptive threshold computation
- Clean dark-mode analytics interface

---

## Future Improvements

- Push dynamic thresholds from dashboard to ESP32
- Add hysteresis-based control logic
- Daily / weekly aggregation summaries
- CO₂ emissions estimation
- Automated energy reports