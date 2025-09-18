# -*- coding: utf-8 -*-
import streamlit as st
import numpy as np
import datetime
import io
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm

# ==============================
# CONFIGURAÇÃO DA PÁGINA
# ==============================
st.set_page_config(page_title="Simulador Recria a Pasto", layout="wide")
st.markdown("<h1 style='text-align: center;'> 🐂 Análise Econômica da Recria a Pasto </h1>", unsafe_allow_html=True)
st.markdown("---")

# ==============================
# ENTRADAS
# ==============================
st.sidebar.header("Parâmetros de Entrada")

peso_inicial = st.sidebar.number_input("Peso inicial (kg)", value=190.0, min_value=0.0, step=1.0, format="%.2f")
preco_compra_pyg = st.sidebar.number_input("Preço compra (₲/kg PV)", value=17800.0, min_value=0.0, step=100.0, format="%.2f")
cambio = st.sidebar.number_input("Câmbio (₲/US$)", value=7820.0, min_value=0.0, step=10.0, format="%.2f")

dias = st.sidebar.number_input("Período (dias em pastejo)", value=280, min_value=1, step=1)
gmd = st.sidebar.number_input("Ganho médio diário (kg/dia)", value=0.80, min_value=0.0, step=0.01, format="%.2f")

custo_aluguel = st.sidebar.number_input("Custo aluguel (US$/mês)", value=5.40, min_value=0.0, step=0.1, format="%.2f")
custo_nutricional = st.sidebar.number_input("Custo nutrição (US$/mês)", value=4.0, min_value=0.0, step=0.1, format="%.2f")
custo_operacional = st.sidebar.number_input("Custo operações (US$/mês)", value=3.44, min_value=0.0, step=0.1, format="%.2f")

juros_anual = st.sidebar.number_input("Juros anual (%)", value=8.5, min_value=0.0, step=0.1, format="%.2f") / 100
preco_venda_kg = st.sidebar.number_input("Preço venda (US$/kg PV)", value=2.40, min_value=0.0, step=0.01, format="%.2f")

# ==============================
# CÁLCULOS
# ==============================
valor_compra_usd = (peso_inicial * preco_compra_pyg) / cambio
preco_compra_usd_kg = preco_compra_pyg / cambio

peso_final = peso_inicial + gmd * dias
gpv = peso_final - peso_inicial

meses = dias / 30
custo_mensal = custo_aluguel + custo_nutricional + custo_operacional
custo_total_periodo = custo_mensal * meses
custo_total = valor_compra_usd + custo_total_periodo

receita = peso_final * preco_venda_kg
juros_valor = valor_compra_usd * juros_anual * (dias / 365)

lucro = receita - custo_total - juros_valor
margem_periodo = (lucro / receita * 100) if receita > 0 else 0
margem_mensal = margem_periodo / meses if meses > 0 else 0
roi = (lucro / valor_compra_usd * 100) if valor_compra_usd > 0 else 0
roi_mensal = roi / meses if meses > 0 else 0
roi_custo = (lucro / custo_total * 100) if custo_total > 0 else 0
roi_custo_mensal = roi_custo / meses if meses > 0 else 0

# Datas
data_inicial = datetime.date.today()
data_final = data_inicial + datetime.timedelta(days=int(dias))

# ==============================
# QUADRO DE COMPRA
# ==============================
st.subheader("📋 Parâmetros de Compra")
st.write(f"💱 Câmbio: **₲ {cambio:,.0f}/US$**")
st.write(f"🐄 Preço bezerro: **₲ {preco_compra_pyg:,.0f}/kg PV**")
st.write(f"💵 Preço bezerro: **${preco_compra_usd_kg:.2f}/kg PV**")

st.markdown("---")

# ==============================
# SAÍDAS EM 3 COLUNAS
# ==============================
col1, col2, col3 = st.columns([1.2,1.2,1.2])

