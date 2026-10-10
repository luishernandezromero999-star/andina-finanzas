"""
Dashboard Financiero Integral - Distribuciones Andina Comercial S.A.S.
Desarrollado con Streamlit, Plotly y Pandas para el análisis y visualización de indicadores financieros.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configuración de página
st.set_page_config(
    page_title="Andina Comercial S.A.S. | Dashboard Financiero",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo personalizado CSS moderno y ejecutivo
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #0f2b48 0%, #1a4a75 50%, #20639b 100%);
        padding: 24px 30px;
        border-radius: 12px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .main-header h1 {
        color: #ffffff;
        margin: 0;
        font-size: 28px;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    .main-header p {
        color: #d1e2f2;
        margin: 6px 0 0 0;
        font-size: 14px;
    }
    .metric-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 16px 20px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.03);
    }
    .badge-success {
        background-color: #d1fae5;
        color: #065f46;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 12px;
    }
    .badge-warning {
        background-color: #fef3c7;
        color: #92400e;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 12px;
    }
    .badge-danger {
        background-color: #fee2e2;
        color: #991b1b;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 12px;
    }
    .tab-subtitle {
        color: #475569;
        font-size: 15px;
        margin-bottom: 20px;
    }
    div[data-testid="stMetricValue"] {
        font-size: 24px;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# DATOS HISTÓRICOS Y MODELADOS (2021 - 2025)
# Basados en el modelo financiero del caso Distribuciones Andina y MicroDrive
# -------------------------------------------------------------
@st.cache_data
def load_financial_data():
    years = [2021, 2022, 2023, 2024, 2025]
    
    # Estado de Resultados (Cifras en Millones COP / USD)
    is_data = {
        "Ventas Netas": [2350.0, 2600.0, 2850.0, 3000.0, 3320.0],
        "Costo de Ventas y Op": [2068.0, 2280.0, 2497.0, 2616.2, 2855.2],
        "EBITDA": [282.0, 320.0, 353.0, 383.8, 464.8],
        "Depreciación y Amort": [75.0, 82.0, 90.0, 100.0, 105.0],
        "Utilidad Operacional (UAII / EBIT)": [207.0, 238.0, 263.0, 283.8, 359.8],
        "Gastos Financieros (Intereses)": [42.0, 50.0, 60.0, 88.0, 75.0],
        "Utilidad Antes Impuestos (UAI)": [165.0, 188.0, 203.0, 195.8, 284.8],
        "Impuestos (40%)": [66.0, 75.2, 81.2, 78.3, 113.9],
        "Utilidad Neta antes Pref": [99.0, 112.8, 121.8, 117.5, 170.9],
        "Dividendos Preferentes": [4.0, 4.0, 4.0, 4.0, 4.0],
        "Utilidad Neta": [95.0, 108.8, 117.8, 113.5, 166.9]
    }
    
    # Balance General
    bs_data = {
        "Efectivo y Equivalentes": [18.0, 20.0, 15.0, 10.0, 35.0],
        "Inversiones Corto Plazo": [50.0, 60.0, 65.0, 0.0, 20.0],
        "Cuentas por Cobrar": [260.0, 285.0, 315.0, 375.0, 365.0],
        "Inventarios": [340.0, 375.0, 415.0, 615.0, 520.0],
        "Total Activo Corriente": [668.0, 740.0, 810.0, 1000.0, 940.0],
        "Activo Fijo Neto (Planta y Eq)": [760.0, 810.0, 870.0, 1000.0, 1040.0],
        "Total Activo": [1428.0, 1550.0, 1680.0, 2000.0, 1980.0],
        "Cuentas por Pagar": [25.0, 28.0, 30.0, 60.0, 65.0],
        "Documentos por Pagar": [45.0, 50.0, 60.0, 110.0, 60.0],
        "Acumulaciones": [110.0, 120.0, 130.0, 140.0, 145.0],
        "Total Pasivo Corriente": [180.0, 198.0, 220.0, 310.0, 270.0],
        "Deuda a Largo Plazo": [510.0, 560.0, 580.0, 754.0, 670.0],
        "Total Pasivo": [690.0, 758.0, 800.0, 1064.0, 940.0],
        "Patrimonio Total": [738.0, 792.0, 840.0, 896.0, 1040.0]
    }
    
    # Flujo de Efectivo y Creación de Valor
    cf_eva = {
        "KTN Operativo (ActCteOp - PasCteOp)": [508.0, 532.0, 585.0, 800.0, 675.0],
        "Capital Fijo Operativo": [760.0, 810.0, 870.0, 1000.0, 1040.0],
        "Capital Operativo Total (KOT)": [1268.0, 1342.0, 1455.0, 1800.0, 1715.0],
        "Inversión Neta de Capital": [110.0, 74.0, 113.0, 345.0, -85.0],
        "UONDI = UAII * (1 - TasaImp)": [124.2, 142.8, 157.8, 170.28, 215.88],
        "Flujo de Efectivo Libre (FEL)": [14.2, 68.8, 44.8, -174.72, 300.88],
        "WACC (Costo de Capital Prom)": [0.105, 0.106, 0.108, 0.110, 0.107],
        "ROIC (UONDI / KOT)": [0.0979, 0.1064, 0.1085, 0.0946, 0.1259],
        "EVA (Economic Value Added)": [-8.94, 0.55, 0.66, -27.72, 32.38]
    }
    
    df_is = pd.DataFrame(is_data, index=years)
    df_bs = pd.DataFrame(bs_data, index=years)
    df_cf = pd.DataFrame(cf_eva, index=years)
    
    # Cálculo de Indicadores Clave
    ratios = {
        # Liquidez
        "Razón Corriente": df_bs["Total Activo Corriente"] / df_bs["Total Pasivo Corriente"],
        "Prueba Ácida": (df_bs["Total Activo Corriente"] - df_bs["Inventarios"]) / df_bs["Total Pasivo Corriente"],
        "Capital de Trabajo Neto": df_bs["Total Activo Corriente"] - df_bs["Total Pasivo Corriente"],
        
        # Actividad / Eficiencia
        "Rotación Inventarios (veces)": df_is["Ventas Netas"] / df_bs["Inventarios"],
        "Días de Inventario (EPI)": (df_bs["Inventarios"] / (df_is["Ventas Netas"] / 365.0)),
        "Días de Cartera (PPC)": (df_bs["Cuentas por Cobrar"] / (df_is["Ventas Netas"] / 365.0)),
        "Días de Proveedores (PPP)": ((df_bs["Cuentas por Pagar"] + df_bs["Acumulaciones"]) / (df_is["Costo de Ventas y Op"] / 365.0)),
        "Rotación Activo Fijo": df_is["Ventas Netas"] / df_bs["Activo Fijo Neto (Planta y Eq)"],
        "Rotación Activo Total": df_is["Ventas Netas"] / df_bs["Total Activo"],
        
        # Endeudamiento
        "Nivel de Endeudamiento (Leverage)": df_bs["Total Pasivo"] / df_bs["Total Activo"],
        "Cobertura de Intereses (RCI)": df_is["Utilidad Operacional (UAII / EBIT)"] / df_is["Gastos Financieros (Intereses)"],
        "Multiplicador del Patrimonio": df_bs["Total Activo"] / df_bs["Patrimonio Total"],
        
        # Rentabilidad
        "Margen Bruto": (df_is["Ventas Netas"] - df_is["Costo de Ventas y Op"]*0.7) / df_is["Ventas Netas"], # Proxy comercial
        "Margen EBITDA": df_is["EBITDA"] / df_is["Ventas Netas"],
        "Margen Operacional": df_is["Utilidad Operacional (UAII / EBIT)"] / df_is["Ventas Netas"],
        "Margen Neto": df_is["Utilidad Neta"] / df_is["Ventas Netas"],
        "ROA (Rentabilidad Activo)": df_is["Utilidad Neta"] / df_bs["Total Activo"],
        "ROE (Rentabilidad Patrimonio)": df_is["Utilidad Neta"] / df_bs["Patrimonio Total"],
        "ROIC": df_cf["ROIC (UONDI / KOT)"],
        "EVA": df_cf["EVA (Economic Value Added)"],
        "FEL": df_cf["Flujo de Efectivo Libre (FEL)"]
    }
    
    # Ciclo de Conversión de Efectivo (CCE)
    ratios["Ciclo Conversión Efectivo (CCE)"] = (
        ratios["Días de Inventario (EPI)"] + ratios["Días de Cartera (PPC)"] - ratios["Días de Proveedores (PPP)"]
    )
    
    df_ratios = pd.DataFrame(ratios, index=years)
    
    # Benchmarks de la Industria (del Taller MicroDrive / Andina)
    benchmarks = {
        "Razón Corriente": 4.2,
        "Prueba Ácida": 2.1,
        "Rotación Inventarios (veces)": 9.0,
        "Días de Cartera (PPC)": 36.0,
        "Rotación Activo Fijo": 3.0,
        "Rotación Activo Total": 1.8,
        "Nivel de Endeudamiento (Leverage)": 0.40,
        "Cobertura de Intereses (RCI)": 6.0,
        "Multiplicador del Patrimonio": 3.0,
        "Margen Neto": 0.05,
        "ROA (Rentabilidad Activo)": 0.09,
        "ROE (Rentabilidad Patrimonio)": 0.15,
        "Poder Adquisitivo Básico": 0.172
    }
    
    return df_is, df_bs, df_cf, df_ratios, benchmarks

df_is, df_bs, df_cf, df_ratios, benchmarks = load_financial_data()

# -------------------------------------------------------------
# BARRA LATERAL (SIDEBAR) - NAVEGACIÓN Y CONFIGURACIÓN
# -------------------------------------------------------------
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1551836022-d5d88e9218df?auto=format&fit=crop&w=400&q=80", use_container_width=True)
    st.title("Dist. Andina S.A.S.")
    st.caption("Sistema de Inteligencia y Control Financiero")
    
    st.markdown("---")
    
    selected_year = st.selectbox(
        "📅 Año de Análisis Principal:",
        options=[2024, 2025, 2023, 2022, 2021],
        index=0
    )
    
    benchmark_comparison = st.checkbox("Comparar contra Promedio Industria", value=True)
    
    st.markdown("---")
    st.markdown("### 🏢 Contexto Estratégico")
    st.info(
        """
        **Distribuciones Andina Comercial S.A.S.**  
        Distribuidora B2B colombiana de seguridad electrónica, redes y herramientas.  
        • **Propuesta de valor:** Disponibilidad inmediata y soporte técnico.  
        • **Reto crítico:** Disciplina de capital de trabajo y generación de caja.
        """
    )
    st.caption("Modelo Financiero 2021 - 2025")

# -------------------------------------------------------------
# ENCABEZADO PRINCIPAL
# -------------------------------------------------------------
st.markdown(f"""
<div class="main-header">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1>Dashboard Financiero Ejecutivo | Distribuciones Andina Comercial S.A.S.</h1>
            <p>Diagnóstico Estratégico-Financiero • Gestión de Capital de Trabajo • Creación de Valor (EVA & FEL)</p>
        </div>
        <div style="text-align: right;">
            <span style="background: rgba(255,255,255,0.2); padding: 6px 12px; border-radius: 20px; font-weight: 600;">
                Periodo Activo: {selected_year}
            </span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# RESUMEN EJECUTIVO KPI CARDS (Año Seleccionado)
