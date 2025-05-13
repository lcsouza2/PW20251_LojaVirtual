import uvicorn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from babel.numbers import format_currency

from repo.produto_repo import criar_tabela_produtos, obter_produto_por_id, obter_produtos_por_pagina
from repo.cliente_repo import criar_tabela_clientes, obter_cliente_por_id, obter_clientes_por_pagina

criar_tabela_produtos()
criar_tabela_clientes()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def format_currency_br(value, currency='BRL', locale='pt_BR'):
    return format_currency(value, currency, locale=locale)

templates.env.filters['format_currency_br'] = format_currency_br

@app.get("/")
def read_root(request: Request):
    produtos = obter_produtos_por_pagina(12, 0)
    response = templates.TemplateResponse("index.html", {"request": request, "produtos": produtos})
    return response

@app.get("/produtos/{id}")
def read_produto(request: Request, id: int):
    produto = obter_produto_por_id(id)
    response = templates.TemplateResponse("produto.html", {"request": request, "produto": produto})
    return response

@app.get("/clientes")
def read_clientes(request: Request):
    clientes = obter_clientes_por_pagina(12, 0)
    response = templates.TemplateResponse("clientes.html", {"request": request, "clientes": clientes})
    return response

if __name__ == "__main__":
    uvicorn.run(app=app, port=8000, reload=True)