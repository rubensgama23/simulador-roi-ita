
import streamlit as st

st.set_page_config(page_title="Simulador ROI - ITA Frotas", layout="wide")

# Estilo CSS reforçado
st.markdown("""
<style>
html, body, [class*="css"] {
    background-color: #000000 !important;
    color: white !important;
    font-family: 'Arial', sans-serif !important;
}
.css-1d391kg, .css-1v0mbdj {
    background-color: #000000 !important;
}
h1, h2, h3, h4, h5, h6, p, label {
    color: white !important;
}
.stSlider > div[data-baseweb="slider"] > div {
    background: #FFD700 !important;
}
.stSlider > div[data-baseweb="slider"] span {
    background-color: #FFD700 !important;
}
div.stButton > button {
    background-color: #FFD700 !important;
    color: black !important;
    border: none;
}
div.stButton > button:hover {
    background-color: #e6c200 !important;
}
</style>
""", unsafe_allow_html=True)

st.image("logo_ita.png", width=160)
st.markdown('<h1>Simulador de ROI - Frota Corporativa</h1>', unsafe_allow_html=True)
st.markdown('<p style="color: #ccc;">Versão institucional • Desenvolvido para ITA Frotas</p>', unsafe_allow_html=True)
st.markdown("---")

def calcular_roi(valor_fipe, desconto, receita_mensal, juros_mensal, prazo, desvalorizacao, tributos, custo_op, custo_adm, custo_buro, qtd):
    valor_compra = valor_fipe * (1 - desconto)
    total_aquisicao = valor_compra * qtd
    mensal_op = custo_op * valor_compra
    mensal_adm = custo_adm * valor_compra
    total_buro = custo_buro * valor_compra
    mensal_buro = total_buro / prazo
    custo_total_mensal = (mensal_op + mensal_adm + mensal_buro) * qtd
    desval_total = desvalorizacao * (prazo / 12)
    valor_residual = valor_fipe * (1 - desval_total) * qtd
    parcela_mensal = total_aquisicao * (
        juros_mensal * (1 + juros_mensal)**prazo
    ) / ((1 + juros_mensal)**prazo - 1)
    total_pago = parcela_mensal * prazo
    receita_total = receita_mensal * qtd * prazo
    receita_gerada = receita_total + valor_residual
    lucro_bruto = receita_gerada - total_pago
    lucro_antes_ir = lucro_bruto - (custo_total_mensal * prazo)
    lucro_liquido = lucro_antes_ir * (1 - tributos)
    roi = lucro_liquido / total_aquisicao
    return round(lucro_liquido, 2), round(roi * 100, 2)

# Inputs
st.sidebar.header("Parâmetros")
valor_fipe = st.sidebar.number_input("Valor FIPE (R$)", value=120000)
desconto = st.sidebar.slider("Desconto na compra (%)", 0.0, 50.0, 16.7) / 100
prazo = st.sidebar.selectbox("Prazo (meses)", [12, 24, 31, 36])
desvalorizacao = st.sidebar.slider("Desvalorização anual (%)", 0.0, 30.0, 10.0) / 100
juros = st.sidebar.slider("Juros mensal (%)", 0.0, 5.0, 1.2) / 100
tributos = st.sidebar.slider("Carga tributária (%)", 0.0, 50.0, 34.0) / 100
qtd = st.sidebar.number_input("Qtd. de veículos", value=10)

st.markdown("### Premissas de custo (% sobre valor do veículo)")
custo_op = st.slider("Custos operacionais mensais", 0.0, 5.0, 1.0) / 100
custo_adm = st.slider("Despesas administrativas mensais", 0.0, 5.0, 0.55) / 100
custo_buro = st.slider("Custos burocráticos totais", 0.0, 10.0, 5.0) / 100

receita = st.number_input("Receita mensal por veículo (R$)", value=3000)

if st.button("Calcular ROI"):
    lucro, roi = calcular_roi(valor_fipe, desconto, receita, juros, prazo, desvalorizacao, tributos,
                              custo_op, custo_adm, custo_buro, qtd)
    st.markdown(
        f'<div style="border: 2px solid #FFD700; padding: 20px; border-radius: 10px; margin-top: 20px;">'
        f"<h4 style='color:#FFD700;'>Resultado</h4><b>Lucro líquido:</b> R$ {lucro:,.2f}<br><b>ROI líquido:</b> {roi:.2f}%</div>",
        unsafe_allow_html=True
    )
