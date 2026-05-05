import streamlit as st
from datetime import datetime, timedelta
from monitor import verificar_crise, buscar_mencoes_dia
import matplotlib.pyplot as plt

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

marca = st.sidebar.selectbox(
    "🏷️ Escolha uma marca",
    marcas_disponiveis
)

dias = st.sidebar.slider(
    "📅 Quantos dias analisar",
    2, 7, 3
)

limite = st.sidebar.slider(
    "🚨 Limite de alerta (%)",
    1, 100, 20
)

st.sidebar.markdown("---")
st.sidebar.caption("Selecione os parâmetros e visualize os dados")

# =============================
# HEADER
# =============================
st.title("🚨 Brand Watch Dashboard")
st.markdown("Monitoramento de menções e detecção de picos")

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

# inverter ordem (mais antigo → mais recente)
datas = datas[::-1]
dados = dados[::-1]

# =============================
# MÉTRICAS
# =============================
col1, col2, col3 = st.columns(3)

variacao = verificar_crise(marca, limite)

col1.metric("📊 Menções hoje", dados[-1])
col2.metric("📊 Menções ontem", dados[-2] if len(dados) > 1 else 0)
col3.metric("📈 Variação", f"{variacao:+.1f}%")

# =============================
# ALERTA
# =============================
if variacao >= limite:
    st.error(f"🚨 ALERTA DE CRISE: aumento de {variacao:+.1f}%")
else:
    st.success("✅ Situação normal")

st.markdown("---")

# =============================
# GRÁFICO
# =============================
st.subheader("📈 Evolução de menções")

fig, ax = plt.subplots()
ax.plot(datas, dados, marker='o')
ax.set_xlabel("Data")
ax.set_ylabel("Menções")
ax.set_title(f"Menções de {marca}")

st.pyplot(fig)

# =============================
# TABELA
# =============================
st.subheader("📋 Dados detalhados")

for d, m in zip(datas, dados):
    st.write(f"{d} → {m} menções")

# =============================
# RODAPÉ
# =============================
st.markdown("---")
st.caption("Dashboard interativo | Monitoramento de mídia em tempo real")