# -------------------------------------------------------------
prev_year = selected_year - 1 if selected_year > 2021 else 2021

v_ventas = df_is.loc[selected_year, "Ventas Netas"]
delta_ventas = ((v_ventas / df_is.loc[prev_year, "Ventas Netas"]) - 1) * 100 if selected_year > 2021 else 0

v_ebitda = df_is.loc[selected_year, "EBITDA"]
m_ebitda = df_ratios.loc[selected_year, "Margen EBITDA"] * 100

v_rc = df_ratios.loc[selected_year, "Razón Corriente"]
v_end = df_ratios.loc[selected_year, "Nivel de Endeudamiento (Leverage)"] * 100

v_roe = df_ratios.loc[selected_year, "ROE (Rentabilidad Patrimonio)"] * 100
v_fel = df_cf.loc[selected_year, "Flujo de Efectivo Libre (FEL)"]
v_eva = df_cf.loc[selected_year, "EVA (Economic Value Added)"]

kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)

with kpi1:
    st.metric(
        label="Ventas Netas",
        value=f"${v_ventas:,.0f}M",
        delta=f"{delta_ventas:+.1f}% vs {prev_year}" if selected_year > 2021 else None
    )

with kpi2:
    st.metric(
        label="Margen EBITDA",
        value=f"{m_ebitda:.1f}%",
        delta=f"${v_ebitda:,.1f}M EBITDA"
    )

with kpi3:
    st.metric(
        label="Razón Corriente",
        value=f"{v_rc:.2f}x",
        delta="Ind: 4.2x" if benchmark_comparison else None,
        delta_color="normal" if v_rc >= 2.0 else "inverse"
    )

