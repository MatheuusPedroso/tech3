Video

https://youtu.be/xq1AB-Jzyqs

# 🎰 Probabilidade Bets  
**Fase 3 – Tech Challenge | Pós Tech - Machine Learning Engineering**

---

## 📘 Descrição do Projeto
O projeto **Probabilidade Bets** tem como objetivo conscientizar sobre os riscos financeiros em jogos de azar, utilizando **dados simulados e aprendizado de máquina** para estimar a **probabilidade de perda** de um jogador.  

A aplicação foi desenvolvida de forma completa, com **backend em FastAPI**, **frontend em Streamlit** e **modelo de Machine Learning em produção**, atendendo a todos os critérios técnicos e funcionais exigidos no desafio.

O sistema permite:
- Simular apostas e calcular o risco de prejuízo;
- Coletar dados e armazenar métricas em um banco de dados real (SQLite);
- Treinar e executar um modelo de ML diretamente da aplicação;
- Exibir alertas baseados em dados reais e promover conscientização financeira.

---

## 🧠 Tecnologias Utilizadas

### 🔹 Backend
- **Python 3.12**
- **FastAPI**
- **Uvicorn**
- **SQLite**
- **SQLAlchemy**
- **Scikit-learn**
- **Pandas / NumPy**

### 🔹 Frontend
- **Streamlit**
- **Requests**
- **Pandas**

---

## ⚙️ Estrutura do Projeto

```
probabilidade-bets/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── models/
│   │   └── routes/
│   │       ├── ingest.py
│   │       ├── metrics.py
│   │       ├── ml.py
│   │       └── survey.py
│   ├── db/
│   │   └── data.db
│   └── requirements.txt
│
├── frontend/
│   ├── streamlit_app.py
│   └── requirements.txt
│
└── README.md
```

---

## 🚀 Execução do Projeto

### 1️⃣ Iniciar o backend
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Acesse: **http://127.0.0.1:8000**  
Documentação: **http://127.0.0.1:8000/docs**

### 2️⃣ Iniciar o frontend
```bash
cd frontend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Interface disponível em: **http://localhost:8501**

---

## 🧩 Funcionalidades Implementadas

| Módulo | Descrição |
|--------|------------|
| **/ingest/run** | Simula a coleta de dados de denúncias (SPA, Procon e CNC) |
| **/metrics/latest** | Exibe os dados mais recentes coletados |
| **/metrics/history/{source}** | Histórico de métricas por fonte |
| **/api/survey/submit** | Registra respostas anônimas (idade, valor investido e resultado final) |
| **/ml/train** | Treina o modelo de Machine Learning |
| **/ml/predict** | Realiza previsões de risco com base em texto |
| **/frontend** | Interface para interação e visualização dos resultados |

---

## 🧠 Modelo de Machine Learning
O modelo utiliza:
- **TF-IDF Vectorizer** → representação numérica do texto  
- **Logistic Regression** → classificação binária  
  - `risco/perda` → comportamento financeiro de risco  
  - `neutro` → conteúdo não relacionado a apostas  

Modelo salvo em: `app/models/text_model.pkl`.

---

## 🎨 Interface do Usuário
A aplicação web contém quatro seções:

1. **Previsão (principal)** — simulação de apostas e cálculo de risco  
2. **Coleta & Métricas** — coleta e exibição de dados artificiais  
3. **Histórico** — gráficos de métricas coletadas  
4. **ML Avançado** — treinamento e classificação de textos

---

## 🗃️ Armazenamento de Dados
Banco: **SQLite** (`db/data.db`)  
Tabelas:
- `survey` — dados enviados pelos usuários  
- `metrics` — coletas simuladas

---

## 🧩 Arquitetura de Solução

```
[Usuário] ⇄ [Frontend Streamlit]
       ⇅
[API FastAPI] ⇄ [Banco SQLite] ⇄ [Modelo de ML (Scikit-learn)]
```

---


---

## 🧾 Observações Finais
- Projeto desenvolvido por **Matheus da Silva Pedroso (RM: 360903)**  
- Tema: *Análise de probabilidade de perda em jogos de aposta com foco educativo*  
- Aplicação 100% funcional e reproduzível  
- Código revisado com auxílio de IA apenas para padronização e clareza

---

## 📚 Licença
Uso acadêmico e educativo, sem fins comerciais.
