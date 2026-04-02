# Repeatly — Product Spec

**Status:** MVP Built
**Vertical:** Restaurants
**Model:** Self-serve SaaS

## Problem

Restaurant owners get 5-50 reviews/week across Google, Yelp, TripAdvisor. Responding properly takes 5-10 min each. Most skip it or send generic "Thank you!" responses that sound lazy. Negative reviews are hardest — generic responses make things worse.

## Product

Restaurant owners paste a review + their business info → get one contextual, brand-appropriate response in seconds.

## Core Loop

1. Owner enters restaurant profile (name, location, cuisine, dishes, staff, brand voice)
2. Owner pastes a review
3. Agent generates one response matched to the review sentiment
4. Owner copies it, posts it wherever the review lives

## MVP Features

- Business profile form (name, location, cuisine, vibe, popular dishes, staff names, recent context)
- Review input (paste text)
- Brand voice selector (warm, casual, formal, witty)
- Response length selector (short, medium, long)
- Sentiment detection (positive / negative / neutral)
- Mention detection (which dishes/staff the reviewer referenced)
- Single response output with copy button

## Tech Stack

- Streamlit (frontend)
- MiniMax API / Text-01 (LLM)
- Prompt engineering is the core product

## Pricing

| Tier | Price | Features |
|------|-------|----------|
| Free | $0 | 10 reviews/month |
| Starter | $29/month | 100 reviews/month, 1 location |
| Pro | $79/month | Unlimited, brand voice |

## What's Next

- Auth / user accounts
- Save restaurant profiles
- Review history
- Usage tracking / billing
- Google API integration (pull reviews automatically)
- Email digest of new reviews
- Multi-location support

## Files

- `app.py` — Main application
- `requirements.txt` — Dependencies
- `README.md` — Setup instructions
- `SPEC.md` — This spec
