import streamlit as st
import pandas as pd
import plotly.express as px

# ==============================
# 📂 Carregar dados
# ==============================
df = pd.read_csv("data.csv")

st.set_page_config(page_title="Dashboard de Funcionários", layout="wide")

# ==============================
# 🎯 Título
# ==============================
st.title("📊 Dashboard de Funcionários")

# ==============================
# 🔍 Filtros
# ==============================
departamentos = df["departamento"].unique()
cidades = df["cidade"].unique()

col1, col2 = st.columns(2)

with col1:
    filtro_departamento = st.multiselect("Filtrar por Departamento", options=departamentos, default=departamentos)

with col2:
    filtro_cidade = st.multiselect("Filtrar por Cidade", options=cidades, default=cidades)

# Aplicar filtros
df_filtrado = df[(df["departamento"].isin(filtro_departamento)) & (df["cidade"].isin(filtro_cidade))]

# ==============================
# 📋 Estatísticas
# ==============================
st.subheader("📌 Estatísticas Gerais")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("👥 Total Funcionários", len(df_filtrado))

with col2:
    st.metric("💰 Salário Médio", f"R$ {df_filtrado['salario'].mean():,.2f}")

with col3:
    st.metric("🎂 Idade Média", round(df_filtrado['idade'].mean(), 1))

# ==============================
# 📊 Gráficos
# ==============================
st.subheader("📈 Análises")

col1, col2 = st.columns(2)

# Salário médio por departamento
with col1:
    fig1 = px.bar(df_filtrado.groupby("departamento")["salario"].mean().reset_index(),
                  x="departamento", y="salario", color="departamento",
                  title="💰 Salário Médio por Departamento")
    st.plotly_chart(fig1, use_container_width=True)

# Distribuição de idades
with col2:
    fig2 = px.histogram(df_filtrado, x="idade", nbins=10,
                        title="🎂 Distribuição de Idades")
    st.plotly_chart(fig2, use_container_width=True)

# Funcionários por cidade
# Contagem de funcionários por cidade
cidades_count = df_filtrado["cidade"].value_counts().reset_index().head(10)
cidades_count.columns = ["cidade", "count"]  # renomear colunas

fig3 = px.bar(cidades_count,
              x="cidade", y="count", title="🌍 Top 10 Cidades com Mais Funcionários")
fig3.update_layout(xaxis_title="Cidade", yaxis_title="Qtd Funcionários")
st.plotly_chart(fig3, use_container_width=True)


# ==============================
# 📋 Tabela de dados
# ==============================
st.subheader("📋 Dados Filtrados")
st.dataframe(df_filtrado)
