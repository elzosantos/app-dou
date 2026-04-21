from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any, Iterable


def get_project_root() -> Path:
    # src/backend/database.py -> src/backend -> src -> project root
    return Path(__file__).resolve().parents[2]


def get_db_path() -> Path:
    return get_project_root() / "data" / "diariooficial.db"


def get_connection() -> sqlite3.Connection:
    db_path = get_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn


def inicializar_banco() -> None:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS diariooficial (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            noticia TEXT NOT NULL,
            data TEXT NOT NULL,
            UF TEXT NOT NULL,
            status INTEGER DEFAULT 0
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS resposta_gemini (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            noticia TEXT NOT NULL,
            explicacao TEXT NOT NULL,
            data_noticia TEXT NOT NULL,
            data_explicacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status INTEGER DEFAULT 1
        )
        """
    )

    conn.commit()
    conn.close()


def buscar_noticia_completa(id_noticia: int) -> sqlite3.Row | None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, noticia, data, UF FROM diariooficial WHERE id = ?",
        (id_noticia,),
    )
    noticia = cursor.fetchone()
    conn.close()
    return noticia


def listar_noticias_por_data(data: str) -> list[dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, noticia FROM diariooficial WHERE data = ?", (data,))
    noticias = cursor.fetchall()
    conn.close()
    return [{"id": n["id"], "noticia": n["noticia"]} for n in noticias]


def buscar_resposta_cache(noticia_texto: str) -> str | None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT explicacao FROM resposta_gemini WHERE noticia = ?",
        (noticia_texto,),
    )
    cache = cursor.fetchone()
    conn.close()
    return str(cache["explicacao"]) if cache else None


def salvar_resposta_no_cache(noticia_texto: str, explicacao: str, data_noticia: str) -> None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO resposta_gemini (noticia, explicacao, data_noticia, status)
        VALUES (?, ?, ?, 1)
        """,
        (noticia_texto, explicacao, data_noticia),
    )
    conn.commit()
    conn.close()


def inserir_noticias(lista_noticias: Iterable[tuple[str, str, str, int]]) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO diariooficial (noticia, data, UF, status) VALUES (?, ?, ?, ?)"
    cursor.executemany(query, list(lista_noticias))
    count = cursor.rowcount
    conn.commit()
    conn.close()
    return int(count)

