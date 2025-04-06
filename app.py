
import streamlit as st
import numpy as np

st.set_page_config(page_title="Simulador ROI - ITA Frotas", layout="centered")

st.markdown(
    """
    <style>
    .big-title {
        font-size: 28px;
        font-weight: 600;
        color: #111;
        padding-top: 10px;
        padding-bottom: 5px;
    }
    .subdued {
        font-size: 14px;
        color: #777;
    }
    .result-box {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 20px;
        background-color: #f9f9f9;
        margin-top: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.image("logo_ita.png", width=160)
st.markdown('<div class="big-title">Simulador de ROI - Frota Corporativa</div>', unsafe_allow_html=True)
st.markdown('<div class="subdued">Versão institucional • Desenvolvido para ITA Frotas</div>', unsafe_allow_html=True)
st.markdown("---")

def calcular_roi(valor_fipe, desconto_compra, receita_mensal, taxa_juros_mensal,
                 prazo_meses, desvalorizacao_anual, carga_tributaria,
                 perc_operacional, perc_administrativo, perc_burocratico,
                 quantidade_veiculos):

    valor_compra = valor_fipe * (1 - desconto_compra)
    valor_total_aquisicao = valor_compra * quantidade_veiculos

    custo_operacional_mensal = (perc_operacional * valor_compra)
    despesa_administrativa_mensal = (perc_administrativo * valor_compra)
    custo_burocratico_total = (perc_burocratico * valor_compra)
    custo_burocratico_mensal = custo_burocratico_total / prazo_meses
    custo_total_mensal = (custo_operacional_mensal + despesa_administrativa_mensal + custo_burocratico_mensal) * quantidade_veiculos

    desvalorizacao_total = desvalorizacao_anual * (prazo_meses / 12)
    valor_residual_unitario = valor_fipe * (1 - desvalorizacao_total)
    valor_residual_total = valor_residual_unitario * quantidade_veiculos

    parcela_mensal = valor_total_aquisicao * (
        taxa_juros_mensal * (1 + taxa_juros_mensal)**prazo_meses
    ) / ((1 + taxa_juros_mensal)**prazo_meses - 1)
    valor_total_pago = parcela_mensal * prazo_meses

    receita_total = receita_mensal * quantidade_veiculos * prazo_meses
    receita_total_gerada = receita_total + valor_residual_total

    lucro_bruto = receita_total_gerada - valor_total_pago
    lucro_antes_imposto = lucro_bruto - (custo_total_mensal * prazo_meses)
    lucro_liquido = lucro_antes_imposto * (1 - carga_tributaria)
    roi_liquido = lucro_liquido / valor_total_aquisicao

    return round(lucro_liquido, 2), round(roi_liquido * 100, 2)

def calcular_locacao_para_roi(valor_fipe, desconto_compra, taxa_juros_mensal,
                              prazo_meses, desvalorizacao_anual, carga_tributaria,
                              perc_operacional, perc_administrativo, perc_burocratico,
                              roi_alvo, quantidade_veiculos):

    def objetivo(receita):
        _, roi = calcular_roi(
            valor_fipe, desconto_compra, receita,
            taxa_juros_mensal, prazo_meses,
            desvalorizacao_anual, carga_tributaria,
            perc_operacional, perc_administrativo, perc_burocratico,
            quantidade_veiculos
        )
        return roi - roi_alvo

    min_val, max_val = 100.0, 10000.0
    for _ in range(100):
        mid = (min_val + max_val) / 2
        if objetivo(mid) > 0:
            max_val = mid
        else:
            min_val = mid
    return round(mid, 2)

modo = st.radio("Escolha o modo de cálculo:", ["Calcular ROI com valor da locação", "Calcular valor da locação para ROI desejado"])

col1, col2 = st.columns(2)
with col1:
    valor_fipe = st.number_input("Valor FIPE do veículo (R$)", value=120000)
    desconto_compra = st.slider("Desconto na compra (%)", 0.0, 50.0, 16.7) / 100
    prazo_meses = st.selectbox("Prazo do contrato (meses)", [12, 24, 31, 36])
    desvalorizacao_anual = st.slider("Desvalorização anual (%)", 0.0, 30.0, 10.0) / 100

with col2:
    taxa_juros_mensal = st.slider("Taxa de juros mensal (%)", 0.0, 5.0, 1.2) / 100
    carga_tributaria = st.slider("Carga tributária (%)", 0.0, 50.0, 34.0) / 100
    quantidade_veiculos = st.number_input("Quantidade de veículos", value=10, step=1)

st.markdown("### Premissas de custo (% sobre valor do veículo)")
perc_operacional = st.slider("Custos operacionais mensais", 0.0, 5.0, 1.0) / 100
perc_administrativo = st.slider("Despesas administrativas mensais", 0.0, 5.0, 0.55) / 100
perc_burocratico = st.slider("Custos burocráticos totais", 0.0, 10.0, 5.0) / 100

if modo == "Calcular ROI com valor da locação":
    receita_mensal = st.number_input("Receita mensal por veículo (R$)", value=3000)
    if st.button("Calcular ROI"):
        lucro_liquido, roi_liquido = calcular_roi(
            valor_fipe, desconto_compra, receita_mensal,
            taxa_juros_mensal, prazo_meses,
            desvalorizacao_anual, carga_tributaria,
            perc_operacional, perc_administrativo, perc_burocratico,
            quantidade_veiculos
        )
        st.markdown(
            f"<div class='result-box'><h4>Resultado da Simulação</h4><b>Lucro líquido:</b> R$ {lucro_liquido:,.2f}<br><b>ROI líquido:</b> {roi_liquido:.2f}%</div>",
            unsafe_allow_html=True)

else:
    roi_desejado = st.number_input("ROI líquido desejado (%)", value=15.0)
    if st.button("Calcular valor da locação"):
        valor_locacao = calcular_locacao_para_roi(
            valor_fipe, desconto_compra, taxa_juros_mensal, prazo_meses,
            desvalorizacao_anual, carga_tributaria,
            perc_operacional, perc_administrativo, perc_burocratico,
            roi_desejado, quantidade_veiculos
        )
        st.markdown(
            f"<div class='result-box'><h4>Resultado da Simulação</h4><b>Valor da locação mensal por veículo:</b> R$ {valor_locacao:,.2f}</div>",
            unsafe_allow_html=True)