with col1:
    st.subheader("⚖️ Indicadores Zootécnicos")
    st.write(f"📆 Data inicial: **{data_inicial.strftime('%d/%m/%Y')}**")
    st.write(f"📆 Data final: **{data_final.strftime('%d/%m/%Y')}**")
    st.write(f"📆 Dias em pastejo: **{dias}**")
    st.write(f"🐄 Peso inicial: **{peso_inicial:.2f} kg**")
    st.write(f"⚖️ Peso final: **{peso_final:.2f} kg**")
    st.write(f"➕ GPV: **{gpv:.2f} kg**")
    st.write(f"📈 GMD: **{gmd:.2f} kg/dia**")

with col2:
    st.subheader("💰 Custos Detalhados")
    st.write(f"🐂 Custo do animal: **${valor_compra_usd:,.2f}**")
    st.write(f"🌱 Custo aluguel/mês: **${custo_aluguel:.2f}**")
    st.write(f"🥣 Custo nutrição/mês: **${custo_nutricional:.2f}**")
    st.write(f"👨‍🌾 Custo operações/mês: **${custo_operacional:.2f}**")
    st.write(f"🗓️ Custo total período: **${custo_total_periodo:,.2f}**")
    st.markdown(f"🔴 <span style='color:red'>**Custo total: ${custo_total:,.2f}**</span>", unsafe_allow_html=True)
    st.write(f"🏦 Juros sobre compra do animal: **${juros_valor:.2f}**")

with col3:
    st.subheader("📊 Resultado Econômico")
    st.write(f"💵 Receita de venda: **${receita:,.2f}**")
    st.markdown(f"🟢 <span style='color:green'>**Lucro líquido: ${lucro:,.2f}**</span>", unsafe_allow_html=True)
    st.write(f"📈 Margem de lucro: **{margem_periodo:.2f}%**")
    st.write(f"📆 Margem mensal: **{margem_mensal:.2f}%**")
    st.write(f"📊 Retorno sobre investimento: **{roi:.2f}%**")
    st.write(f"📆 ROI mensal: **{roi_mensal:.2f}%/mês**")
    st.write(f"📊 Retorno sobre custo total: **{roi_custo:.2f}%**")
    st.write(f"📆 ROI mensal sobre custo total: **{roi_custo_mensal:.2f}%/mês**")

# ==============================
# PDF EXPORT (SEM GRÁFICO, MELHORADO)
# ==============================
def gerar_pdf():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="TituloSecao", fontSize=12, textColor=colors.HexColor("#003366"), spaceBefore=8, spaceAfter=8))
    elementos = []

    elementos.append(Paragraph("Relatório de Viabilidade Econômica – Recria a Pasto", styles["Heading1"]))

    # Quadro compra
    elementos.append(Paragraph("Parâmetros de Compra", styles["TituloSecao"]))
    tabela_compra = Table([
        ["Câmbio (G/US$)", f"{cambio:,.0f}"],
        ["Preço bezerro (G/kg PV)", f"{preco_compra_pyg:,.0f}"],
        ["Preço bezerro (US$/kg PV)", f"{preco_compra_usd_kg:.2f}"],
    ], colWidths=[220,200])
    tabela_compra.setStyle(TableStyle([("GRID",(0,0),(-1,-1),0.5,colors.black)]))
    elementos.append(tabela_compra)
    elementos.append(Spacer(1,12))

    # Indicadores
    elementos.append(Paragraph("Indicadores Zootécnicos", styles["TituloSecao"]))
    tabela_ind = Table([
        ["Data inicial", data_inicial.strftime('%d/%m/%Y')],
        ["Data final", data_final.strftime('%d/%m/%Y')],
        ["Dias em pastejo", f"{dias}"],
        ["Peso inicial (kg)", f"{peso_inicial:.2f}"],
        ["Peso final (kg)", f"{peso_final:.2f}"],
        ["GPV (kg)", f"{gpv:.2f}"],
        ["GMD (kg/dia)", f"{gmd:.2f}"],
    ], colWidths=[220,200])
    tabela_ind.setStyle(TableStyle([("GRID",(0,0),(-1,-1),0.5,colors.black)]))
    elementos.append(tabela_ind)
    elementos.append(Spacer(1,12))

    # Custos
    elementos.append(Paragraph("Custos Detalhados", styles["TituloSecao"]))
    tabela_custos = Table([
        ["Custo do animal (US$)", f"{valor_compra_usd:,.2f}"],
        ["Custo aluguel/mês (US$)", f"{custo_aluguel:.2f}"],
        ["Custo nutrição/mês (US$)", f"{custo_nutricional:.2f}"],
        ["Custo operações/mês (US$)", f"{custo_operacional:.2f}"],
        ["Custo total período (US$)", f"{custo_total_periodo:,.2f}"],
        ["Custo total (US$)", f"{custo_total:,.2f}"],
        ["Juros sobre compra do animal (US$)", f"{juros_valor:.2f}"],
    ], colWidths=[220,200])
    tabela_custos.setStyle(TableStyle([("GRID",(0,0),(-1,-1),0.5,colors.black)]))
    elementos.append(tabela_custos)
    elementos.append(Spacer(1,12))

    # Resultado
    elementos.append(Paragraph("Resultado Econômico", styles["TituloSecao"]))
    tabela_res = Table([
        ["Receita (US$)", f"{receita:,.2f}"],
        ["Lucro líquido (US$)", f"{lucro:,.2f}"],
        ["Margem período (%)", f"{margem_periodo:.2f}%"],
        ["Margem mensal (%)", f"{margem_mensal:.2f}%"],
        ["ROI (%)", f"{roi:.2f}%"],
        ["ROI mensal (%)", f"{roi_mensal:.2f}%"],
        ["ROI sobre custo total (%)", f"{roi_custo:.2f}%"],
        ["ROI mensal sobre custo total (%)", f"{roi_custo_mensal:.2f}%"],
    ], colWidths=[220,200])
    tabela_res.setStyle(TableStyle([("GRID",(0,0),(-1,-1),0.5,colors.black)]))
    elementos.append(tabela_res)

    doc.build(elementos)
    buffer.seek(0)
    return buffer

