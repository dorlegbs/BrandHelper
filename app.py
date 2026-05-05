import streamlit as st
from datetime import datetime, timedelta
from monitor import verificar_crise

# =============================
# CONFIGURAÇÃO DA PÁGINA
# =============================
st.set_page_config(
    page_title="Brand Watch 🚨",
    page_icon="🚨",
    layout="centered"
)

# =============================
# ESTILO (DEIXA BONITO)
# =============================
st.markdown("""
<style>
.big-title {
    font-size: 40px;
    font-weight: bold;
    color: #ff4b4b;
}
.card {
    padding: 20px;
    border-radius: 12px;
    background-color: #f5f5f5;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# =============================
# HEADER
# =============================
st.markdown('<p class="big-title">🚨 Brand Watch Dashboard</p>', unsafe_allow_html=True)
st.caption("Monitoramento inteligente de crises de marca em tempo real")

st.markdown("---")

# =============================
# INPUTS
# =============================
marca = st.text_input("🏷️ Marca", value="Nike")

col1, col2 = st.columns(2)

with col1:
    d1 = st.number_input("📅 Dia 1 (dias atrás)", 0, 30, 1)

with col2:
    d2 = st.number_input("📅 Dia 2 (dias atrás)", 0, 30, 2)

limite = st.slider("🚨 Limite de alerta (%)", 1, 100, 20)

st.markdown("---")

# =============================
# BOTÃO
# =============================
if st.button("🔍 Analisar agora"):

    if d1 == d2:
        st.error("Escolha dois dias diferentes!")
    else:
        with st.spinner("Analisando dados..."):
            variacao = verificar_crise(marca, limite, d1, d2)

        # Datas
        data_1 = (datetime.now() - timedelta(days=d1)).strftime("%d/%m/%Y")
        data_2 = (datetime.now() - timedelta(days=d2)).strftime("%d/%m/%Y")

        st.markdown("## 📊 Resultado")

        # Cards
        st.markdown(f"""
        <div class="card">
        <b>Marca:</b> {marca} <br>
        <b>Comparação:</b> {data_1} vs {data_2} <br>
        <b>Variação:</b> {variacao:+.1f}%
        </div>
        """, unsafe_allow_html=True)

        # Status
        if variacao >= limite:
            st.error(f"🚨 ALERTA DE CRISE! Pico de {variacao:+.1f}%")
        else:
            st.success(f"✅ Situação normal ({variacao:+.1f}%)")

st.markdown("---")

# =============================
# RODAPÉ
# =============================
st.caption("Desenvolvido com Streamlit | Monitoramento automatizado de mídia")
