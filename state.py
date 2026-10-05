from datetime import datetime

USERS = {}
HISTORY = []


def add_history(user: str, category: str, prompt: str, result: str):
    HISTORY.insert(0, {
        "user": user,
        "category": category,
        "prompt": prompt,
        "result": result,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    })
    del HISTORY[50:]
