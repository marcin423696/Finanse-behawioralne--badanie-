# Behavioral Finance Experiment Web Application (Flask / Python)

## Overview
A Flask-based web application designed to conduct behavioral finance experiments investigating decision-making under risk, time pressure, and uncertainty. The platform evaluates framing effects, loss aversion, and prospect theory principles by simulating dynamic capital tracking and recording decision reaction times across controlled experimental conditions.

## Key Features
* **Participant Demographics & Psychometrics**: Captures baseline demographic data (age, gender, field of study) along with self-assessed stress resilience and financial liquidity indicators.
* **Controlled Decision Environment**: Presents structured choices between deterministic and probabilistic options, incorporating a decision threshold question to evaluate individual risk aversion limits.
* **Real-Time Capital & Time Pressure Simulation**: Dynamic client-side timer enforces decision constraints, deducting penalty capital for non-responses (timeouts).
* **Randomized Outcome Realization**: Calculates dynamic capital adjustments based on expected values or probabilistic simulations per question.
* **Session & Data Management**: Utilizes secure Flask session handling and unique UUID assignment for participant identification and record integrity.
* **CSV Result Export**: Automatically logs participant profile, categorical choices (Q0–Q14), decision reaction times (RT0–RT14), and final capital metrics to `wyniki.csv`.

## System Architecture & Flow
[ Intro Form ] --> [ Instructions ] --> [ Question Loop ] --> [ Intermission Break ] --> [ End & CSV Export ]



### Key Functions
* `intro()`: Validates onboarding inputs, generates participant UUID, and initializes tracking states.
* `question()`: Manages question routing, reaction time calculation (`time.time()`), and timeout processing.
* `apply_capital_change()`: Executes capital adjustment logic based on selected option rules and mathematical operators.
* `save_result()`: Appends structured participant decision vectors and reaction time metrics into CSV storage.

## Tech Stack
* **Backend**: Python 3, Flask (Routing, Session Management, Templating)
* **Frontend**: HTML5, CSS3, JavaScript (Client-side Timer & Redirects)
* **Data Storage**: CSV (`wyniki.csv`), UUID, `time`
