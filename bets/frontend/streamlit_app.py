
import streamlit as st
import pandas as pd
import numpy as np
import requests

API_BASE = st.secrets.get("API_BASE", "http://127.0.0.1:8000")

st.set_page_config(page_title="Probabilidade de Perda — Projeto Completo", page_icon="🎰", layout="wide")
st.sidebar.title("Menu")
page = st.sidebar.radio("Navegação", ["Previsão (principal)", "Coleta & Métricas", "Histórico", "ML Avançado"], index=0)

GAMES = {
    "Fortune Tiger (caça-níqueis)": {"rtp": 0.9681, "k": 2500.0},
    "Slots genéricos (96%)": {"rtp": 0.96, "k": 2000.0},
    "Crash (exemplo)": {"rtp": 0.97, "k": 100.0},
    "Roleta (ilustrativo 97,3%)": {"rtp": 0.973, "k": 36.0},
}

def simulate_multimodal(spins, stake, rtp, k_max, sims, vol="alta"):
    rng = np.random.default_rng(42)
    mult = np.array([0.0,0.5,1.0,2.0,5.0,10.0,50.0,100.0,float(k_max)], dtype=float)
    if vol == "baixa":
        probs = np.array([0.62,0.12,0.12,0.10,0.035,0.01,0.004,0.0009,1e-5])
    elif vol == "média":
        probs = np.array([0.72,0.08,0.08,0.07,0.03,0.01,0.004,0.0009,1e-5])
    else:
        probs = np.array([0.82,0.06,0.05,0.04,0.02,0.01,0.004,0.00099,1e-5])
    probs = probs / probs.sum()
    exp_mult = float((probs*mult).sum())
    scale = rtp/exp_mult if exp_mult>0 else 1.0
    eff_mult = mult*scale
    idx = rng.choice(len(eff_mult), size=(int(sims), int(spins)), p=probs)
    gains = eff_mult[idx]*stake
    retorno = gains.sum(axis=1)
    gasto = spins*stake
    lucro = retorno - gasto
    perda_prob = float((lucro<0).mean())
    perda_esp = float((1-rtp)*gasto)
    return perda_prob, perda_esp

def pagina_previsao():
    st.title("Probabilidade de perda — interação simples")
    ALERTA_URL = "https://www.infomoney.com.br/consumo/chance-de-levar-premio-maximo-no-tigrinho-e-maior-que-na-mega-sena-mostra-calculo/"
    st.warning("⚠️ A maioria termina no prejuízo. Leia mais: " + ALERTA_URL)

    with st.form("form"):
        c1,c2 = st.columns([2,1])
        with c1: game = st.selectbox("Jogo", list(GAMES.keys()))
        with c2: sugest = st.checkbox("Usar sugestão do jogo", True)

        a,b = st.columns(2)
        with a: stake = st.number_input("Valor por aposta (R$)", 0.1, 1000.0, 2.0, step=0.1)
        with b: spins = st.number_input("Giros na sessão", 1, 200000, 500, step=10)

        r1,r2,r3,r4 = st.columns(4)
        if sugest:
            st.session_state["rtp"] = float(GAMES[game]["rtp"])
            st.session_state["k"] = float(GAMES[game]["k"])
        with r1: rtp = st.number_input("RTP (0–1)", 0.0, 0.9999, st.session_state.get("rtp", 0.9681), 0.0001)
        with r2: kmax = st.number_input("Max win (k×)", 1.1, 50000.0, st.session_state.get("k", 2500.0), 1.0)
        with r3: vol = st.selectbox("Volatilidade", ["baixa","média","alta"], index=2)
        with r4: sims = st.number_input("Simulações (Monte Carlo)", 1000, 100000, 20000, step=1000)

        sess_mes = st.slider("Sessões por mês (opcional)", 1, 60, 4)
        ok = st.form_submit_button("Calcular probabilidade", use_container_width=True)

    if not ok: 
        st.info("Preencha e clique em **Calcular probabilidade**.")
        return

    try:
        train_info = requests.post(f"{API_BASE}/ml/train", timeout=60).json()
    except Exception as e:
        train_info = {"status":"erro", "detalhe": str(e)}

    perda_prob, perda_esp = simulate_multimodal(spins, stake, rtp, kmax, sims, vol)
    gasto = spins*stake
    perda_esp_mes = perda_esp * sess_mes

    cA,cB,cC = st.columns(3)
    with cA: st.metric("Gasto na sessão", f"R$ {gasto:,.2f}".replace(",", "X").replace(".", ",").replace("X","."))
    with cB: st.metric("Probabilidade de terminar no prejuízo", f"{perda_prob*100:.2f}%")
    with cC: st.metric("Perda esperada / sessão", f"R$ {perda_esp:,.2f}".replace(",", "X").replace(".", ",").replace("X","."))
    st.metric("Perda esperada / mês", f"R$ {perda_esp_mes:,.2f}".replace(",", "X").replace(".", ",").replace("X","."))

    # ALERTA solicitado
    st.warning("""
⚠️ **ALERTA BASEADO EM DADOS REAIS:**

• 204 denúncias no CRC sobre apostas \n
• R$ 147.408 em valores reclamados  \n
• Média de R$ 722 por pessoa prejudicada  \n

🎯 **NOSSA RECOMENDAÇÃO:**  
Considere alternativas de investimento com retorno mais previsível e seguro.
""")

    st.subheader("Pesquisa (anônima)")
    with st.form("survey"):
        col1,col2,col3 = st.columns(3)
        with col1: idade = st.number_input("Idade", 10, 100, 25)
        with col2: investido = st.number_input("Valor investido na sessão (R$)", 0.0, 1e7, float(gasto), 1.0, format="%.2f")
        with col3: final = st.number_input("Valor final após a sessão (R$)", 0.0, 1e7, max(0.0, float(gasto)-perda_esp), 1.0, format="%.2f")
        enviar = st.form_submit_button("Enviar resposta")
    if enviar:
        try:
            r = requests.post(f"{API_BASE}/api/survey/submit", json={
                "age": int(idade), "invested": float(investido), "final": float(final),
                "game": game, "rtp": float(rtp), "k": float(kmax), "spins": int(spins),
                "sessions_per_month": int(sess_mes)
            }, timeout=20)
            if r.ok: st.success("Obrigado! Resposta registrada.")
            else: st.error(r.text)
        except Exception as e:
            st.error(f"Falha ao enviar: {e}")

