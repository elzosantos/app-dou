from __future__ import annotations

import json
import os
from dataclasses import dataclass

from dotenv import find_dotenv, load_dotenv

from google.genai import Client


load_dotenv(find_dotenv())


@dataclass(frozen=True)
class GeminiConfig:
    api_key: str
    model: str


def get_gemini_config() -> GeminiConfig:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("A variável GEMINI_API_KEY não foi encontrada no ambiente/.env")

    model = os.getenv("MODEL") or "gemini-2.5-flash"
    return GeminiConfig(api_key=api_key, model=model)


def get_client() -> Client:
    cfg = get_gemini_config()
    return Client(api_key=cfg.api_key)


def generate_content(prompt: str, model: str | None = None) -> str:
    cfg = get_gemini_config()
    client = get_client()
    response = client.models.generate_content(
        model=(model or cfg.model),
        contents=prompt,
    )
    return str(response.text)


def gerar_explicacao_simples(noticia_texto: str) -> str:
    return generate_content(f"Explique de forma simples para um leigo: '{noticia_texto}'")


def gerar_info_complementar_gemini(noticia_texto: str) -> dict[str, str]:
    prompt = f"""
Analise a seguinte notícia e extraia as seguintes informações em formato JSON curto:
Notícia: '{noticia_texto}'
JSON Esperado:
{{
  "ramo_atividade": "Nome do setor principal (ex: Tecnologia, Varejo, Agricultura)",
  "impacto_pequenos_negocios": "Uma frase curta (máx 20 palavras) sobre o impacto positivo ou negativo."
}}
""".strip()

    try:
        text = generate_content(prompt)
        json_str = text.strip().replace("```json", "").replace("```", "")
        data = json.loads(json_str)
        return {
            "ramo_atividade": str(data.get("ramo_atividade", "Não Identificado")),
            "impacto_pequenos_negocios": str(
                data.get("impacto_pequenos_negocios", "Análise temporariamente indisponível.")
            ),
        }
    except Exception:
        return {
            "ramo_atividade": "Não Identificado",
            "impacto_pequenos_negocios": "Análise temporariamente indisponível.",
        }