with kpi4:
    st.metric(
        label="Endeudamiento",
        value=f"{v_end:.1f}%",
        delta="Ind: 40.0%" if benchmark_comparison else None,
        delta_color="inverse"
    )

with kpi5:
    st.metric(
        label="ROE (Rent. Patr.)",
        value=f"{v_roe:.1f}%",
        delta="Ind: 15.0%" if benchmark_comparison else None
    )

with kpi6:
    st.metric(
        label="EVA (Valor Agregado)",
        value=f"${v_eva:,.1f}M",
        delta=f"FEL: ${v_fel:,.1f}M",
        delta_color="normal" if v_eva > 0 else "inverse"
    )

st.markdown("---")

# -------------------------------------------------------------
# PESTAÑAS PRINCIPALES DEL DASHBOARD
# -------------------------------------------------------------
tab_overview, tab_liquidity, tab_efficiency, tab_debt, tab_profit, tab_dupont, tab_eva_fel, tab_sim = st.tabs([
    "📈 Visión Global & Tendencias",
    "💧 Liquidez y Solvencia",
    "🔄 Eficiencia Operativa & CCE",
    "⚖️ Endeudamiento & Apalancamiento",
    "💰 Rentabilidad & Márgenes",
    "🧩 Descomposición DuPont",
    "💎 Creación de Valor (EVA & FEL)",
    "🎛️ Simulador Gerencial de Sensibilidad"
])

# =============================================================
# TAB 1: VISIÓN GLOBAL & TENDENCIAS
# =============================================================
with tab_overview:
    st.subheader("Trayectoria Financiera Multianual (2021 - 2025)")
    st.markdown('<p class="tab-subtitle">Evolución de los ingresos, estructura de rentabilidad y acumulación de activos en Distribuciones Andina S.A.S.</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([7, 5])
    
    with col1:
        fig_revenue = go.Figure()
        fig_revenue.add_trace(go.Bar(
            x=df_is.index,
            y=df_is["Ventas Netas"],
            name="Ventas Netas",
            marker_color="#1E3D59"
        ))
        fig_revenue.add_trace(go.Scatter(
            x=df_is.index,
            y=df_is["EBITDA"],
            name="EBITDA",
            yaxis="y2",
            mode="lines+markers",
            line=dict(color="#17B978", width=3)
        ))
        fig_revenue.add_trace(go.Scatter(
            x=df_is.index,
            y=df_is["Utilidad Neta"],
            name="Utilidad Neta",
            yaxis="y2",
            mode="lines+markers",
            line=dict(color="#FF6E40", width=3, dash="dot")
        ))
        
        fig_revenue.update_layout(
            title="Evolución de Ventas vs Rentabilidad Operativa y Neta",
            xaxis=dict(title="Año"),
            yaxis=dict(title="Ventas Netas ($M)", showgrid=False),
            yaxis2=dict(title="EBITDA / Utilidad Neta ($M)", overlaying="y", side="right", showgrid=True),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=40, r=40, t=50, b=40),
            hovermode="x unified"
        )
        st.plotly_chart(fig_revenue, use_container_width=True)
        
    with col2:
        # Estructura del Balance General
        fig_bs = go.Figure()
        fig_bs.add_trace(go.Bar(
            x=df_bs.index,
            y=df_bs["Total Activo Corriente"],
            name="Activo Corriente",
            marker_color="#438a5e"
        ))
        fig_bs.add_trace(go.Bar(
            x=df_bs.index,
            y=df_bs["Activo Fijo Neto (Planta y Eq)"],
            name="Activo Fijo Neto",
            marker_color="#2b580c"
        ))
        fig_bs.update_layout(
            barmode="stack",
            title="Composición del Activo Total ($M)",
            xaxis=dict(title="Año"),
            yaxis=dict(title="Activos ($M)"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=40, r=40, t=50, b=40)
        )
        st.plotly_chart(fig_bs, use_container_width=True)

    # Diagnóstico del caso
    st.markdown("### 📋 Resumen del Diagnóstico Estratégico-Financiero")
    st.markdown(
        """
        - **Crecimiento Comercial sostenido:** Las ventas crecieron de **$2,350M en 2021** a **$3,000M en 2024** y proyectadas en **$3,320M en 2025**.
        - **El cuello de botella de 2021-2024 ('Vender sin generar caja'):** La fuerte expansión del portafolio y los tiempos de entrega confiables generaron una acumulación de inventarios (llegando a **$615M en 2024**) y cuentas por cobrar (**$375M**), presionando la tesorería.
        - **Punto de Inflexión 2025:** Implementación del canal digital B2B, optimización de compras y políticas de cobranza que reducen el inventario a **$520M**, normalizando el capital de trabajo y restaurando la generación neta de efectivo libre (**$300.9M**).
        """
    )

# =============================================================
# TAB 2: LIQUIDEZ Y SOLVENCIA
# =============================================================
with tab_liquidity:
    st.subheader("Diagnóstico de Liquidez y Capacidad de Pago a Corto Plazo")
    st.markdown('<p class="tab-subtitle">Evaluación de la cobertura de pasivos corrientes y dependencia del inventario físico.</p>', unsafe_allow_html=True)
    
    col_l1, col_l2 = st.columns([7, 5])
    
    with col_l1:
        fig_liq = go.Figure()
        fig_liq.add_trace(go.Scatter(
            x=df_ratios.index,
            y=df_ratios["Razón Corriente"],
            mode="lines+markers",
            name="Razón Corriente",
            line=dict(color="#1f77b4", width=3)
        ))
        fig_liq.add_trace(go.Scatter(
            x=df_ratios.index,
            y=df_ratios["Prueba Ácida"],
            mode="lines+markers",
            name="Prueba Ácida",
            line=dict(color="#ff7f0e", width=3)
        ))
        if benchmark_comparison:
            fig_liq.add_hline(y=benchmarks["Razón Corriente"], line_dash="dash", line_color="#1f77b4", 
                              annotation_text=f"Benchmark Razón Corr ({benchmarks['Razón Corriente']}x)")
            fig_liq.add_hline(y=benchmarks["Prueba Ácida"], line_dash="dash", line_color="#ff7f0e", 
                              annotation_text=f"Benchmark Prueba Ácida ({benchmarks['Prueba Ácida']}x)")
            
        fig_liq.update_layout(
            title="Evolución de Ratios de Liquidez vs Industria",
            xaxis=dict(title="Año"),
            yaxis=dict(title="Veces (x)"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=40, r=40, t=50, b=40)
        )
        st.plotly_chart(fig_liq, use_container_width=True)
        
    with col_l2:
        # Gráfico de componentes del activo corriente vs pasivo corriente
        curr_year_data = pd.DataFrame({
            "Componente": ["Efectivo", "Inversiones", "Cuentas por Cobrar", "Inventarios", "Pasivo Corriente"],
            "Monto ($M)": [
                df_bs.loc[selected_year, "Efectivo y Equivalentes"],
                df_bs.loc[selected_year, "Inversiones Corto Plazo"],
                df_bs.loc[selected_year, "Cuentas por Cobrar"],
                df_bs.loc[selected_year, "Inventarios"],
                df_bs.loc[selected_year, "Total Pasivo Corriente"]
            ],
            "Tipo": ["Activo", "Activo", "Activo", "Activo", "Pasivo"]
        })
        fig_comp = px.bar(
            curr_year_data,
            x="Componente",
            y="Monto ($M)",
            color="Tipo",
            color_discrete_map={"Activo": "#2ca02c", "Pasivo": "#d62728"},
            title=f"Estructura Corriente ({selected_year})"
        )
        fig_comp.update_layout(margin=dict(l=40, r=40, t=50, b=40), showlegend=False)
        st.plotly_chart(fig_comp, use_container_width=True)
        
    st.info(
        f"""
        **💡 Interpretación Experta para {selected_year}:**  
        • **Razón Corriente:** **{df_ratios.loc[selected_year, 'Razón Corriente']:.2f} veces** (Industria: {benchmarks['Razón Corriente']} veces). Por cada peso en pasivos a corto plazo, la empresa dispone de ${df_ratios.loc[selected_year, 'Razón Corriente']:.2f} en activos corrientes.  
        • **Prueba Ácida:** **{df_ratios.loc[selected_year, 'Prueba Ácida']:.2f} veces** (Industria: {benchmarks['Prueba Ácida']} veces). Al excluir inventarios (el activo menos líquido), la cobertura disminuye sustancialmente, evidenciando que una gran porción de la solvencia inmediata depende de la rotación efectiva de las existencias.
        """
    )

