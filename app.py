import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Cargar datos y filtros
@st.cache_data
def load_data():
    df_datos = pd.read_excel("DOR OPERACIONAL.xlsx", sheet_name="DOR OPERACIONAL")
    df_filtros = pd.read_excel("DOR OPERACIONAL.xlsx", sheet_name="FILTROS DASHBOARD")
    df_datos["FECHA"] = pd.to_datetime(df_datos["FECHA"])
    return df_datos, df_filtros

df, filtros = load_data()

# Leer los filtros desde la hoja FILTROS DASHBOARD
fecha_inicio = pd.to_datetime(filtros.loc[0, "DESDE"])
fecha_fin = pd.to_datetime(filtros.loc[0, "HASTA"])
responsable = filtros.loc[0, "RESPONSABLE"]

# Filtrar datos
df_filtrado = df[(df["FECHA"] >= fecha_inicio) & (df["FECHA"] <= fecha_fin)]
df_filtrado = df_filtrado[df_filtrado["RESPONSABLE"].str.lower() == responsable.lower()]

st.title("Dashboard SVG - FEPASA")

# Función para gráfico SVG de indicador
def plot_indicator_vs_responsable(df, indicador, titulo):
    agg = df.groupby("RESPONSABLE")[indicador].mean().reset_index()
    agg = agg.sort_values(by=indicador)

    fig, ax = plt.subplots(figsize=(6, 3))
    bars = ax.barh(agg["RESPONSABLE"], agg[indicador])

    for bar, val in zip(bars, agg[indicador]):
        color = "green" if val == 100 else "red"
        bar.set_color(color)
        ax.text(val - 5 if val > 10 else val + 2, bar.get_y() + bar.get_height()/2, f"{val:.0f}%", va='center', ha='right' if val > 10 else 'left', color="white" if val > 10 else "black")

    ax.set_xlim(0, 100)
    ax.set_xlabel("% Cumplimiento")
    ax.set_title(titulo)
    st.pyplot(fig)

# Mostrar gráficos
plot_indicator_vs_responsable(df_filtrado, "CARROS IND%", "Indicador Carros vs Responsable")
plot_indicator_vs_responsable(df_filtrado, "LLEG IND%", "Indicador Llegada vs Responsable")
plot_indicator_vs_responsable(df_filtrado, "SALIDA IND%", "Indicador Salida vs Responsable")