st.markdown("---")
if st.button("📥 Exportar Relatório PDF"):
    pdf_final = gerar_pdf()
    st.download_button("⬇️ Baixar PDF", data=pdf_final, file_name="recria_pasto.pdf", mime="application/pdf")
st.markdown("---")
st.subheader("📈 Análise de Sensibilidade Interativa")

col_a, col_b, col_c = st.columns(3)

with col_a:
    preco_compra_pyg_sens = st.slider(
        "Preço compra (₲/kg PV)", 
        min_value=int(preco_compra_pyg*0.8), 
        max_value=int(preco_compra_pyg*1.2), 
        value=int(preco_compra_pyg), 
        step=100
    )

with col_b:
    preco_venda_sens = st.slider(
        "Preço venda (US$/kg PV)", 
        min_value=float(preco_venda_kg*0.8), 
        max_value=float(preco_venda_kg*1.2), 
        value=float(preco_venda_kg), 
        step=0.05
    )

with col_c:
    gmd_sens = st.slider(
        "GMD (kg/dia)", 
        min_value=float(gmd*0.7), 
        max_value=float(gmd*1.3), 
        value=float(gmd), 
        step=0.05
    )

# Recalcular cenário
valor_compra_usd_sens = (peso_inicial * preco_compra_pyg_sens) / cambio
peso_final_sens = peso_inicial + gmd_sens * dias
gpv_sens = peso_final_sens - peso_inicial
receita_sens = peso_final_sens * preco_venda_sens
lucro_sens = receita_sens - (valor_compra_usd_sens + custo_total_periodo) - juros_valor

# Mostrar resultados do cenário
st.write("### 🔎 Resultado do Cenário")
st.write(f"🐂 Preço compra: ₲ {preco_compra_pyg_sens:,}  |  ${preco_compra_pyg_sens/cambio:.2f}/kg PV")
st.write(f"💵 Preço venda: ${preco_venda_sens:.2f}/kg PV")
st.write(f"📈 GMD: {gmd_sens:.2f} kg/dia")
st.markdown(f"🟢 **Lucro líquido: ${lucro_sens:,.2f}**")