# =============================================================
# TAB 3: EFICIENCIA OPERATIVA & CICLO DE EFECTIVO
# =============================================================
with tab_efficiency:
    st.subheader("Ciclo de Conversión de Efectivo (CCE) y Eficiencia Operativa")
    st.markdown('<p class="tab-subtitle">Análisis del tiempo que toma transformar la inversión en inventarios y cartera en efectivo disponible en banco.</p>', unsafe_allow_html=True)
    
    col_e1, col_e2 = st.columns([6, 6])
    
    with col_e1:
        # Gráfico de días de ciclo de efectivo
        fig_cce = go.Figure()
        fig_cce.add_trace(go.Bar(
            x=df_ratios.index,
            y=df_ratios["Días de Inventario (EPI)"],
            name="(+) Días Inventario (EPI)",
            marker_color="#f39c12"
        ))
        fig_cce.add_trace(go.Bar(
            x=df_ratios.index,
            y=df_ratios["Días de Cartera (PPC)"],
            name="(+) Días Cobranza (PPC)",
            marker_color="#3498db"
        ))
        fig_cce.add_trace(go.Bar(
            x=df_ratios.index,
            y=-df_ratios["Días de Proveedores (PPP)"],
            name="(-) Días Proveedores (PPP)",
            marker_color="#9b59b6"
        ))
        fig_cce.add_trace(go.Scatter(
            x=df_ratios.index,
            y=df_ratios["Ciclo Conversión Efectivo (CCE)"],
            name="CCE Neto (Días)",
            mode="lines+markers",
            line=dict(color="#e74c3c", width=4)
        ))
        fig_cce.update_layout(
            barmode="relative",
            title="Desglose del Ciclo de Conversión de Efectivo (Días)",
            xaxis=dict(title="Año"),
            yaxis=dict(title="Días"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=40, r=40, t=50, b=40)
        )
        st.plotly_chart(fig_cce, use_container_width=True)
        
    with col_e2:
        # Rotación de Activos Fijos y Totales
        fig_rot = go.Figure()
        fig_rot.add_trace(go.Scatter(
            x=df_ratios.index,
            y=df_ratios["Rotación Inventarios (veces)"],
            name="Rot. Inventarios",
            mode="lines+markers",
            line=dict(color="#d35400", width=2.5)
        ))
        fig_rot.add_trace(go.Scatter(
            x=df_ratios.index,
            y=df_ratios["Rotación Activo Fijo"],
            name="Rot. Activo Fijo",
            mode="lines+markers",
            line=dict(color="#27ae60", width=2.5)
        ))
        fig_rot.add_trace(go.Scatter(
            x=df_ratios.index,
            y=df_ratios["Rotación Activo Total"],
            name="Rot. Activo Total",
            mode="lines+markers",
            line=dict(color="#2980b9", width=2.5)
        ))
        if benchmark_comparison:
            fig_rot.add_hline(y=benchmarks["Rotación Inventarios (veces)"], line_dash="dash", line_color="#d35400", 
                              annotation_text=f"Benchmark Rot. Inv ({benchmarks['Rotación Inventarios (veces)']}x)")
            fig_rot.add_hline(y=benchmarks["Rotación Activo Total"], line_dash="dash", line_color="#2980b9", 
                              annotation_text=f"Benchmark Rot. Act Total ({benchmarks['Rotación Activo Total']}x)")

        fig_rot.update_layout(
            title="Ratios de Rotación de Activos (Veces al año)",
            xaxis=dict(title="Año"),
            yaxis=dict(title="Veces (x)"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=40, r=40, t=50, b=40)
        )
        st.plotly_chart(fig_rot, use_container_width=True)
        
    # Tabla resumen de actividad para el año
    cce_val = df_ratios.loc[selected_year, 'Ciclo Conversión Efectivo (CCE)']
    epi_val = df_ratios.loc[selected_year, 'Días de Inventario (EPI)']
    ppc_val = df_ratios.loc[selected_year, 'Días de Cartera (PPC)']
    ppp_val = df_ratios.loc[selected_year, 'Días de Proveedores (PPP)']
    
    col_t1, col_t2, col_t3, col_t4 = st.columns(4)
    col_t1.metric("Días Inventario (EPI)", f"{epi_val:.1f} días", delta=f"{df_ratios.loc[selected_year, 'Rotación Inventarios (veces)']:.1f}x Rot.")
    col_t2.metric("Días Cobranza (PPC)", f"{ppc_val:.1f} días", delta=f"Bench: {benchmarks['Días de Cartera (PPC)']:.0f} días", delta_color="inverse")
    col_t3.metric("Días Proveedores (PPP)", f"{ppp_val:.1f} días", delta="Financiamiento comercial")
    col_t4.metric("CCE Neto", f"{cce_val:.1f} días", delta="Días para recuperar caja", delta_color="inverse" if cce_val > 80 else "normal")

