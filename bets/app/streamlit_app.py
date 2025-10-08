import streamlit as st
import pandas as pd
import numpy as np
import re, requests, math
from bs4 import BeautifulSoup

st.set_page_config(page_title="Perdas em Cassinos/Bets — Painel Social", page_icon="🎰", layout="wide")

st.title("Perdas em Cassinos/Bets — Painel Social (🇧🇷 dados com links oficiais)")
st.caption("Dados coletados **ao vivo** de fontes oficiais/noticiosas. O painel mostra *estimativas* e trechos das fontes com link. Objetivo educativo — **não é aconselhamento financeiro**.")

DEFAULT_SOURCES = {
    "spa_news": "https://www.gov.br/fazenda/pt-br/assuntos/noticias/2025/agosto/no-primeiro-semestre-17-7-milhoes-de-brasileiros-realizaram-apostas-de-quota-fixa-e-ultrapassou-se-o-total-de-15-mil-sites-ilegais-bloqueados",
    "agencia_gov": "https://agenciagov.ebc.com.br/noticias/202508/anatel-bloqueia-15-mil-sites-ilegais-de-apostas-no-primeiro-semestre",
    "procon_news": "https://www.procon.sp.gov.br/jogos-e-apostas-quase-metade-das-pessoas-que-afirmam-jogar-ja-comprometeram-parte-da-renda-incluindo-retiradas-de-aplicacoes-financeiras-e-emprestimo-para-poder-jogar-constata-consulta-do-procon-sp/",
    "procon_pdf": "https://www.procon.sp.gov.br/wp-content/uploads/2025/02/RELATPESQCOMPJOGOSEAPOSTAS2025.pdf",
    "cnc_news": "https://agenciabrasil.ebc.com.br/economia/noticia/2025-01/cnc-diz-que-bets-causaram-perdas-de-r-103-bilhoes-ao-varejo-em-2024",
    "law_14790": "https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2023/lei/l14790.htm",
    "rfb_irpf": "https://www.gov.br/receitafederal/pt-br/assuntos/noticias/2024/maio/receita-regulamenta-tributacao-de-apostas-de-quota-fixa",
    "rtp_ref": "https://tribuna.com/en/casino/blogs/fortune-tiger-indepth-look-at-the-pg-soft-slot-with-968-rtp/"
}

with st.sidebar:
    st.subheader("Fontes (editáveis)")
    sources = {}
    for key, url in DEFAULT_SOURCES.items():
        sources[key] = st.text_input(key, url)
    st.caption("Troque os links quando houver nova divulgação. O painel tentará extrair números/trechos automaticamente.")

def fetch_text(url):
    r = requests.get(url, timeout=30, headers={"User-Agent":"Mozilla/5.0"})
    r.raise_for_status()
    return r.text

def extract_indicators_spa(html):
    soup = BeautifulSoup(html, "lxml"); text = soup.get_text(" ", strip=True)
    m_bettors = re.search(r"(\d{1,2}[\.,]\d)\s*milh[õo]es", text, flags=re.I)
    m_block = re.search(r"(\d{1,2}[\.,]?\d*)\s*mil\s*site[s]?\s*ilegais\s*bloqueados", text, flags=re.I)
    m_ggr = re.search(r"GGR[^\d]*(R\$\s*[\d\.,]+\s*bilh[õo]es)", text, flags=re.I)
    out = {}
    if m_bettors: out["apostadores_semestre"] = m_bettors.group(1) + " milhões"
    if m_block: out["sites_ilegais_bloqueados"] = m_block.group(1) + " mil"
    if m_ggr: out["ggr_semestre"] = m_ggr.group(1)
    snippets = []
    for pat in [r"\b[Gg]ross\s+Gaming\s+Revenue\b.*?\.", r"\bapostas no primeiro semestre.*?\.", r"\bsite[s]? ilegais.*?\."]:
        mm = re.search(pat, text, flags=re.I)
        if mm: snippets.append(mm.group(0))
    return out, snippets[:3]

def extract_number_from_text(html, patterns):
    soup = BeautifulSoup(html, "lxml"); text = soup.get_text(" ", strip=True)
    for pat in patterns:
        m = re.search(pat, text, flags=re.I)
        if m: return m.group(1), m.group(0)
    return None, None

cols = st.columns(3)
with cols[0]:
    st.markdown("#### Ministério da Fazenda — SPA")
    try:
        h = fetch_text(sources["spa_news"])
        ind, snips = extract_indicators_spa(h)
        st.write(ind if ind else "—")
        for s in snips: st.caption(s[:300]+"...")
        st.link_button("Abrir notícia SPA", sources["spa_news"])
    except Exception as e:
        st.error(f"Falha SPA: {e}")
with cols[1]:
    st.markdown("#### Agência Gov/Anatel")
    try:
        h = fetch_text(sources["agencia_gov"])
        val, snip = extract_number_from_text(h, [r"GGR[^\d]*(R\$\s*[\d\.,]+\s*bilh[õo]es)"])
        if val: st.write({ "ggr_semestre": val })
        if snip: st.caption(snip[:300]+"...")
        st.link_button("Abrir Agência Gov", sources["agencia_gov"])
    except Exception as e:
        st.error(f"Falha AgênciaGov: {e}")
with cols[2]:
    st.markdown("#### CNC — Impacto no varejo (2024)")
    try:
        h = fetch_text(sources["cnc_news"])
        val, snip = extract_number_from_text(h, [r"([R\$\s]*103\s*bilh[õo]es)"])
        if val: st.write({ "impacto_varejo_2024": val })
        if snip: st.caption(snip[:300]+"...")
        st.link_button("Abrir matéria CNC", sources["cnc_news"])
    except Exception as e:
        st.error(f"Falha CNC: {e}")

st.markdown("---")
st.header("Indicadores do consumidor (Procon-SP)")
try:
    h = fetch_text(sources["procon_news"])
    soup = BeautifulSoup(h, "lxml"); text = soup.get_text(" ", strip=True)
    m_perde = re.search(r"(70[,\.]?\d?\d?)%.*perdas", text, flags=re.I) or re.search(r"71%.*perd", text, flags=re.I)
    m_comp = re.search(r"(48%)", text, flags=re.I)
    m_div = re.search(r"(39%)", text, flags=re.I)
    bullets = []
    if m_perde: bullets.append(f"{m_perde.group(1)} dos apostadores relatam **perder mais do que ganhar** (consulta Procon-SP).")
    if m_comp: bullets.append(f"{m_comp.group(1)} comprometeram renda/aplicações/empréstimos para jogar.")
    if m_div: bullets.append(f"{m_div.group(1)} estão endividados por jogar/apostar.")
    st.write("\n".join([f"- {b}" for b in bullets]) if bullets else "—")
    st.link_button("Abrir notícia Procon-SP", sources["procon_news"])
    st.link_button("PDF da pesquisa", sources["procon_pdf"])
except Exception as e:
    st.error(f"Falha Procon: {e}")

st.markdown("---")
st.header("Simulador de perda esperada (RTP)")
c1,c2,c3 = st.columns(3)
with c1:
    aposta_mes = st.number_input("Aposta por mês (R$)", min_value=0.0, max_value=100000.0, value=200.0, step=10.0)
with c2:
    meses = st.number_input("Meses", min_value=1, max_value=60, value=12, step=1)
with c3:
    rtp = st.number_input("RTP (0–1) — ex.: Fortune Tiger ≈ 0,9681", min_value=0.0, max_value=0.9999, value=0.9681, step=0.0001)
gasto_total = aposta_mes * meses
house_edge = 1 - rtp
perda_esp = gasto_total * house_edge
st.metric("Perda esperada (longo prazo)", f"R$ {perda_esp:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), help="(1 - RTP) × aposta mensal × meses")
st.caption("Fonte do RTP: fabricantes/sites de jogos e imprensa. Ajuste o RTP conforme o jogo.")

st.markdown("##### Probabilidade de 'jackpot' (ilustrativa)")
colA, colB = st.columns(2)
with colA:
    odds = st.number_input("Odds do prêmio máximo (ex.: 1 em 40.000.000)", min_value=1.0, max_value=1e9, value=40000000.0, step=1000.0)
with colB:
    apostas = st.number_input("Número de apostas", min_value=0.0, max_value=1e8, value=1000.0, step=100.0)
prob_pelo_menos_um = 1 - (1 - 1/odds) ** apostas if odds>0 else 0.0
st.write(f"Chance de ao menos 1 prêmio máximo: **{prob_pelo_menos_um*100:.6f}%**")

st.markdown("---")
st.header("Tributação (links oficiais)")
st.write("• **Lei 14.790/2023** (15% sobre prêmios líquidos) — " + f"[link]({DEFAULT_SOURCES['law_14790']})")
st.write("• **IN RFB 2.191/2024** — " + f"[link]({DEFAULT_SOURCES['rfb_irpf']})")

st.info("O painel usa *links em tempo real*. Se algum link mudar, edite na barra lateral.")