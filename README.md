# AI Payroll System

A multi-entity **payroll automation demo** — a Streamlit HR dashboard, an AI-assisted
processing app, and an email "digital employee" that moves payroll requests through a
human-in-the-loop approval flow.

> **Demo project.** All employees, entities, salaries and figures are **fictional sample
> data**. Credentials are read from a `.env` file (see `.env.example`) — nothing real is
> committed. Point it at your own Gmail + data to run it for real.

---

## What's inside

| App | Run | What it does |
|-----|-----|--------------|
| `dashboard.py` | `streamlit run dashboard.py` | HR dashboard — pending approvals, entity-wise payroll summary, receipt-validation queue, analytics. |
| `real_payroll_system.py` | `streamlit run real_payroll_system.py` | Upload timesheets / receipts / Paychex exports / entity configs and run a processing pipeline with a live progress view. |
| `ai_employee.py` | `python ai_employee.py` | Email bot: reads an inbox over IMAP, files each request into a vault (`Needs_Action → Pending_Approval → Approved/Rejected`), sends templated acknowledgements/approvals over SMTP, and generates a sample payroll workbook. |

## The approval flow

```
Incoming request  →  Needs_Action  →  Pending_Approval  →  Approved / Rejected  →  Done
                                          │
                              human approves by email/UI
```

A human stays in the loop: the agent never disburses anything on its own — it prepares
the work and routes it for sign-off.

## Tech stack

Python · Streamlit · pandas · openpyxl · IMAP/SMTP (`smtplib` / `imaplib`) · `python-dotenv`

## Getting started

```bash
pip install -r requirements.txt
cp .env.example .env         # then edit .env with your Gmail app password
streamlit run dashboard.py   # or: python ai_employee.py
```

Create a Gmail **App Password** at https://myaccount.google.com/apppasswords (do not use
your normal login password).

## Notes

- `vault/` and `uploaded_files/` are runtime working folders and are gitignored — real
  payroll files never get committed.
- The presentation architecture (LangGraph orchestration, Gemini document intelligence,
  receipt OCR, Paychex integration) is the target design; this repository is the working
  demo of the dashboard + approval workflow.

## License

[MIT](LICENSE)