# =============================================================
# TAB 4: ENDEUDAMIENTO & APALANCAMIENTO
# =============================================================
with tab_debt:
    st.subheader("Estructura de Capital, Solvencia a Largo Plazo y Cobertura")
    st.markdown('<p class="tab-subtitle">Análisis de la proporción de pasivos frente a activos y la capacidad operativa de pagar los intereses de la deuda.</p>', unsafe_allow_html=True)
    
    col_d1, col_d2 = st.columns([6, 6])
    
    with col_d1:
        # Composición Pasivo vs Patrimonio
        fig_cap = go.Figure()
        fig_cap.add_trace(go.Bar(
            x=df_bs.index,
            y=df_bs["Total Pasivo Corriente"],
            name="Pasivo Corriente",
            marker_color="#e74c3c"
        ))
        fig_cap.add_trace(go.Bar(
            x=df_bs.index,
            y=df_bs["Deuda a Largo Plazo"],
            name="Deuda Largo Plazo",
            marker_color="#c0392b"
        ))
        fig_cap.add_trace(go.Bar(
            x=df_bs.index,
            y=df_bs["Patrimonio Total"],
            name="Patrimonio Neto",
            marker_color="#27ae60"
        ))
        fig_cap.update_layout(
            barmode="stack",
            title="Estructura de Financiamiento ($M)",
            xaxis=dict(title="Año"),
            yaxis=dict(title="Monto ($M)"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=40, r=40, t=50, b=40)
        )
        st.plotly_chart(fig_cap, use_container_width=True)
        
    with col_d2:
        # Cobertura de Intereses vs Nivel de Endeudamiento
        fig_cob = make_subplots(specs=[[{"secondary_y": True}]])
        fig_cob.add_trace(
            go.Scatter(x=df_ratios.index, y=df_ratios["Nivel de Endeudamiento (Leverage)"]*100, 
                       name="Nivel Endeudamiento (%)", line=dict(color="#e67e22", width=3)),
            secondary_y=False
        )
        fig_cob.add_trace(
            go.Scatter(x=df_ratios.index, y=df_ratios["Cobertura de Intereses (RCI)"], 
                       name="Cobertura Intereses (veces)", line=dict(color="#2980b9", width=3, dash="dot")),
            secondary_y=True
        )
        if benchmark_comparison:
            fig_cob.add_hline(y=benchmarks["Nivel de Endeudamiento (Leverage)"]*100, line_dash="dash", line_color="#e67e22",
                              annotation_text=f"Benchmark Deuda ({benchmarks['Nivel de Endeudamiento (Leverage)']*100:.0f}%)", secondary_y=False)
            fig_cob.add_hline(y=benchmarks["Cobertura de Intereses (RCI)"], line_dash="dash", line_color="#2980b9",
                              annotation_text=f"Benchmark RCI ({benchmarks['Cobertura de Intereses (RCI)']}x)", secondary_y=True)
            
        fig_cob.update_layout(
            title="Endeudamiento (%) vs Cobertura de Intereses (x)",
            xaxis=dict(title="Año"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=40, r=40, t=50, b=40)
        )
        fig_cob.update_yaxes(title_text="Nivel de Deuda (%)", secondary_y=False)
        fig_cob.update_yaxes(title_text="Cobertura Intereses (x)", secondary_y=True)
        st.plotly_chart(fig_cob, use_container_width=True)
        
    st.warning(
        f"""
        **⚠️ Evaluación de Riesgo Crediticio ({selected_year}):**  
        • **Apalancamiento:** {df_ratios.loc[selected_year, 'Nivel de Endeudamiento (Leverage)']*100:.1f}% de los activos están financiados por acreedores (Frente al {benchmarks['Nivel de Endeudamiento (Leverage)']*100:.0f}% del estándar de la industria).  
        • **Multiplicador de Patrimonio:** {df_ratios.loc[selected_year, 'Multiplicador del Patrimonio']:.2f}x.  
        • **Cobertura de Intereses (RCI):** {df_ratios.loc[selected_year, 'Cobertura de Intereses (RCI)']:.2f} veces (Promedio Industria: {benchmarks['Cobertura de Intereses (RCI)']} veces). En 2024 el costo financiero aumentó a $88M erosionando la ganancia operativa y comprimiendo la holgura ante shocks de tasas.
        """
    )

