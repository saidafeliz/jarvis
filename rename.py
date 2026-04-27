import os

def replace_in_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = content.replace("SaidaAgenda", "SaidaAgenda")
    new_content = new_content.replace("saidaagenda", "saidaagenda")
    new_content = new_content.replace("SAIDA_AGENDA", "SAIDA_AGENDA")

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filepath}")

for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith((".py", ".md", ".sql")):
            if file == "rename.py":
                continue
            replace_in_file(os.path.join(root, file))

# Create .env
env_content = """# ─── MAJBURIY ───
BOT_TOKEN=8778547909:AAEcP2HdyKILabJ4TtA0IQFJvlq_Fz42gfE
OWNER_TELEGRAM_ID=your_telegram_user_id
GEMINI_API_KEY=your_gemini_api_key

# ─── TELEGRAM USERBOT (ixtiyoriy) ───
TG_API_ID=your_api_id
TG_API_HASH=your_api_hash
TG_PHONE=+998901234567
TG_SESSION_STRING=your_session_string

# ─── INSTAGRAM (ixtiyoriy) ───
INSTAGRAM_USER=your_instagram_username
INSTAGRAM_PASS=your_instagram_password

# ─── NOTION (ixtiyoriy) ───
NOTION_TOKEN=your_notion_integration_token
NOTION_DB_ID=your_notion_database_id

# ─── GOOGLE CALENDAR (ixtiyoriy) ───
# Agar Google Calendar ishlatsangiz, credentials.json faylini loyiha papkasiga tashlang.
GOOGLE_CALENDAR_ID=primary

# ─── GMAIL (ixtiyoriy) ───
GMAIL_EMAIL=your_email@gmail.com
GMAIL_APP_PASSWORD=your_16_char_app_password

# ─── SOZLAMALAR ───
VOICE_REPLY=true
MEMORY_PATH=data/memory.json
"""
with open(".env", "w", encoding='utf-8') as f:
    f.write(env_content)
print("Created .env")
