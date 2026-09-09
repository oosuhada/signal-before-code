# Embedded AI Coach

The coach makes this repository itself the learning interface. It is deliberately not an answer
generator attached to the personal evidence layer.

## Context unlock, not prompt-only safety

The LLM receives different repository data by phase:

```text
pre_attempt
→ learner-facing problem only
→ no expected_signal
→ no answer key
→ no chapter name

approach_committed
→ learner-facing problem + learner's own candidates/guess
→ still no answer key
→ adversarial questions only

post_submission
→ expected pattern + expected signal may unlock
→ relevant textbook sections may unlock
→ reviewer / counterexample / mutation mode
```

This boundary is enforced in Python **before a prompt reaches the provider**. Prompt wording is a
second line of defense, not the only one.

## Google Cloud setup

The configured Google Cloud target is:

```text
flai-oosuhada-20260506
```

The checked-in `.env.example` records only non-secret configuration. Billing and API enablement
remain Cloud-side concerns; `doctor` deliberately does not enumerate billing accounts, projects, or
credentials.

Install the optional Google Gen AI SDK:

```bash
python3 -m pip install -r requirements-ai.txt
```

The preferred path is Vertex AI through Google's standard **Application Default Credentials** (ADC).
The provider delegates authentication to the Google SDK and never shells out to print an access
token:

```bash
export GOOGLE_CLOUD_PROJECT=flai-oosuhada-20260506
export GOOGLE_CLOUD_LOCATION=global
python3 scripts/coach.py doctor
python3 scripts/coach.py doctor --smoke
python3 scripts/coach.py start
```

For a local workstation, configure ADC outside this repository with Google's normal authentication
flow (for example, `gcloud auth application-default login`). No credential file or token is copied
into this repository.

## Optional API-key modes

The provider also supports a Vertex AI Express Mode key or Gemini Developer API key:

```bash
# Vertex AI Express Mode
export GOOGLE_API_KEY=...
python3 scripts/coach.py doctor --backend vertex-api-key --smoke

# Gemini Developer API
export GEMINI_API_KEY=...
python3 scripts/coach.py doctor --backend gemini-api --smoke
```

Do not commit keys. The coach never prints their values.

The default model is `gemini-3.5-flash`. It is configurable through `--model` or environment.

The provider reads these optional process-environment variables:

```text
GOOGLE_API_KEY
GEMINI_API_KEY
GOOGLE_CLOUD_PROJECT
GOOGLE_CLOUD_LOCATION
VERTEX_AI_MODEL
SIGNAL_BEFORE_CODE_GOOGLE_BACKEND
SIGNAL_BEFORE_CODE_MODEL
```

If a trusted project already has a local env file, it can be reused without copying secrets into
this repository:

```bash
python3 scripts/coach.py doctor --env-file /absolute/path/to/project/.env
python3 scripts/coach.py start --env-file /absolute/path/to/project/.env
```

Only the variable names above are accepted from that file. Other entries are ignored and secret
values are never printed.

`doctor` reports only safe diagnostics: SDK installed, ADC availability, API-key **presence**, and
selected project/model/location. It never returns credential values.

## Interactive flow

```bash
python3 scripts/coach.py start --problem leetcode-704
```

Inside the session:

```text
/status
/commit <my-pattern-guess>
/review
/debug
/oral
/revisit
/quit
```

`/commit` moves from Socratic coaching to adversarial interviewer mode, but the answer key remains
blocked. `/review` should be used only after the learner actually submits or finishes the attempt.
It unlocks review context but deliberately does **not** create `solved`, `hint_free`, or mastery
evidence.

`/oral` is available only after review unlock and uses the expected pattern/reference material to
run an algorithm-defense interview. `/revisit` deliberately hides prior reference-bearing chat
history again so recall is tested rather than replayed.

Actual evidence remains the job of [`../scripts/attempt.py`](../scripts/attempt.py).

## Local session logs

Interactive chat logs live under `.signal-before-code/coach/`, which Git ignores. They are scratch
context, not learner achievement.

## Provider references

The implementation follows Google's current `google-genai` `generate_content` interface and keeps
the model configurable. Google documents Application Default Credentials for Vertex AI and supports
`gemini-2.5-flash` in the global location.