def pagina_coleta():
    st.title("Coleta & Métricas")
    a,b = st.columns([1,2])
    with a:
        if st.button("Executar coleta artificial agora", use_container_width=True):
            try:
                r = requests.post(f"{API_BASE}/ingest/run", timeout=30)
                st.success("Coleta OK"); st.json(r.json())
            except Exception as e:
                st.error(f"Falha: {e}")
    with b:
        try:
            resp = requests.get(f"{API_BASE}/metrics/latest", timeout=20)
            latest = resp.json()
            if isinstance(latest, dict):
                st.error(latest)
            else:
                st.subheader("Últimos indicadores")
                st.dataframe(pd.DataFrame(latest))
        except Exception as e:
            st.error(f"Falha ao buscar indicadores: {e}")

def pagina_hist():
    st.title("Histórico")
    src = st.selectbox("Fonte", ["spa","procon","cnc"])
    try:
        resp = requests.get(f"{API_BASE}/metrics/history/{src}", timeout=20)
        hist = resp.json()
        if isinstance(hist, dict):
            st.error(hist)
            return
        df = pd.DataFrame(hist)
        if df.empty:
            st.info("Sem histórico ainda. Clique em 'Executar coleta artificial agora' na aba anterior e volte aqui.")
        else:
            st.line_chart(df.pivot_table(index="t", columns="key", values="value", aggfunc="first"))
    except Exception as e:
        st.error(str(e))

def pagina_ml():
    st.title("ML Avançado — classificador de textos")
    txt = st.text_area("Cole um texto/notícia sobre apostas/cassinos:", height=140)
    c1,c2 = st.columns(2)
    with c1:
        if st.button("Treinar modelo de texto", use_container_width=True):
            try:
                st.json(requests.post(f"{API_BASE}/ml/train", timeout=60).json())
            except Exception as e:
                st.error(str(e))
    with c2:
        if st.button("Classificar texto", use_container_width=True):
            if not txt.strip():
                st.warning("Cole algum texto para classificar."); return
            try:
                r = requests.post(f"{API_BASE}/ml/predict", params={"text": txt}, timeout=30)
                st.json(r.json())
            except Exception as e:
                st.error(str(e))

if page == "Previsão (principal)":
    pagina_previsao()
elif page == "Coleta & Métricas":
    pagina_coleta()
elif page == "Histórico":
    pagina_hist()
else:
    pagina_ml()
