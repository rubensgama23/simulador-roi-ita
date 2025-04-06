
import streamlit as st

def calcular_roi_simulacao(
    valor_fipe: float,
    desconto_compra: float,
    receita_mensal: float,
    custo_operacional_mensal: float,
    taxa_juros_mensal: float,
    prazo_meses: int,
    desvalorizacao_anual: float,
    carga_tributaria: float,
    quantidade_veiculos: int = 10
):
    valor_compra = valor_fipe * (1 - desconto_compra)
    valor_total_aquisicao = valor_compra * quantidade_veiculos
    desvalorizacao_total = desvalorizacao_anual * (prazo_meses / 12)
    valor_residual_unitario = valor_fipe * (1 - desvalorizacao_total)
    valor_residual_total = valor_residual_unitario * quantidade_veiculos

    parcela_mensal = valor_total_aquisicao * (
        taxa_juros_mensal * (1 + taxa_juros_mensal)**prazo_meses
    ) / ((1 + taxa_juros_mensal)**prazo_meses - 1)
    valor_total_pago = parcela_mensal * prazo_meses

    receita_total = receita_mensal * quantidade_veiculos * prazo_meses
    custo_operacional_total = custo_operacional_mensal * quantidade_veiculos * prazo_meses
    receita_total_gerada = receita_total + valor_residual_total

    lucro_bruto = receita_total_gerada - valor_total_pago
    lucro_antes_imposto = lucro_bruto - custo_operacional_total
    lucro_liquido = lucro_antes_imposto * (1 - carga_tributaria)
    roi_liquido = lucro_liquido / valor_total_aquisicao

    return round(lucro_liquido, 2), round(roi_liquido * 100, 2)

st.title("Simulador de ROI - Locação de Frotas")

valor_fipe = st.number_input("Valor FIPE do veículo (R$)", value=120000)
desconto_compra = st.slider("Desconto na compra (%)", 0.0, 50.0, 16.7) / 100
receita_mensal = st.number_input("Receita mensal por veículo (R$)", value=3000)
custo_operacional_mensal = st.number_input("Custo operacional mensal por veículo (R$)", value=1246.0)
taxa_juros_mensal = st.slider("Taxa de juros mensal (%)", 0.0, 5.0, 1.2) / 100
prazo_meses = st.selectbox("Prazo do contrato (meses)", [12, 24, 36])
desvalorizacao_anual = st.slider("Desvalorização anual (%)", 0.0, 30.0, 10.0) / 100
carga_tributaria = st.slider("Carga tributária sobre lucro (%)", 0.0, 50.0, 34.0) / 100
quantidade_veiculos = st.number_input("Quantidade de veículos", value=10, step=1)

if st.button("Calcular ROI"):
    lucro_liquido, roi_liquido = calcular_roi_simulacao(
        valor_fipe,
        desconto_compra,
        receita_mensal,
        custo_operacional_mensal,
        taxa_juros_mensal,
        prazo_meses,
        desvalorizacao_anual,
        carga_tributaria,
        quantidade_veiculos
    )

    st.success(f"Lucro líquido: R$ {lucro_liquido:,.2f}")
    st.info(f"ROI líquido: {roi_liquido:.2f}%")
