# Starter Idea - Food Price Spike Watch

## Why This Is Interesting

Food prices matter directly for households, inflation tracking, and local policy response. A project like this stays close to everyday economics and gives you a clear prediction target.

## Likely Project Type

Predictive

## Core Question

Can we predict short-term price spikes in one essential food item across a set of markets or districts?

## Good Stakeholder

A mandi planner, district administration team, or food and civil supplies department.

## Likely Main Metric

Your main metric could be:

- RMSE or MAE for next-period price prediction
- or spike-detection accuracy if you define a price spike clearly

## Simple Baseline

Use a naive baseline first:

- tomorrow's price equals today's price
- or next week's price equals this week's price

## Likely Data Sources

- Agmarknet market price data
- weather data for the same places and dates
- holiday or festival calendar if it matters

## First 24-Hour Feasibility Check

- pick one commodity
- pick one state or a small set of districts
- download a small sample
- confirm that dates and prices are usable

## Main Risk

The data may be noisy or inconsistent across markets. If that happens, keep the geography small instead of trying to cover all of India.

## How To Keep It Small

Start with:

- one commodity
- one state
- one clear forecast horizon

That is already enough for a strong student project.
