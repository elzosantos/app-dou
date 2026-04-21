from __future__ import annotations

from pathlib import Path

import imgkit

from .database import get_project_root


def get_cartoes_dir() -> Path:
    return get_project_root() / "cartoes"


def get_imgkit_config() -> imgkit.config:
    return imgkit.config(wkhtmltoimage="/usr/bin/wkhtmltoimage")


def gerar_cartao_virtual(noticia, explicacao: str, info_complementar: dict[str, str]) -> str | None:
    cartoes_dir = get_cartoes_dir()
    cartoes_dir.mkdir(parents=True, exist_ok=True)

    nome_arquivo = cartoes_dir / f"{noticia['id']}_{noticia['data']}.png"

    html_template = f"""
<!DOCTYPE html>
<html lang="pt-br">
<head>
  <meta charset="UTF-8">
  <style>
    body {{
      width: 600px;
      height: 800px;
      font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
      margin: 0;
      padding: 0;
      background-color: #f4f7f6;
    }}
    .card {{
      background-color: #ffffff;
      margin: 30px;
      padding: 40px;
      border-radius: 15px;
      box-shadow: 0 10px 25px rgba(0,0,0,0.1);
      border-left: 10px solid #0056ac;
    }}
    .header {{
      text-align: center;
      border-bottom: 2px solid #eee;
      padding-bottom: 20px;
      margin-bottom: 30px;
    }}
    .header h1 {{
      font-size: 28px;
      color: #333;
      margin: 0;
    }}
    .uf-tag {{
      background-color: #0056ac;
      color: white;
      padding: 5px 15px;
      border-radius: 20px;
      font-size: 14px;
      font-weight: bold;
      margin-top: 10px;
      display: inline-block;
    }}
    .section {{
      margin-bottom: 25px;
    }}
    .label {{
      font-weight: bold;
      color: #0056ac;
      text-transform: uppercase;
      font-size: 12px;
      letter-spacing: 1px;
      margin-bottom: 5px;
      display: block;
    }}
    .content {{
      font-size: 16px;
      color: #555;
      line-height: 1.6;
    }}
    .highlight {{
      background-color: #e6f0fa;
      padding: 15px;
      border-radius: 8px;
      border-right: 5px solid #0056ac;
    }}
    .footer {{
      text-align: center;
      font-size: 12px;
      color: #999;
      margin-top: 40px;
      border-top: 1px solid #eee;
      padding-top: 15px;
    }}
  </style>
</head>
<body>
  <div class="card">
    <div class="header">
      <h1>Infográfico da Notícia</h1>
      <div class="uf-tag">{noticia['UF']} | {noticia['data']}</div>
    </div>

    <div class="section">
      <span class="label">Título da Notícia</span>
      <div class="content">"{noticia['noticia']}"</div>
    </div>

    <div class="section highlight">
      <span class="label">Ramo de Atividade</span>
      <div class="content"><strong>{info_complementar['ramo_atividade']}</strong></div>
    </div>

    <div class="section highlight">
      <span class="label">Impacto nos Pequenos Negócios</span>
      <div class="content">{info_complementar['impacto_pequenos_negocios']}</div>
    </div>

    <div class="section">
      <span class="label">Explicação Simplificada (IA)</span>
      <div class="content">{explicacao[:300]}... (veja completa na API)</div>
    </div>

    <div class="footer">
      Gerado automaticamente pelo app-gemini | Protocolo: {noticia['id']}
    </div>
  </div>
</body>
</html>
""".strip()

    options = {
        "quiet": "",
        "enable-local-file-access": "",
        "format": "png",
        "encoding": "UTF-8",
    }

    try:
        imgkit.from_string(
            html_template,
            str(nome_arquivo),
            options=options,
            config=get_imgkit_config(),
        )
        # Para o Streamlit conseguir abrir, retornamos o path relativo à raiz do projeto
        return str(Path("cartoes") / nome_arquivo.name)
    except Exception:
        return None

