import os, json, asyncio, logging
from datetime import datetime
import aiosqlite

logger = logging.getLogger("saidaagenda.db")

_db_path = "database.sqlite"

INIT_SQL = """
CREATE TABLE IF NOT EXISTS memories (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    category    TEXT NOT NULL,
    key         TEXT NOT NULL,
    value       TEXT NOT NULL,
    embedding   TEXT,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(category, key)
);

CREATE TABLE IF NOT EXISTS messages (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    role        TEXT NOT NULL,
    content     TEXT NOT NULL,
    source      TEXT DEFAULT 'telegram',
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS transactions (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    type        TEXT NOT NULL,
    amount      REAL NOT NULL,
    category    TEXT NOT NULL,
    description TEXT,
    payment_method TEXT DEFAULT 'naqd',
    currency    TEXT DEFAULT 'UZS',
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_memories_category ON memories(category);
CREATE INDEX IF NOT EXISTS idx_messages_created ON messages(created_at);
CREATE INDEX IF NOT EXISTS idx_transactions_created ON transactions(created_at);
"""

async def init_db():
    try:
        async with aiosqlite.connect(_db_path) as db:
            await db.executescript(INIT_SQL)
            try:
                await db.execute("ALTER TABLE transactions ADD COLUMN payment_method TEXT DEFAULT 'naqd'")
                await db.execute("ALTER TABLE transactions ADD COLUMN currency TEXT DEFAULT 'UZS'")
                await db.commit()
            except Exception:
                pass
        logger.info("✅ DB jadvallar tayyor (SQLite)")
    except Exception as e:
        logger.error(f"❌ DB init xatosi: {e}")
        raise

async def db_save_memory(category: str, key: str, value: str, embedding: list = None):
    try:
        async with aiosqlite.connect(_db_path) as db:
            await db.execute("""
                INSERT INTO memories (category, key, value, embedding, updated_at)
                VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT (category, key) 
                DO UPDATE SET value=?, embedding=?, updated_at=CURRENT_TIMESTAMP
            """, (category, key, value, json.dumps(embedding) if embedding else None, value, json.dumps(embedding) if embedding else None))
            await db.commit()
        return f"✅ Xotiraga saqlandi: [{category}] {key}"
    except Exception as e:
        logger.error(f"db_save_memory xatosi: {e}")
        return f"❌ Сохранитьda xatolik: {e}"

