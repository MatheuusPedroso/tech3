
# Probabilidade Bets — Projeto completo

## Como rodar

### Backend (API)
```bash
cd backend
python -m venv .venv
# Windows
.\.venv\Scripts\Activate.ps1
# Linux/Mac
# source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload
```

API raiz: http://127.0.0.1:8000/  
Docs: http://127.0.0.1:8000/docs

### Frontend (Streamlit)
```bash
cd frontend
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## O que está incluso
- **Previsão (principal):** simulador multimodal realista, cálculo de probabilidade de perda e pesquisa anônima enviada para `/api/survey/submit`.
- **ML Avançado:** treinamento e predição de um classificador de textos (TF‑IDF + LogisticRegression).
- **Coleta & Métricas:** coleta artificial (`/ingest/run`) e exibição de métricas atuais e histórico (`/metrics/*`), persistência em SQLite (`backend/db/data.db`).
- **Survey:** estatísticas em `/api/survey/stats`.
