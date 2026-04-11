# Bethpage Tee Time Analysis — Project Roadmap

## Core Research Question

Is there evidence of automated or non-human booking behavior at Bethpage, and did the April 2025 rule changes reduce it?

---

## Phase 1 — System Baseline

**Objective:** Establish the structure of tee time supply and demand.

**Purpose:** Define what constitutes high-value inventory and typical usage patterns.

### Key Analyses
- Tee time demand by hour of day
- Demand by day of week
- Seasonal trends (year-over-year comparison)
- Total bookings vs cancellations

### Output
- Identification of peak demand windows (high-value inventory)
- Context for interpreting downstream behavioral patterns

---

## Phase 2 — Behavioral Anomalies

**Objective:** Identify patterns inconsistent with standard individual user behavior.

### 2A. Cancellation Behavior

**Metrics:**
- Cancellation rate by hour of day
- Cancellation rate by day of week
- Late cancellation rate (e.g., cancellations within 24 hours)
- Distribution of time between booking and cancellation

**Purpose:**
Assess whether users behave as single-intent participants or exhibit signs of speculative booking.

---

### 2B. Inventory Instability

**Definition:**
Instability = high demand combined with high cancellation rate

**Analysis:**
- Identify time windows where both demand and cancellation rates are elevated
- Compare weekday vs weekend instability patterns

**Purpose:**
Highlight time periods where the booking system is least reliable.

---

## Phase 3 — Booking Timing Analysis

**Objective:** Detect timing patterns consistent with automated booking systems.

### 3A. Booking Speed Relative to Release

**Steps:**
1. Define tee time release rule (e.g., 7 days prior at fixed time)
2. Compute:
   - `time_since_release = booking_timestamp - release_timestamp`

**Analyses:**
- Histogram of bookings within:
  - 0–10 seconds
  - 0–60 seconds
  - 0–5 minutes
- Density of bookings immediately after release

**Purpose:**
Identify clustering of bookings within timeframes unlikely to be achieved manually.

---

### 3B. Pattern Consistency

**Analyses:**
- Repeatability of booking timing patterns across days
- Similarity of booking spikes across weeks

**Purpose:**
Distinguish between human variability and consistent, systematic behavior.

---

## Phase 4 — Policy Impact Evaluation (April 2025)

**Objective:** Assess whether rule changes altered booking and cancellation behavior.

### Data Segmentation
- Pre-policy period: Before April 2025
- Post-policy period: After April 2025

### Comparisons

1. Booking timing:
   - Frequency of near-instant bookings

2. Cancellation behavior:
   - Overall cancellation rate
   - Late cancellation rate

3. Inventory instability:
   - Changes in high-demand/high-cancellation windows

### Purpose
Evaluate whether observed behavioral patterns decrease following policy implementation.

---

## Phase 5 — Synthesis and Interpretation

**Objective:** Integrate findings into a coherent evaluation of system behavior.

### Structure

1. Identify concentration of high-value inventory (Phase 1)
2. Demonstrate behavioral anomalies (Phase 2)
3. Present timing-based evidence (Phase 3)
4. Evaluate changes post-policy (Phase 4)

### Outcome

Formulate a conclusion along the lines of:

- Whether observed behaviors are consistent with automated or coordinated booking
- Whether policy interventions had measurable impact

---

## Key Deliverables

### Required Visualizations
- Demand heatmap (hour x day of week)
- Cancellation rate (normalized, not counts)
- Late cancellation distribution
- Booking timing histogram relative to release
- Pre vs post policy comparison charts

### De-emphasize
- Raw count charts without normalization
- Redundant or descriptive-only plots not tied to core question

---

## Guiding Principle

All analysis should contribute evidence toward evaluating the presence of automated booking behavior and the effectiveness of policy interventions.