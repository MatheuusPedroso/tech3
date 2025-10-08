# Tech Challenge — Bets Social (com ingestão, BD, ML e dashboard)

## Como este projeto cobre **todos os pontos** do desafio
1. **API que coleta e armazena** (tempo real/agendamento): `POST /ingest/run` faz scraping de links oficiais (Gov.br/SPA, Procon-SP, Agência Brasil/CNC) e salva em **SQLite**/**Postgres** via SQLAlchemy. Agendamento com **APScheduler** em `startup`.
2. **Modelo de ML treinado com *esta* base**: módulo **/ml** treina um classificador TF‑IDF + LogisticRegression usando o **texto** das próprias páginas coletadas (tabela `documents`) com rótulos heurísticos (`mercado`, `fiscalizacao`, `consumidor`). Endpoints: `POST /ml/train` e `POST /ml/predict`.
3. **Código + documentação**: estrutura organizada `backend/` `frontend/` `docs/` com README e `.env.example`. Suba para o **GitHub** e inclua o link na entrega.
4. **Storytelling em vídeo**: arquivo `docs/storytelling.md` traz roteiro (3–5 min) conectando problema, dados, pipeline, ML e demo.
5. **Modelo produtivo alimentando aplicação**: front **Streamlit** consome a API para acionar coleta, ver **métricas/histórico** e **treinar/prever** com o modelo de texto em tempo real.

> Requisito do enunciado: construir **API de coleta + BD/DW/Data Lake**, **um modelo de ML**, **código documentado no GitHub**, **storytelling em vídeo** e o **modelo em produção** numa aplicação simples ou dashboard. (vide PDF do desafio).

## Rodar (dev)
### Backend
```bash
cd backend
python -m venv .venv && . .venv/Scripts/Activate.ps1  # mac/linux: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

### Frontend
```bash
cd ../frontend
python -m venv .venv && . .venv/Scripts/Activate.ps1
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Notas
- As regex dos *extractors* são heurísticas e podem exigir ajuste se as páginas mudarem.
- Para Postgres, defina `DATABASE_URL=postgresql+psycopg://user:pass@host:5432/db`.
- O classificador é propositalmente leve para ser treinado **ao vivo** durante a apresentação.
