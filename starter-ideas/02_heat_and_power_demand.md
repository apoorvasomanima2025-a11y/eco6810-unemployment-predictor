# Starter Idea - Heat And Power Demand

## Why This Is Interesting

Extreme heat affects electricity demand in visible and policy-relevant ways. This gives you a clean economic question with a strong time-series structure.

## Likely Project Type

Predictive

## Core Question

Can weather variables help predict daily electricity demand or peak demand in one state?

## Good Stakeholder

A state electricity utility, load dispatch center, or energy planning team.

## Likely Main Metric

Your main metric could be:

- MAE
- RMSE
- or MAPE on daily demand or daily peak demand

## Simple Baseline

Use a simple baseline first:

- yesterday's demand
- or last week's same-day demand

## Likely Data Sources

- state-level electricity demand series
- IMD or other weather data
- calendar controls such as weekends and holidays

## First 24-Hour Feasibility Check

- pick one state
- confirm you can get a continuous demand series
- check whether the weather data can be matched by date

## Main Risk

Demand data and weather data may not line up neatly in geography or timing. If matching is messy, reduce the time window or focus on one clean state.

## How To Keep It Small

Start with:

- one state
- one summer period
- one simple target like daily peak demand

That is enough to make the project manageable.
