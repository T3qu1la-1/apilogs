from fastapi import FastAPI, UploadFile, File, Query
import sqlite3

app = FastAPI(title="Credenciais API", version="1.0")

DB_NAME = "data/credenciais.db"
conn = sqlite3.connect(DB_NAME, check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS credenciais (
        url TEXT,
        user TEXT,
        pass TEXT,
        UNIQUE(url, user, pass)
    )
""")
conn.commit()

def classificar_tokens(tokens):
    url, user, senha = None, None, None
    for t in tokens:
        if "http" in t or ".com" in t or ".net" in t or ".org" in t or ".gov" in t:
            url = t
        elif "@" in t or (len(t) < 30 and not url):
            user = t
        else:
            senha = t
    return url, user, senha

def processar_linha(linha):
    tokens = linha.strip().split(":")
    if len(tokens) < 2:
        return None
    return classificar_tokens(tokens)

def salvar_db(url, user, senha):
    cursor.execute(
        "INSERT OR IGNORE INTO credenciais (url, user, pass) VALUES (?, ?, ?)",
        (url, user, senha)
    )
    conn.commit()



@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    conteudo = (await file.read()).decode("utf-8", errors="ignore")
    linhas = conteudo.splitlines()
    added = 0

    for linha in linhas:
        dados = processar_linha(linha)
        if dados:
            salvar_db(*dados)
            added += 1

    return {"status": "ok", "msg": f"{added} linhas processadas do upload {file.filename}"}


@app.get("/search")
async def search(term: str = Query(..., description="Parte da URL/domínio a procurar")):
    cursor.execute("SELECT url, user, pass FROM credenciais WHERE url LIKE ?", (f"%{term}%",))
    resultados = cursor.fetchall()
    return {
        "busca": term,
        "total": len(resultados),
        "results": [
            {"url": url or "", "user": user or "", "pass": senha or ""}
            for url, user, senha in resultados
        ]
    }