async def db_load_all_memories() -> dict:
    try:
        async with aiosqlite.connect(_db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("SELECT category, key, value FROM memories ORDER BY updated_at DESC") as cursor:
                rows = await cursor.fetchall()
        result = {}
        for row in rows:
            cat = row["category"]
            if cat not in result:
                result[cat] = {}
            result[cat][row["key"]] = row["value"]
        return result
    except Exception as e:
        logger.error(f"db_load_memories xatosi: {e}")
        return {}

async def db_search_memory(query_embedding: list, limit: int = 5) -> list:
    import numpy as np
    try:
        async with aiosqlite.connect(_db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("SELECT category, key, value, embedding FROM memories WHERE embedding IS NOT NULL") as cursor:
                rows = await cursor.fetchall()
        if not rows or not query_embedding:
            return []

        q_vec = np.array(query_embedding)
        scored = []
        for row in rows:
            emb = json.loads(row["embedding"])
            m_vec = np.array(emb)
            sim = float(np.dot(q_vec, m_vec) / (np.linalg.norm(q_vec) * np.linalg.norm(m_vec) + 1e-9))
            scored.append((sim, row["category"], row["key"], row["value"]))

        scored.sort(reverse=True)
        return [(cat, key, val) for _, cat, key, val in scored[:limit]]
    except Exception as e:
        logger.error(f"db_search xatosi: {e}")
        return []

async def db_add_message(role: str, content: str, source: str = "telegram"):
    try:
        async with aiosqlite.connect(_db_path) as db:
            await db.execute(
                "INSERT INTO messages (role, content, source) VALUES (?, ?, ?)",
                (role, content, source)
            )
            await db.commit()
    except Exception as e:
        logger.error(f"db_add_message xatosi: {e}")

async def db_get_history(limit: int = 30) -> list:
    try:
        async with aiosqlite.connect(_db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("SELECT role, content, source, created_at FROM messages ORDER BY created_at DESC LIMIT ?", (limit,)) as cursor:
                rows = await cursor.fetchall()
        return [{"role": r["role"], "parts": [r["content"]], "source": r["source"]} for r in reversed(rows)]
    except Exception as e:
        logger.error(f"db_get_history xatosi: {e}")
        return []

async def db_get_history_display(limit: int = 50) -> list:
    try:
        async with aiosqlite.connect(_db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("SELECT role, content, source, created_at FROM messages ORDER BY created_at DESC LIMIT ?", (limit,)) as cursor:
                rows = await cursor.fetchall()
        return [
            {
                "role": r["role"],
                "parts": [r["content"]],
                "source": r["source"],
                "time": str(r["created_at"])[11:16]
            } for r in reversed(rows)
        ]
    except Exception as e:
        logger.error(f"db_get_history_display xatosi: {e}")
        return []

async def db_clear_history():
    try:
        async with aiosqlite.connect(_db_path) as db:
            await db.execute("DELETE FROM messages")
            await db.commit()
    except Exception as e:
        logger.error(f"db_clear_history xatosi: {e}")

async def db_log_transaction(type: str, amount: float, category: str, description: str = "", payment_method: str = "naqd", currency: str = "UZS") -> str:
    try:
        async with aiosqlite.connect(_db_path) as db:
            await db.execute(
                "INSERT INTO transactions (type, amount, category, description, payment_method, currency) VALUES (?, ?, ?, ?, ?, ?)",
                (type, amount, category, description, payment_method, currency)
            )
            await db.commit()
        return f"✅ Финансыviy yozuv muvaffaqiyatli saqlandi! ({category} guruhiga, to'lov: {payment_method}, {currency})"
    except Exception as e:
        logger.error(f"db_log_transaction xatosi: {e}")
        return f"❌ Финансы yozishda xatolik: {e}"

async def db_get_transactions_raw() -> list:
    try:
        async with aiosqlite.connect(_db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("SELECT id, type, amount, category, description, payment_method, currency, created_at FROM transactions ORDER BY created_at ASC") as cursor:
                rows = await cursor.fetchall()
        return [dict(r) for r in rows]
    except Exception as e:
        logger.error(f"db_get_transactions_raw xatosi: {e}")
        return []

async def db_get_finance_data() -> dict:
    try:
        async with aiosqlite.connect(_db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("SELECT type, amount, category, description, payment_method, currency, created_at FROM transactions ORDER BY created_at DESC") as cursor:
                rows = await cursor.fetchall()
            
        transactions = []
        total_income_uzs = 0; total_expense_uzs = 0
        categories_expense_uzs = {}
        total_income_usd = 0; total_expense_usd = 0
        categories_expense_usd = {}
        payment_methods = {"naqd": 0, "karta": 0}
        
        for r in rows:
            amount = float(r["amount"])
            t_type = r["type"]
            cat = r["category"]
            pm = r["payment_method"] or "naqd"
            curr = r["currency"] or "UZS"
            curr = curr.upper()
            pm = pm.lower()
            
            transactions.append({
                "type": t_type, "amount": amount, "category": cat,
                "description": r["description"], "payment_method": pm, "currency": curr,
                "date": str(r["created_at"])[:16]
            })
            
            if curr == "UZS":
                if t_type == "income": total_income_uzs += amount
                elif t_type == "expense": 
                    total_expense_uzs += amount
                    categories_expense_uzs[cat] = categories_expense_uzs.get(cat, 0) + amount
                    if pm in payment_methods: payment_methods[pm] += amount
            elif curr == "USD":
                if t_type == "income": total_income_usd += amount
                elif t_type == "expense": 
                    total_expense_usd += amount
                    categories_expense_usd[cat] = categories_expense_usd.get(cat, 0) + amount
                
        return {
            "uzs": {
                "income": total_income_uzs,
                "expense": total_expense_uzs,
                "balance": total_income_uzs - total_expense_uzs,
                "expense_by_category": categories_expense_uzs
            },
            "usd": {
                "income": total_income_usd,
                "expense": total_expense_usd,
                "balance": total_income_usd - total_expense_usd,
                "expense_by_category": categories_expense_usd
            },
            "payment_methods": payment_methods,
            "transactions": transactions[:100]
        }
    except Exception as e:
        logger.error(f"db_get_finance_data xatosi: {e}")
        return {"uzs": {"income": 0, "expense": 0, "balance": 0, "expense_by_category": {}}, "usd": {"income": 0, "expense": 0, "balance": 0, "expense_by_category": {}}, "payment_methods": {}, "transactions": []}
