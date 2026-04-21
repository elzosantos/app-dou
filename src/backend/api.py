from __future__ import annotations

from fastapi import FastAPI, HTTPException

from .database import (
    buscar_noticia_completa,
    buscar_resposta_cache,
    listar_noticias_por_data,
    salvar_resposta_no_cache,
)
from .gemini import gerar_explicacao_simples, gerar_info_complementar_gemini
from .utils import gerar_cartao_virtual


app = FastAPI()


@app.get("/noticias-por-data/{data}")
def endpoint_listar_noticias_por_data(data: str):
    return listar_noticias_por_data(data)


@app.post("/gerar-cartao/{id}")
def endpoint_gerar_cartao(id: int):
    noticia = buscar_noticia_completa(id)
    if not noticia:
        raise HTTPException(status_code=404, detail="Notícia não encontrada.")

    explicacao = buscar_resposta_cache(noticia["noticia"])
    if not explicacao:
        try:
            explicacao = gerar_explicacao_simples(noticia["noticia"])
            salvar_resposta_no_cache(noticia["noticia"], explicacao, noticia["data"])
        except Exception:
            raise HTTPException(status_code=503, detail="Serviço de IA indisponível para explicação.")

    info_complementar = gerar_info_complementar_gemini(noticia["noticia"])
    caminho = gerar_cartao_virtual(noticia, explicacao, info_complementar)
    return {"caminho_cartao": caminho}


@app.get("/explicar/{id}")
def explicar_e_gerar_cartao(id: int):
    noticia = buscar_noticia_completa(id)
    if not noticia:
        raise HTTPException(status_code=404, detail="Notícia não encontrada.")

    explicacao = buscar_resposta_cache(noticia["noticia"])
    if not explicacao:
        try:
            explicacao = gerar_explicacao_simples(noticia["noticia"])
            salvar_resposta_no_cache(noticia["noticia"], explicacao, noticia["data"])
        except Exception:
            raise HTTPException(status_code=503, detail="Serviço de IA indisponível para explicação.")

    info_complementar = gerar_info_complementar_gemini(noticia["noticia"])
    caminho_cartao = gerar_cartao_virtual(noticia, explicacao, info_complementar)

    return {
        "status": "sucesso",
        "id_noticia": noticia["id"],
        "noticia_original": noticia["noticia"],
        "explicacao_inteligente": explicacao,
        "ramo_atividade": info_complementar["ramo_atividade"],
        "impacto_pequenos_negocios": info_complementar["impacto_pequenos_negocios"],
        "caminho_cartao_virtual": caminho_cartao if caminho_cartao else "Erro na geração da imagem.",
    }

