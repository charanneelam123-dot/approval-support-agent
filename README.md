# Approval Support Agent

[![Checks](https://github.com/charanneelam123-dot/approval-support-agent/actions/workflows/tests.yml/badge.svg)](https://github.com/charanneelam123-dot/approval-support-agent/actions/workflows/tests.yml)

A bounded tool-using support agent with policy checks, an approval queue, and auditable traces.

A focused tool-calling example. For the larger deployed application, see [enterprise-agentic-platform](https://github.com/charanneelam123-dot/enterprise-agentic-platform).

Project by Charan Neelam. Python 3.11+; no third-party packages required.
All bundled business data is fictional.

## Quick start

```bash
git clone https://github.com/charanneelam123-dot/approval-support-agent.git
cd approval-support-agent
python agent.py "Please refund order A100" --output runs/demo.json
python -m unittest discover -s tests -v
```

## Optional live model

Set environment variables in your shell; `.env.example` documents the names
but `.env` files are not automatically loaded. Choose a chat/tool-compatible
model available to your API account.

```powershell
$env:OPENAI_API_KEY = "your-key"
$env:OPENAI_MODEL = "your-model-id"
```

Append `--live` to the demo command. Live mode sends question/context data to
OpenAI and incurs API usage. Missing credentials cause an explicit error.
The adapter uses the [Chat Completions API](https://developers.openai.com/api/reference/resources/chat).

## How it works

```mermaid
flowchart LR
    A[User request] --> B[Bounded planner]
    B --> C[Allowlisted tools]
    C --> D[Policy enforced in Python]
    D --> E[Pending human approval]
    C --> F[JSON audit trace]
```

Default mode is a scripted workflow for reproducible demonstrations. `--live`
enables an LLM tool-calling loop with a six-step budget and at most four calls
per step. Tools validate arguments and enforce refund eligibility independently
of the model. Duplicate proposals are idempotent within one agent instance.

Try A100 (eligible), A200 (expired), A300 (not delivered), and A999 (unknown).
The approval queue is included in JSON output; it never executes a payment.

## Design decisions and limitations

This is a simulation with synthetic orders and an in-memory approval queue.
It has no payment integration or approval execution endpoint. Real deployment
needs customer authentication, per-user order authorization, durable storage,
concurrency controls, redacted traces, and an authenticated reviewer interface.
The final model response may still make unsupported claims; tool outcomes and
the approval queue are the authoritative state.

## Interview walkthrough

Demonstrate an eligible refund, an expired refund, and a disallowed tool call.
Explain why a system prompt cannot replace application-level permissions.

## Validation

Unit tests run without API credentials and include mocked provider behavior.
GitHub Actions runs tests on Python 3.11–3.14. See `docs/validation.md` for the
local validation record. Live provider behavior has not been validated with a
paid API call.

## Portfolio talking point

See `docs/linkedin-draft.md` for an editable project announcement. Use only
results you have reproduced and can explain. Licensed under MIT.
