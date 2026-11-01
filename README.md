# ADU Self Service — Student Assistant (Concept Prototype)

A Streamlit prototype styled after the university Self Service screenshots. It includes a portal-style dashboard, left navigation, and a right-side ADU Assistant chat panel. All included student records are fictional.

## Features

- Portal-inspired dashboard and navigation for Student Center, Gradebook, Enrollment, Academic Planning, Make Up Exam Requests, Campus Finances, Academic Records, Attendance, and related sections.
- Student-specific demo sign-in and read-only SQLite lookups.
- Chatbot answers about attendance, outstanding fees/payment deadlines, and make-up/resit exam requests.
- Suggested prompts in the assistant panel.
- Runs without Ollama by default. Optional local Ollama intent classification can be enabled on a personal computer.

## Run locally (Windows)

Open Command Prompt in this folder, then:

```powershell
py -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python create_db.py
streamlit run app.py
```

Demo accounts:

| Student ID | PIN |
|---|---|
| STU1001 | 1234 |
| STU1002 | 2468 |
| STU1003 | 1357 |

Try: “How many absences do I have?”, “How much do I owe?”, “When is my payment deadline?”, or “Was my make-up exam approved?”.

### Optional Ollama (local computer only)

The app works without Ollama. To enable the optional local intent classifier, install Ollama, download a model such as `qwen2.5:3b`, then set the environment variable before launching:

```powershell
$env:OLLAMA_ENABLED="true"
ollama pull qwen2.5:3b
streamlit run app.py
```

Do not enable this setting on Streamlit Community Cloud unless you have separately configured a reachable model endpoint. The hosted version defaults to keyword-based intent matching.

## Publish a public test website (Streamlit Community Cloud)

This project is prepared for Streamlit Community Cloud, but it has **not** been published. To create a public URL:

1. Create a GitHub account (if you do not already have one).
2. Create a new repository, for example `adu-student-assistant-demo`.
3. Upload the contents of this project folder to the repository (the `app.py` file must be at the repository root).
4. Open [Streamlit Community Cloud](https://share.streamlit.io/) and sign in with GitHub.
5. Choose **Create app**, select your repository and branch, set the main file path to `app.py`, and deploy.
6. When deployment finishes, use the generated `*.streamlit.app` URL to invite testers.

The app does not require secrets or Ollama for the hosted demo. Keep the repository public only if you are comfortable making this prototype code and the fictional demo accounts public.

## Important: public-testing limitations

- This is an unofficial concept prototype, not affiliated with or integrated into the university's live systems.
- All student names, IDs, balances, attendance and exam requests are fictional. Never upload real student data or ask students to enter real university credentials.
- Demo credentials are shared and intentionally weak; anyone can sign in to any sample account. This is acceptable only for testing with fictional records.
- SQLite is bundled with the app for demonstration. It is not a multi-user production database.
- Demo PIN authentication is not production-grade. A real deployment needs university SSO, secure session handling, access logging, HTTPS, rate limiting, privacy controls, and a properly managed database.
- Several portal tiles are navigation/design placeholders. Only Attendance, Campus Finances, and Make Up Exam Requests currently show record data in the dashboard; the assistant supports the same core data areas.
- No payment processing, enrollment, grade changes, or university actions are performed.

## Project files

- `app.py` — Streamlit UI, demo authentication, intent classification and fixed read-only database lookups
- `create_db.py` — creates fictional sample data
- `students.db` — sample SQLite database
- `requirements.txt` — Python dependencies
- `.streamlit/config.toml` — portal-style theme

## Updates for the deployed demo

Replace the repository files with this package, including app.py, create_db.py,
and students.db, then reboot the Streamlit app. The bundled database is already
rebuilt; running create_db.py again resets all fictional records.

Chat messages use Streamlit's active theme colors in both Light and Dark modes.
Test both using Streamlit Settings > Theme after signing in.

The sample accounts now use BBA courses from the supplied study plan:
ACC200, BUS204, ECO201, MGT255, MKT200, HRM313, and FIN301.
Course names match the plan; attendance, exam requests, staff and fees remain
fictional. Demo fees are denominated in AED.
Try "How many absences do I have in ACC200?" as STU1001.

Sidebar, Self Service cards, headings and navigation buttons now use active theme colors. Blue primary buttons retain white labels in both themes.
