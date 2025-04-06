
import streamlit as st

import numpy as np

# Função de cálculo do ROI e lucro líquido
def calcular_roi(valor_fipe, desconto_compra, receita_mensal, taxa_juros_mensal,
                 prazo_meses, desvalorizacao_anual, carga_tributaria,
                 perc_operacional, perc_administrativo, perc_burocratico,
                 quantidade_veiculos):

    valor_compra = valor_fipe * (1 - desconto_compra)
    valor_total_aquisicao = valor_compra * quantidade_veiculos

    # Cálculo de custos mensais e totais
    custo_operacional_mensal = (perc_operacional * valor_compra)
    despesa_administrativa_mensal = (perc_administrativo * valor_compra)
    custo_burocratico_total = (perc_burocratico * valor_compra)
    custo_burocratico_mensal = custo_burocratico_total / prazo_meses

    custo_total_mensal = (custo_operacional_mensal + despesa_administrativa_mensal + custo_burocratico_mensal) * quantidade_veiculos

    # Valor residual após depreciação
    desvalorizacao_total = desvalorizacao_anual * (prazo_meses / 12)
    valor_residual_unitario = valor_fipe * (1 - desvalorizacao_total)
    valor_residual_total = valor_residual_unitario * quantidade_veiculos

    # Cálculo da parcela mensal do financiamento
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

# Função para buscar valor de locação necessário para atingir ROI alvo
def calcular_locacao_para_roi(valor_fipe, desconto_compra, taxa_juros_mensal,
                              prazo_meses, desvalorizacao_anual, carga_tributaria,
                              perc_operacional, perc_administrativo, perc_burocratico,
                              roi_alvo, quantidade_veiculos):

    def objetivo(receita):
        lucro, roi = calcular_roi(
            valor_fipe, desconto_compra, receita,
            taxa_juros_mensal, prazo_meses,
            desvalorizacao_anual, carga_tributaria,
            perc_operacional, perc_administrativo, perc_burocratico,
            quantidade_veiculos
        )
        return roi - roi_alvo

    # Busca binária simples para encontrar receita mensal
    min_val, max_val = 100.0, 10000.0
    for _ in range(100):
        mid = (min_val + max_val) / 2
        if objetivo(mid) > 0:
            max_val = mid
        else:
            min_val = mid
    return round(mid, 2)

# --- Interface Streamlit ---
st.title("Simulador de ROI - Locação de Frotas")

modo = st.radio("Modo de cálculo", ["Calcular ROI com locação conhecida", "Calcular valor da locação para ROI desejado"])

valor_fipe = st.number_input("Valor FIPE do veículo (R$)", value=120000)
desconto_compra = st.slider("Desconto na compra (%)", 0.0, 50.0, 16.7) / 100
taxa_juros_mensal = st.slider("Taxa de juros mensal (%)", 0.0, 5.0, 1.2) / 100
prazo_meses = st.selectbox("Prazo do contrato (meses)", [12, 24, 31, 36])
desvalorizacao_anual = st.slider("Desvalorização anual (%)", 0.0, 30.0, 10.0) / 100
carga_tributaria = st.slider("Carga tributária sobre lucro (%)", 0.0, 50.0, 34.0) / 100
quantidade_veiculos = st.number_input("Quantidade de veículos", value=10, step=1)

perc_operacional = st.slider("Custos operacionais mensais (% sobre valor do veículo)", 0.0, 5.0, 1.0) / 100
perc_administrativo = st.slider("Despesas administrativas mensais (% sobre valor do veículo)", 0.0, 5.0, 0.55) / 100
perc_burocratico = st.slider("Custos burocráticos totais (% sobre valor do veículo)", 0.0, 10.0, 5.0) / 100

if modo == "Calcular ROI com locação conhecida":
    receita_mensal = st.number_input("Receita mensal por veículo (R$)", value=3000)
    if st.button("Calcular ROI"):
        lucro_liquido, roi_liquido = calcular_roi(
            valor_fipe, desconto_compra, receita_mensal,
            taxa_juros_mensal, prazo_meses,
            desvalorizacao_anual, carga_tributaria,
            perc_operacional, perc_administrativo, perc_burocratico,
            quantidade_veiculos
        )
        st.success(f"Lucro líquido: R$ {lucro_liquido:,.2f}")
        st.info(f"ROI líquido: {roi_liquido:.2f}%")
else:
    roi_desejado = st.number_input("ROI líquido desejado (%)", value=15.0)
    if st.button("Calcular valor da locação mensal"):
        valor_locacao = calcular_locacao_para_roi(
            valor_fipe, desconto_compra,
            taxa_juros_mensal, prazo_meses,
            desvalorizacao_anual, carga_tributaria,
            perc_operacional, perc_administrativo, perc_burocratico,
            roi_desejado, quantidade_veiculos
        )
        st.success(f"Valor mensal necessário por veículo: R$ {valor_locacao:,.2f}")
