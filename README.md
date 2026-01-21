# 🌱 Soil & Water Conservation (SWC) Decision Support System

## Overview

The **Soil & Water Conservation (SWC) Decision Support System** is a **backend-first, production-grade geospatial decision support platform** built to assist in **scientifically defensible planning of soil and water conservation measures** for agricultural land in India.

The system is designed to strictly follow **ICAR (Indian Council of Agricultural Research)** principles, thresholds, and terminology, and intentionally avoids probabilistic or black-box decision-making. All outputs are **deterministic, auditable, and explainable**.

This repository contains the **core backend engine**, implemented as a **Flask REST API**, which ingests geographic coordinates and land-use information and returns conservation-relevant insights.

---

## Key Objectives

- Determine whether a location is **arable agricultural land**
- Compute key **biophysical factors** relevant to SWC planning
- Recommend **ICAR-approved mechanical SWC measures**
- Assess **soil erosion risk**
- Provide **transparent explanations** for every output
- Maintain strict separation between **core logic** and **future AI components**

---

## Guiding Principles

- **No machine learning** in core decision logic
- **No probabilistic thresholds**
- **No undocumented assumptions**
- **Conservative classifications**
- **ICAR-aligned thresholds**
- **Deterministic outputs**
- **Auditability over optimization**

---

## Technology Stack

### Backend
- **Python 3.x**
- **Flask** – REST API framework

### Geospatial & Scientific Processing
- **Raster-based land cover analysis**
- **Terrain analysis from elevation data**
- **Rule-based inference engines**

### External Data Sources
- ESRI Global Land Cover
- NASA POWER Climate Data
- Mapbox Terrain-RGB Elevation

### Architecture Style
- Modular, rule-driven
- Dataset-agnostic interfaces
- Explicit separation of concerns

---

## High-Level System Architecture

