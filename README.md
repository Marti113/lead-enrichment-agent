# Lead Enrichment Agent

A Python agent that automates company research for sales teams. Given a list of company names in a Google Sheet, it automatically enriches each row with company data and an AI-generated fit score — the kind of research a sales rep would otherwise do manually.

## What it does

- Reads company names from a Google Sheet
- Looks up company data (industry, size, location) via the Hunter.io API
- Uses Claude AI to generate a 2-sentence summary and fit rating (Good/Maybe/Poor)
- Writes results back to the sheet automatically

## Why I built it

I wanted to understand how GTM enrichment tools like Clay work under the hood. Instead of just using the tool, I built a lightweight version from scratch in Python to get hands-on with the underlying patterns — API integrations, AI scoring, and automated data pipelines.

## Tech stack

- Python
- Claude AI (Anthropic) — lead scoring and summarization
- Hunter.io API — company data enrichment
- Google Sheets API — input/output layer
- gspread — Google Sheets Python client

## Setup

1. Clone the repo
2. Create a virtual environment and install dependencies:
