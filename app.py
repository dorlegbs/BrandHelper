import streamlit as st
from datetime import datetime, timedelta
from monitor import verificar_crise, buscar_mencoes_dia
import plotly.express as px
import pandas as pd
import random

# =============================
# CONFIG
# =============================
st.set_page_config(
    page_title="Brand Watch 🚨",
    page_icon="🚨",
    layout="wide"
)

# =============================
# SIDEBAR
# =============================
st.sidebar.title("⚙️ Configurações")

marcas_disponiveis = ["Nike", "Adidas", "Petrobras", "Apple", "Google"]

marca = st.sidebar.selectbox("🏷️ Marca", marcas_disponiveis)

dias = st.sidebar.slider("📅 Dias analisados", 2, 7, 3)

limite = st.sidebar.slider("🚨 Limite de alerta (%)", 1, 100, 20)

# =============================
# HEADER
# =============================
st.title("🚨 Brand Watch Dashboard")
st.markdown("Monitoramento inteligente de menções")

st.markdown("---")

# =============================
# COLETAR DADOS
# =============================
dados = []
datas = []

with st.spinner("Buscando dados..."):
    for i in range(dias):
        dia = datetime.now() - timedelta(days=i)
        label = dia.strftime("%d/%m")
        mencoes = buscar_mencoes_dia(marca, i)

        datas.append(label)
        dados.append(mencoes)

datas = datas[::-1]
dados = dados[::-1]

# =============================
# MÉTRICAS
# =============================
col1, col2, col3 = st.columns(3)

variacao = verificar_crise(marca, limite)

col1.metric("📊 Hoje", dados[-1])
col2.metric("📊 Ontem", dados[-2] if len(dados) > 1 else 0)
col3.metric("📈 Variação", f"{variacao:+.1f}%")

# =============================
# ALERTA
# =============================
if variacao >= limite:
    st.error(f"🚨 ALERTA: aumento de {variacao:+.1f}%")
else:
    st.success("✅ Situação normal")

st.markdown("---")

# =============================
# GRÁFICO (PLOTLY)
# =============================
st.subheader("📈 Evolução de menções")

fig = px.line(
    x=datas,
    y=dados,
    markers=True,
    title=f"Menções de {marca}"
)

st.plotly_chart(fig, use_container_width=True)

# =============================
# HEATMAP (REDES)
# =============================
st.subheader("🔥 Distribuição por redes")

redes = ["Twitter", "Instagram", "Facebook", "YouTube", "TikTok"]

# Simulação inteligente (proporcional ao volume real)
heat_data = []

for data, total in zip(datas, dados):
    distribuicao = [random.uniform(0.1, 1.0) for _ in redes]
    soma = sum(distribuicao)

    valores = [int((x/soma) * total) for x in distribuicao]

    for rede, valor in zip(redes, valores):
        heat_data.append({
            "Data": data,
            "Rede": rede,
            "Menções": valor
        })

df = pd.DataFrame(heat_data)

heatmap = px.density_heatmap(
    df,
    x="Data",
    y="Rede",
    z="Menções",
    color_continuous_scale="Reds"
)

st.plotly_chart(heatmap, use_container_width=True)

# =============================
# RODAPÉ
# =============================
st.markdown("---")
st.caption("Dashboard com análise visual de crise de marca")
