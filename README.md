# Credenciais API

API em **FastAPI** que:
- Recebe uploads de arquivos `.txt`
- Processa linhas no formato `url:user:pass` (ou variações)
- Armazena no banco SQLite `credenciais.db`
- Oferece rota `/search?term=` para buscar credenciais por domínio

---

## 🚀 Rodando localmente

1. Clone este repositório
2. Crie e ative um virtualenv (opcional)
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
