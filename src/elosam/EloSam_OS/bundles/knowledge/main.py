import json
import sqlite3
import time
from pathlib import Path


DB_PATH = Path("data") / "knowledge.db"


def connect():
    DB_PATH.parent.mkdir(exist_ok=True)
    return sqlite3.connect(DB_PATH)


async def activate(resolver, transport, logger):
    with connect() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS knowledge (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                metadata TEXT,
                created_at REAL NOT NULL,
                updated_at REAL NOT NULL
            )
            """
        )

    logger.info("Knowledge Engine ativado.")


def knowledge_store(
    resolver,
    key: str,
    value,
    metadata=None,
):
    now = time.time()

    with connect() as connection:
        existing = connection.execute(
            "SELECT created_at FROM knowledge WHERE key = ?",
            (key,),
        ).fetchone()

        created_at = existing[0] if existing else now

        connection.execute(
            """
            INSERT OR REPLACE INTO knowledge
            (
                key,
                value,
                metadata,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                key,
                json.dumps(
                    value,
                    ensure_ascii=False,
                ),
                json.dumps(
                    metadata,
                    ensure_ascii=False,
                )
                if metadata is not None
                else None,
                created_at,
                now,
            ),
        )

    return {
        "success": True,
        "key": key,
    }


def knowledge_retrieve(resolver, key: str):
    with connect() as connection:
        row = connection.execute(
            """
            SELECT value, metadata, created_at, updated_at
            FROM knowledge
            WHERE key = ?
            """,
            (key,),
        ).fetchone()

    if not row:
        return {
            "found": False,
            "key": key,
        }

    return {
        "found": True,
        "key": key,
        "value": json.loads(row[0]),
        "metadata":
            json.loads(row[1])
            if row[1]
            else None,
        "created_at": row[2],
        "updated_at": row[3],
    }
