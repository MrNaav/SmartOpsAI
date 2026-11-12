
import streamlit as st
import pandas as pd

from io import BytesIO

from src.ai_service import analisar_incidente

from src.database import (
    criar_tabela,
    salvar_incidente,
    listar_incidentes_dataframe
)


# Configuração da página
st.set_page_config(
    page_title="SmartOps AI",
    page_icon="🤖",
    layout="wide"
)


# Inicializa o banco de dados
criar_tabela()


# Cabeçalho
st.title("🤖 SmartOps AI")
st.subheader("Assistente Inteligente para Operações de TI")

st.markdown("""
Bem-vindo ao SmartOps AI!

Uma ferramenta de inteligência artificial para auxiliar
na análise, classificação e acompanhamento de incidentes de TI.
""")


# Área de registro de incidentes
st.divider()

st.header("📋 Análise de incidentes")

descricao = st.text_area(
    "Descreva o incidente de TI:",
    placeholder="Ex.: Servidor de aplicação apresenta lentidão..."
)


# Guarda o resultado da análise durante as atualizações da página
if "analise_atual" not in st.session_state:
    st.session_state.analise_atual = None

if "descricao_analisada" not in st.session_state:
    st.session_state.descricao_analisada = ""

if "analise_salva" not in st.session_state:
    st.session_state.analise_salva = False


# Botão para analisar o incidente
if st.button("Analisar incidente"):

    if descricao.strip():

        try:
            with st.spinner("A inteligência artificial está analisando o incidente..."):

                resultado = analisar_incidente(descricao.strip())

                st.session_state.analise_atual = resultado
                st.session_state.descricao_analisada = descricao.strip()
                st.session_state.analise_salva = False

        except Exception as erro:
            st.error(f"Erro ao analisar incidente: {erro}")

    else:
        st.warning("Informe uma descrição antes de continuar.")


# Exibe o resultado da análise
if (
    st.session_state.analise_atual is not None
    and st.session_state.descricao_analisada == descricao.strip()
):

    resultado = st.session_state.analise_atual

    st.subheader("Resultado da análise")

    st.write("**Categoria:**", resultado["categoria"])
    st.write("**Prioridade:**", resultado["prioridade"])
    st.write("**Impacto:**", resultado["impacto"])

    st.write("**Possíveis causas:**")

    for causa in resultado["causas"]:
        st.write(f"- {causa}")

    st.write("**Recomendações:**")

    for recomendacao in resultado["recomendacoes"]:
        st.write(f"- {recomendacao}")


    # Área de salvamento
    st.divider()

    if not st.session_state.analise_salva:

        if st.button("💾 Salvar incidente"):

            try:
                incidente_id = salvar_incidente(
                    descricao=st.session_state.descricao_analisada,
                    categoria=resultado["categoria"],
                    prioridade=resultado["prioridade"],
                    impacto=resultado["impacto"],
                    causas=resultado["causas"],
                    recomendacoes=resultado["recomendacoes"]
                )

                st.session_state.analise_salva = True

                st.success(
                    f"Incidente salvo com sucesso! ID: {incidente_id}"
                )

            except Exception as erro:
                st.error(f"Erro ao salvar incidente: {erro}")

    else:
        st.success("Este incidente já foi salvo.")


# Consulta os incidentes registrados no banco de dados
df = listar_incidentes_dataframe()


# Dashboard de indicadores operacionais
st.divider()

st.header("📊 Dashboard de operações")

if not df.empty:

    # Indicadores gerais
    total_incidentes = len(df)

    incidentes_criticos = (
        df["prioridade"] == "Crítica"
    ).sum()

    incidentes_altos = (
        df["prioridade"] == "Alta"
    ).sum()


    # Exibição dos indicadores
    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total de incidentes",
        total_incidentes
    )

    col2.metric(
        "Prioridade crítica",
        incidentes_criticos
    )

    col3.metric(
        "Prioridade alta",
        incidentes_altos
    )


    # Gráficos operacionais
    st.divider()

    col_grafico1, col_grafico2 = st.columns(2)

    with col_grafico1:

        st.subheader("Incidentes por categoria")

        incidentes_categoria = (
            df["categoria"]
            .fillna("Não classificado")
            .value_counts()
        )

        st.bar_chart(incidentes_categoria)


    with col_grafico2:

        st.subheader("Incidentes por prioridade")

        incidentes_prioridade = (
            df["prioridade"]
            .fillna("Não classificada")
            .value_counts()
        )

        st.bar_chart(incidentes_prioridade)


    # Evolução temporal dos incidentes
    st.divider()

    st.subheader("Evolução de incidentes por dia")

    # Cria uma cópia para preservar o DataFrame original
    df_temporal = df.copy()

    # Converte a coluna para o formato de data
    df_temporal["data_criacao"] = pd.to_datetime(
        df_temporal["data_criacao"],
        errors="coerce"
    )

    # Agrupa os incidentes por dia
    incidentes_por_dia = (
        df_temporal
        .dropna(subset=["data_criacao"])
        .groupby(df_temporal["data_criacao"].dt.date)
        .size()
        .sort_index()
    )

    # Exibe o gráfico
    st.line_chart(incidentes_por_dia)


else:
    st.info("Ainda não existem incidentes para gerar indicadores.")


# Histórico de incidentes
st.divider()

st.header("📚 Histórico de incidentes")

if not df.empty:

    # Filtros do histórico
    col_filtro1, col_filtro2 = st.columns(2)

    # Filtro por prioridade
    with col_filtro1:

        prioridades = ["Todas"] + sorted(
            df["prioridade"].dropna().unique().tolist()
        )

        prioridade_selecionada = st.selectbox(
            "Filtrar por prioridade:",
            prioridades
        )

    # Filtro por categoria
    with col_filtro2:

        categorias = ["Todas"] + sorted(
            df["categoria"].dropna().unique().tolist()
        )

        categoria_selecionada = st.selectbox(
            "Filtrar por categoria:",
            categorias
        )

    # Cria uma cópia dos registros
    df_filtrado = df.copy()

    # Aplica o filtro de prioridade
    if prioridade_selecionada != "Todas":

        df_filtrado = df_filtrado[
            df_filtrado["prioridade"] == prioridade_selecionada
        ]

    # Aplica o filtro de categoria
    if categoria_selecionada != "Todas":

        df_filtrado = df_filtrado[
            df_filtrado["categoria"] == categoria_selecionada
        ]

    # Quantidade de registros encontrados
    st.write(
        f"Incidentes encontrados: {len(df_filtrado)}"
    )

    # Exibe o histórico filtrado
    st.dataframe(
        df_filtrado,
        width="stretch",
        hide_index=True
    )


    # Exportação dos incidentes para Excel
    if not df_filtrado.empty:

        arquivo_excel = BytesIO()

        with pd.ExcelWriter(
            arquivo_excel,
            engine="openpyxl"
        ) as escritor:

            df_filtrado.to_excel(
                escritor,
                index=False,
                sheet_name="Incidentes"
            )

        st.download_button(
            label="📥 Exportar para Excel",
            data=arquivo_excel.getvalue(),
            file_name="relatorio_incidentes.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )


else:
    st.info("Nenhum incidente registrado até o momento.")
