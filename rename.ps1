$files = Get-ChildItem -Path . -Recurse -Include *.py, *.md, *.sql
foreach ($file in $files) {
    $content = Get-Content -Path $file.FullName -Raw -Encoding UTF8
    $newContent = $content.Replace('Jarvis', 'SaidaAgenda').Replace('jarvis', 'saidaagenda').Replace('JARVIS', 'SAIDA_AGENDA')
    if ($content -ne $newContent) {
        Set-Content -Path $file.FullName -Value $newContent -Encoding UTF8 -NoNewline
        Write-Host "Updated $($file.FullName)"
    }
}

$envContent = @"
# ─── MAJBURIY ───
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
"@

Set-Content -Path ".env" -Value $envContent -Encoding UTF8
Write-Host "Created .env"
