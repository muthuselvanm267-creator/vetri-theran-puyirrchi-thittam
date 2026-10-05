# PocketSmart AI — Your Smart Budget & Recommendation Assistant

A FastAPI + Google Gemini starter implementation for the PocketSmart AI concept.

## Features
- User registration/login with JWT cookie authentication
- Dashboard
- Home Interior budget planner
- Party Event budget planner
- Jewelry recommendation planner with optional outfit upload
- Recommendation history
- Responsive UI

## Run on Windows
```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```
Edit `.env` and add your Google Gemini API key and a strong `SECRET_KEY`.

```powershell
uvicorn app:app --reload
```
Open http://127.0.0.1:8000

## Notes
The project keeps users/history in memory for demo purposes. Restarting the server clears them. For production, replace the in-memory state with a database and use a production secret.

### Starlette/Jinja TemplateResponse fix
This project uses the current `TemplateResponse(request, template_name, context)` API. This avoids the `TypeError: cannot use 'tuple' as a dict key (unhashable type: 'dict')` error caused by the old TemplateResponse calling convention with newer Starlette versions.
