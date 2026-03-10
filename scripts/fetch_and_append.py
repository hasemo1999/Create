# scripts/fetch_and_append.py
import os, datetime, pathlib, openai

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
DST = BASE_DIR / "docs" / "100倍まとめ.md"
THREAD = os.getenv("CHAT_THREAD_ID", "100x")  # 予備ID

openai.api_key = os.getenv("OPENAI_API_KEY")

def fetch_chat_summary():
    today = datetime.date.today().isoformat()
    prompt = f"{today} の 100倍プロジェクト要点を200字でMarkdownに"
    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}]
    )
    return resp.choices[0].message.content.strip()

def append(text):
    DST.parent.mkdir(parents=True, exist_ok=True)
    with DST.open("a", encoding="utf-8") as f:
        f.write(f"\\n\\n## {datetime.date.today()}\\n{text}\\n")

if __name__ == "__main__":
    append(fetch_chat_summary())
