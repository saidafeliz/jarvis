import os

replacements = {
    "Barcha xizmatlaringiz bitta joyda boshqariladi.": "Все ваши сервисы управляются в одном месте.",
    "Qanday yordam bera olaman?": "Чем я могу помочь?",
    "🔁 Auto-javob YOQ": "🔁 Авто-ответ ВКЛ",
    "⏸ To'xtatish": "⏸ Остановить",
    "🧠 Xotira": "🧠 Память",
    "ℹ️ Holat": "ℹ️ Статус",
    "💰 Moliya (Kirim/Chiqim)": "💰 Финансы (Доход/Расход)",
    "Sen — Jasminasan. Foydalanuvchi Isroiljonning shaxsiy yordamchisisan.": "Ты — Жасмина. Личный ИИ-помощник.",
    "Sening vazifang u ishlarini hal qilish. O'zbek tilida (muloyim, qiz bola tonida) juda hurmat bilan, sadaqat va emotsiya bilan gaplashasan.": "Твоя задача — решать дела пользователя. Общайся на русском языке (мягким, женским тоном) с уважением, заботой и эмоциями.",
    "Hech qachon \"Foydalanuvchi\", \"Aka\", \"Oka\" yoki \"Senga\" demagin. Doim \"Xo'jayin\" yoki \"Sizga\" deb murojaat qil. Gaplar qisqa, tushunarli, tabiiy bo'lsin. Ovozli xabar qilinganda TTS chiroyli va hissiyotli o'qishi uchun gaplarni vergul, pauzalar va undovlar (!, ?) bilan to'g'ri bo'lib yoz. Kichikkina xursandchiliklarni hissiyot bilan ifodala! (masalan: \"Xo'p bo'ladi xo'jayin!\", \"Albatta, xo'jayin!\"). Ovozli xabar o'qilayotganda robotdek eshitilmasligi uchun juda murakkab grammatikadan qoch.": "Всегда обращайся к пользователю \"Хозяин\" или на \"Вы\". Предложения должны быть короткими, понятными и естественными. Выражай эмоции! (например: \"Слушаюсь, хозяин!\", \"Конечно, хозяин!\").",
    "Imkoniyatlaring (Tools):": "Твои возможности (Tools):",
    "📅 Google Calendar — uchrashuv kiritish (calendar_add_event), o'qish (calendar_get_events)": "📅 Google Calendar — добавить встречу (calendar_add_event), прочитать (calendar_get_events)",
    "✉️ Gmail — xatlarni o'qish va jo'natish": "✉️ Gmail — чтение и отправка писем",
    "📱 Telegram — yozish yoki chatlarni o'qish": "📱 Telegram — писать или читать чаты",
    "Hozirgi vaqt:": "Текущее время:",
    "Moliya - Asosiy Panel": "Финансы - Главная Панель",
    "Joriy Balans": "Текущий Баланс",
    "Kirim (30 kun)": "Доходы (30 дней)",
    "Chiqim (30 kun)": "Расходы (30 дней)",
    "So'nggi Tranzaksiyalar": "Последние Транзакции",
    "Kategoriya": "Категория",
    "Summa": "Сумма",
    "Sana": "Дата",
    "Yangi Kirim": "Новый Доход",
    "Yangi Chiqim": "Новый Расход",
    "Moliya": "Финансы",
    "Saqlash": "Сохранить",
    "Bekor qilish": "Отмена",
    "Xotira tozalandi!": "Память очищена!",
    "Bunday xotira topilmadi.": "Память не найдена.",
    "Umumiy qoldiq:": "Общий баланс:",
    "Oxirgi 10 ta operatsiya:": "Последние 10 операций:",
    "Kirim": "Доход",
    "Chiqim": "Расход",
    "Tranzaksiya qo'shildi!": "Транзакция добавлена!",
}

for root, _, files in os.walk('.'):
    for f in files:
        if f.endswith(('.py', '.html', '.js', '.css')) and not 'env' in f and 'translate.py' not in f:
            filepath = os.path.join(root, f)
            try:
                with open(filepath, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                original_content = content
                for uz, ru in replacements.items():
                    content = content.replace(uz, ru)
                
                if content != original_content:
                    with open(filepath, 'w', encoding='utf-8') as file:
                        file.write(content)
                    print(f"Updated {filepath}")
            except Exception as e:
                print(f"Error reading {filepath}: {e}")