# =============================================================
# TAB 5: RENTABILIDAD & MÁRGENES
# =============================================================
with tab_profit:
    st.subheader("Cascada de Rentabilidad y Retornos sobre la Inversión")
    st.markdown('<p class="tab-subtitle">Análisis del margen EBITDA, margen operacional, margen neto y rendimientos sobre activos (ROA) y patrimonio (ROE).</p>', unsafe_allow_html=True)
    
    col_p1, col_p2 = st.columns([6, 6])
    
    with col_p1:
        # Gráfico de Márgenes
        fig_mrg = go.Figure()
        fig_mrg.add_trace(go.Scatter(x=df_ratios.index, y=df_ratios["Margen EBITDA"]*100, name="Margen EBITDA (%)", line=dict(color="#27ae60", width=3)))
        fig_mrg.add_trace(go.Scatter(x=df_ratios.index, y=df_ratios["Margen Operacional"]*100, name="Margen Operacional (%)", line=dict(color="#2980b9", width=3)))
        fig_mrg.add_trace(go.Scatter(x=df_ratios.index, y=df_ratios["Margen Neto"]*100, name="Margen Neto (%)", line=dict(color="#8e44ad", width=3)))
        
        if benchmark_comparison:
            fig_mrg.add_hline(y=benchmarks["Margen Neto"]*100, line_dash="dash", line_color="#8e44ad", annotation_text=f"Benchmark Margen Neto ({benchmarks['Margen Neto']*100:.1f}%)")
            
        fig_mrg.update_layout(
            title="Evolución de Márgenes de Utilidad (%)",
            xaxis=dict(title="Año"),
            yaxis=dict(title="Porcentaje (%)"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=40, r=40, t=50, b=40)
        )
        st.plotly_chart(fig_mrg, use_container_width=True)
        
    with col_p2:
        # Retorno ROA vs ROE
        fig_ret = go.Figure()
        fig_ret.add_trace(go.Bar(x=df_ratios.index, y=df_ratios["ROA (Rentabilidad Activo)"]*100, name="ROA (%)", marker_color="#16a085"))
        fig_ret.add_trace(go.Bar(x=df_ratios.index, y=df_ratios["ROE (Rentabilidad Patrimonio)"]*100, name="ROE (%)", marker_color="#2c3e50"))
        
        if benchmark_comparison:
            fig_ret.add_hline(y=benchmarks["ROA (Rentabilidad Activo)"]*100, line_dash="dash", line_color="#16a085", annotation_text=f"Bench ROA ({benchmarks['ROA (Rentabilidad Activo)']*100:.1f}%)")
            fig_ret.add_hline(y=benchmarks["ROE (Rentabilidad Patrimonio)"]*100, line_dash="dash", line_color="#2c3e50", annotation_text=f"Bench ROE ({benchmarks['ROE (Rentabilidad Patrimonio)']*100:.1f}%)")
            
        fig_ret.update_layout(
            barmode="group",
            title="Rentabilidad sobre Activos (ROA) vs Patrimonio (ROE)",
            xaxis=dict(title="Año"),
            yaxis=dict(title="Porcentaje (%)"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=40, r=40, t=50, b=40)
        )
        st.plotly_chart(fig_ret, use_container_width=True)
        
    # Cascada de Resultados del Año Seleccionado
    st.markdown(f"#### Cascada del Estado de Resultados ({selected_year})")
    wf_data = [
        {"x": "Ventas Netas", "y": df_is.loc[selected_year, "Ventas Netas"]},
        {"x": "Costos y Gastos Op", "y": -df_is.loc[selected_year, "Costo de Ventas y Op"]},
        {"x": "Depreciación", "y": -df_is.loc[selected_year, "Depreciación y Amort"]},
        {"x": "Gastos Financieros", "y": -df_is.loc[selected_year, "Gastos Financieros (Intereses)"]},
        {"x": "Impuestos", "y": -df_is.loc[selected_year, "Impuestos (40%)"]},
        {"x": "Div. Preferentes", "y": -df_is.loc[selected_year, "Dividendos Preferentes"]},
        {"x": "Utilidad Neta", "y": df_is.loc[selected_year, "Utilidad Neta"]}
    ]
    
    fig_wf = go.Figure(go.Waterfall(
        name="Resultados",
        orientation="v",
        measure=["absolute", "relative", "relative", "relative", "relative", "relative", "total"],
        x=[d["x"] for d in wf_data],
        y=[d["y"] for d in wf_data],
        connector={"line": {"color": "rgb(63, 63, 63)"}},
        decreasing={"marker": {"color": "#e74c3c"}},
        increasing={"marker": {"color": "#2ecc71"}},
        totals={"marker": {"color": "#3498db"}}
    ))
    fig_wf.update_layout(
        title=f"Flujo de Generación de Utilidad Neta ($M) - Año {selected_year}",
        yaxis=dict(title="Millones ($)"),
        margin=dict(l=40, r=40, t=50, b=40)
    )
    st.plotly_chart(fig_wf, use_container_width=True)

