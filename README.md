# Weather-Adaptive IoT Energy Monitor

## Overview

Weather-Adaptive IoT Energy Monitor is a real-time embedded + cloud system built using an ESP32, Supabase, and Streamlit.

The system measures ambient temperature and fan power usage, applies weather-based adaptive control logic, and visualizes energy consumption and cost impact through a live dashboard.

This project demonstrates end-to-end IoT architecture, real-time telemetry streaming, adaptive decision logic, and cloud-based analytics.

---

## System Architecture

### ESP32 (Edge Device)
- Reads ambient temperature (°C)
- Measures fan power draw (W)
- Fetches weather-informed thresholds
- Determines fan mode (LOW / MED / HIGH) based on adaptive logic
- Streams telemetry data to Supabase

### Supabase (Cloud Layer)
- Stores time-series data (`fan_readings`)
- Serves as backend data source for analytics dashboard

### Streamlit Dashboard (Analytics + Visualization)
- Polls Supabase in real time
- Computes time-weighted energy usage (kWh)
- Compares against baseline constant-watt scenario
- Estimates energy savings and cost impact
- Displays mode distribution and weather thresholds

### Next.js Website (Project Landing Page)
- Built with Next.js and Tailwind CSS
- Introduces the project with a hero section, system overview, and feature highlights
- Embeds the live Streamlit dashboard via inline frame
- Sections: Overview, How It Works, Highlights, Dashboard
- Located in `website/`

---

## Weather-Adaptive Logic

Using the Open-Meteo API:

- MED threshold = current outdoor temperature (°F)
- HIGH threshold = daily peak temperature − 1°F
- Minimum separation enforced between MED and HIGH thresholds

The ESP32 evaluates indoor temperature against these thresholds and determines the appropriate operating mode.

> Note: Current implementation computes and reports adaptive mode decisions. Future revisions will extend this to direct hardware actuation.

---

## Key Features

- Real-time ESP32 telemetry streaming
- Weather-based adaptive control logic
- Time-weighted energy integration
- Baseline vs adaptive energy comparison
- Cost and savings estimation
- Dark-mode interactive dashboard
- Next.js landing page with embedded live dashboard

---

## Tech Stack

- ESP32 (C++)
- Supabase (PostgreSQL backend)
- Streamlit (Python dashboard)
- Next.js + Tailwind CSS (landing page)
- Open-Meteo API (weather data)
- Plotly (dashboard visualization)

---

## Potential Future Improvements

- Direct hardware control of fan speed via PWM or relay
- Hysteresis-based control stabilization
- Historical aggregation (daily / weekly)
- CO₂ emissions estimation
- Deployment of dashboard to cloud hosting