# =============================================================
# TAB 6: DESCOMPOSICIÓN DUPONT
# =============================================================
with tab_dupont:
    st.subheader("Análisis DuPont de 3 Factores: Desagregación del ROE")
    st.markdown(
        """
        <p class="tab-subtitle">
        La identidad de DuPont explica cómo la rentabilidad de los accionistas (ROE) se genera a partir de tres motores:  
        <b>ROE = Margen Neto (Rentabilidad) × Rotación del Activo (Eficiencia) × Multiplicador del Patrimonio (Apalancamiento)</b>
        </p>
        """, 
        unsafe_allow_html=True
    )
    
    col_dup1, col_dup2 = st.columns([5, 7])
    
    with col_dup1:
        st.markdown(f"### 🔍 Desglose para el Año {selected_year}")
        m_net = df_ratios.loc[selected_year, "Margen Neto"]
        rot_act = df_ratios.loc[selected_year, "Rotación Activo Total"]
        mult_pat = df_ratios.loc[selected_year, "Multiplicador del Patrimonio"]
        roe_val = df_ratios.loc[selected_year, "ROE (Rentabilidad Patrimonio)"]
        
        st.markdown(f"""
        <div style="background-color: #f8fafc; border-radius: 8px; padding: 20px; border-left: 5px solid #2563eb;">
            <p style="font-size: 16px; margin-bottom: 8px;"><b>1. Margen Neto (Eficacia Operativa y Precios):</b><br>
            <span style="font-size: 22px; font-weight: 700; color: #1e293b;">{m_net*100:.2f}%</span> (Ganancia por peso vendido)</p>
            <p style="font-size: 16px; margin-bottom: 8px;"><b>2. Rotación del Activo Total (Productividad de Capital):</b><br>
            <span style="font-size: 22px; font-weight: 700; color: #1e293b;">{rot_act:.2f} veces</span> (Ventas generadas por activo)</p>
            <p style="font-size: 16px; margin-bottom: 8px;"><b>3. Multiplicador de Patrimonio (Efecto Deuda):</b><br>
            <span style="font-size: 22px; font-weight: 700; color: #1e293b;">{mult_pat:.2f} veces</span> (Activo total / Patrimonio)</p>
            <hr style="margin: 15px 0;">
            <p style="font-size: 18px; margin: 0;"><b>ROE Resultante:</b><br>
            <span style="font-size: 28px; font-weight: 800; color: #2563eb;">{roe_val*100:.2f}%</span></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.caption(f"Fórmula: {m_net*100:.2f}% × {rot_act:.2f} × {mult_pat:.2f} = {roe_val*100:.2f}%")
        
    with col_dup2:
        # Comparativo histórico de los 3 componentes normalizados
        dup_df = pd.DataFrame({
            "Margen Neto (%)": df_ratios["Margen Neto"] * 100,
            "Rotación Activo (x)": df_ratios["Rotación Activo Total"],
            "Multiplicador (x)": df_ratios["Multiplicador del Patrimonio"],
            "ROE (%)": df_ratios["ROE (Rentabilidad Patrimonio)"] * 100
        }, index=df_ratios.index)
        
        fig_dup = make_subplots(rows=3, cols=1, shared_xaxes=True, 
                                subplot_titles=["Margen Neto (%)", "Rotación del Activo Total (x)", "Multiplicador del Patrimonio (x)"])
        fig_dup.add_trace(go.Scatter(x=dup_df.index, y=dup_df["Margen Neto (%)"], mode="lines+markers", line=dict(color="#8e44ad", width=3)), row=1, col=1)
        fig_dup.add_trace(go.Scatter(x=dup_df.index, y=dup_df["Rotación Activo (x)"], mode="lines+markers", line=dict(color="#2980b9", width=3)), row=2, col=1)
        fig_dup.add_trace(go.Scatter(x=dup_df.index, y=dup_df["Multiplicador (x)"], mode="lines+markers", line=dict(color="#e67e22", width=3)), row=3, col=1)
        
        fig_dup.update_layout(height=450, showlegend=False, margin=dict(l=40, r=40, t=40, b=40))
        st.plotly_chart(fig_dup, use_container_width=True)
        
    st.info(
        """
        **💡 Conclusión del Análisis DuPont en Andina:**  
        En 2024 el ROE cayó a **12.67%** (desde **14.02%** en 2023) a pesar de haber incrementado el apalancamiento financiero (el multiplicador subió de 2.0x a 2.23x). Esto demuestra que el mayor endeudamiento no pudo compensar el deterioro simultáneo del margen neto (debido a mayores costos financieros) y la menor rotación de activos provocada por la inmovilización de inventarios. En 2025, la mejora en rotación y margen impulsa el ROE por encima del 16%.
        """
    )

# =============================================================
# TAB 7: CREACIÓN DE VALOR (EVA & FEL)
# =============================================================
with tab_eva_fel:
    st.subheader("Evaluación de Creación de Valor: ROIC, WACC, EVA y Flujo de Efectivo Libre")
    st.markdown('<p class="tab-subtitle">El verdadero valor económico: ¿Gana la empresa más de lo que le cuesta financiar su operación?</p>', unsafe_allow_html=True)
    
    col_v1, col_v2 = st.columns([6, 6])
    
    with col_v1:
        # Gráfico ROIC vs WACC y Spread
        fig_spread = go.Figure()
        fig_spread.add_trace(go.Bar(
            x=df_cf.index,
            y=df_cf["ROIC (UONDI / KOT)"] * 100,
            name="ROIC (%) Retorno Capital",
            marker_color="#2ecc71"
        ))
        fig_spread.add_trace(go.Bar(
            x=df_cf.index,
            y=df_cf["WACC (Costo de Capital Prom)"] * 100,
            name="WACC (%) Costo Capital",
            marker_color="#e74c3c"
        ))
        fig_spread.update_layout(
            barmode="group",
            title="Retorno del Capital (ROIC) vs Costo de Capital (WACC)",
            xaxis=dict(title="Año"),
            yaxis=dict(title="Porcentaje (%)"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=40, r=40, t=50, b=40)
        )
        st.plotly_chart(fig_spread, use_container_width=True)
        
    with col_v2:
        # EVA Histórico
        fig_eva = go.Figure()
        colors = ["#27ae60" if v >= 0 else "#c0392b" for v in df_cf["EVA (Economic Value Added)"]]
        fig_eva.add_trace(go.Bar(
            x=df_cf.index,
            y=df_cf["EVA (Economic Value Added)"],
            marker_color=colors,
            name="EVA ($M)"
        ))
        fig_eva.add_hline(y=0, line_dash="solid", line_color="#333333")
        fig_eva.update_layout(
            title="Valor Económico Agregado - EVA ($ Millones)",
            xaxis=dict(title="Año"),
            yaxis=dict(title="EVA ($M)"),
            margin=dict(l=40, r=40, t=50, b=40)
        )
        st.plotly_chart(fig_eva, use_container_width=True)
        
    st.markdown("---")
    
    # Análisis del Flujo de Efectivo Libre (FEL)
    col_fel1, col_fel2 = st.columns([7, 5])
    
    with col_fel1:
        fig_fel = go.Figure()
        fig_fel.add_trace(go.Scatter(
            x=df_cf.index,
            y=df_cf["UONDI = UAII * (1 - TasaImp)"],
            name="UONDI (Ganancia Op Neta)",
            mode="lines+markers",
            line=dict(color="#2980b9", width=3)
        ))
        fig_fel.add_trace(go.Bar(
            x=df_cf.index,
            y=df_cf["Inversión Neta de Capital"],
            name="Inversión Neta en KOT",
            marker_color="#e67e22"
        ))
        fig_fel.add_trace(go.Scatter(
            x=df_cf.index,
            y=df_cf["Flujo de Efectivo Libre (FEL)"],
            name="Flujo de Efectivo Libre (FEL)",
            mode="lines+markers",
            line=dict(color="#16a085", width=4)
        ))
        fig_fel.update_layout(
            title="Flujo de Efectivo Libre: UONDI vs Inversión Neta de Capital ($M)",
            xaxis=dict(title="Año"),
            yaxis=dict(title="Monto ($M)"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=40, r=40, t=50, b=40)
        )
        st.plotly_chart(fig_fel, use_container_width=True)
        
    with col_fel2:
        st.markdown(f"### 📊 Balance de Creación de Valor ({selected_year})")
        kot_y = df_cf.loc[selected_year, "Capital Operativo Total (KOT)"]
        uondi_y = df_cf.loc[selected_year, "UONDI = UAII * (1 - TasaImp)"]
        inv_y = df_cf.loc[selected_year, "Inversión Neta de Capital"]
        fel_y = df_cf.loc[selected_year, "Flujo de Efectivo Libre (FEL)"]
        roic_y = df_cf.loc[selected_year, "ROIC (UONDI / KOT)"] * 100
        wacc_y = df_cf.loc[selected_year, "WACC (Costo de Capital Prom)"] * 100
        eva_y = df_cf.loc[selected_year, "EVA (Economic Value Added)"]
        
        st.markdown(f"""
        - **Capital Operativo (KOT):** ${kot_y:,.1f}M  
        - **UONDI:** ${uondi_y:,.2f}M  
        - **Inversión Neta:** ${inv_y:,.1f}M  
        - **Flujo Efectivo Libre (FEL):** <b style="color: {'#27ae60' if fel_y >= 0 else '#c0392b'};">${fel_y:,.2f}M</b>  
        - **ROIC:** {roic_y:.2f}% vs **WACC:** {wacc_y:.2f}%  
        - **Spread de Valor (ROIC - WACC):** <b style="color: {'#27ae60' if roic_y >= wacc_y else '#c0392b'};">{roic_y - wacc_y:+.2f}%</b>  
        - **EVA Generado:** <b style="color: {'#27ae60' if eva_y >= 0 else '#c0392b'};">${eva_y:,.2f}M</b>
        """)
        
        if eva_y < 0:
            st.error(f"⚠️ Destrucción de valor en {selected_year}: El retorno de capital ({roic_y:.2f}%) fue inferior al costo de financiarlo ({wacc_y:.2f}%), generando un EVA negativo de ${abs(eva_y):.1f}M.")
        else:
            st.success(f"✅ Creación efectiva de valor en {selected_year}: Spread positivo de {roic_y - wacc_y:.2f}%, aportando ${eva_y:.1f}M de valor económico añadido.")

# =============================================================
# TAB 8: SIMULADOR GERENCIAL DE SENSIBILIDAD
# =============================================================
with tab_sim:
    st.subheader("Simulador Gerencial Interactivo: Sensibilidad de Caja y Creación de Valor")
    st.markdown('<p class="tab-subtitle">Modifica variables operativas y de financiamiento para simular el impacto en el FEL, el EVA y la solvencia de la empresa.</p>', unsafe_allow_html=True)
    
    sim_c1, sim_c2, sim_c3 = st.columns(3)
    
    with sim_c1:
        st.markdown("##### 📦 Gestión de Inventario y Ventas")
        sim_ventas_var = st.slider("Crecimiento de Ventas (%):", -20.0, 30.0, 5.0, 1.0)
        sim_dias_inv = st.slider("Días de Inventario Objetivo (EPI):", 30, 90, int(df_ratios.loc[selected_year, "Días de Inventario (EPI)"]), 2)
        
    with sim_c2:
        st.markdown("##### 💳 Cartera y Proveedores")
        sim_dias_cartera = st.slider("Días de Cartera Objetivo (PPC):", 25, 75, int(df_ratios.loc[selected_year, "Días de Cartera (PPC)"]), 2)
        sim_dias_prov = st.slider("Días de Proveedores Objetivo (PPP):", 15, 60, int(df_ratios.loc[selected_year, "Días de Proveedores (PPP)"]), 2)
        
    with sim_c3:
        st.markdown("##### 🏦 Estructura de Capital y Costo")
        sim_wacc = st.slider("WACC / Costo de Capital (%):", 8.0, 15.0, float(df_cf.loc[selected_year, "WACC (Costo de Capital Prom)"]*100), 0.2)
        sim_margen_op = st.slider("Margen Operacional EBIT (%):", 5.0, 15.0, float(df_ratios.loc[selected_year, "Margen Operacional"]*100), 0.2)

    # Cálculos de Simulación
    base_ventas = df_is.loc[selected_year, "Ventas Netas"] * (1 + sim_ventas_var/100.0)
    sim_ebit = base_ventas * (sim_margen_op / 100.0)
    sim_uondi = sim_ebit * (1 - 0.40) # Tasa de impuestos 40%
    
    # Nuevas necesidades de capital de trabajo
    sim_inv = (sim_dias_inv / 365.0) * base_ventas
    sim_cxc = (sim_dias_cartera / 365.0) * base_ventas
    sim_cxp = (sim_dias_prov / 365.0) * (base_ventas * 0.85) # Aproximación costo de ventas
    
    sim_ktn = sim_cxc + sim_inv - sim_cxp
    sim_kfo = df_cf.loc[selected_year, "Capital Fijo Operativo"] # Manteniendo base
    sim_kot = sim_ktn + sim_kfo
    
    inv_neta_sim = sim_kot - df_cf.loc[prev_year, "Capital Operativo Total (KOT)"]
    sim_fel = sim_uondi - inv_neta_sim
    sim_roic = (sim_uondi / sim_kot) * 100
    sim_eva = sim_uondi - (sim_kot * (sim_wacc / 100.0))
    sim_cce = sim_dias_inv + sim_dias_cartera - sim_dias_prov
    
    st.markdown("---")
    st.markdown("### 🎯 Resultados Proyectados de la Simulación")
    
    r_col1, r_col2, r_col3, r_col4, r_col5 = st.columns(5)
    r_col1.metric("Ventas Simuladas", f"${base_ventas:,.0f}M", delta=f"{sim_ventas_var:+.1f}%")
    r_col2.metric("CCE Simulado", f"{sim_cce:.0f} días", delta=f"{sim_cce - df_ratios.loc[selected_year, 'Ciclo Conversión Efectivo (CCE)']:+.0f} días")
    r_col3.metric("ROIC Simulado", f"{sim_roic:.2f}%", delta=f"{sim_roic - sim_wacc:+.2f}% Spread")
    r_col4.metric("FEL Simulado", f"${sim_fel:,.1f}M", delta_color="normal" if sim_fel > 0 else "inverse")
    r_col5.metric("EVA Simulado", f"${sim_eva:,.1f}M", delta_color="normal" if sim_eva > 0 else "inverse")
    
    st.markdown("---")
    
    # Comparativa Gráfica de Escenarios: Actual vs Simulado
    esc_df = pd.DataFrame({
        "Métrica": ["UONDI ($M)", "Capital Op (KOT) ($M)", "FEL ($M)", "EVA ($M)"],
        "Año Actual": [
            df_cf.loc[selected_year, "UONDI = UAII * (1 - TasaImp)"],
            df_cf.loc[selected_year, "Capital Operativo Total (KOT)"],
            df_cf.loc[selected_year, "Flujo de Efectivo Libre (FEL)"],
            df_cf.loc[selected_year, "EVA (Economic Value Added)"]
        ],
        "Escenario Simulado": [sim_uondi, sim_kot, sim_fel, sim_eva]
    })
    
    fig_esc = px.bar(
        esc_df.melt(id_vars="Métrica", var_name="Escenario", value_name="Valor"),
        x="Métrica",
        y="Valor",
        color="Escenario",
        barmode="group",
        color_discrete_map={"Año Actual": "#7f8c8d", "Escenario Simulado": "#2980b9"},
        title="Comparativo de Métricas Clave: Actual vs Simulado"
    )
    st.plotly_chart(fig_esc, use_container_width=True)

# -------------------------------------------------------------
# TABLA DE DATOS DETALLADOS Y DESCARGA
# -------------------------------------------------------------
with st.expander("📥 Ver Tablas Detalladas de Indicadores y Estados Financieros"):
    st.markdown("### Tabla Maestra de Indicadores Financieros (2021 - 2025)")
    st.dataframe(df_ratios.style.format("{:.2f}"), use_container_width=True)
    
    st.markdown("### Estado de Resultados Histórico ($M)")
    st.dataframe(df_is.style.format("{:,.1f}"), use_container_width=True)
    
    st.markdown("### Balance General Histórico ($M)")
    st.dataframe(df_bs.style.format("{:,.1f}"), use_container_width=True)
    
    st.download_button(
        label="📥 Descargar Indicadores en Formato CSV",
        data=df_ratios.to_csv().encode('utf-8'),
        file_name='indicadores_financieros_andina.csv',
        mime='text/csv'
    )

st.markdown("---")
st.caption("Dashboard de Análisis Financiero desarrollado para Distribuciones Andina Comercial S.A.S. • Powered by Streamlit & Plotly")
