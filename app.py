
import streamlit as st
import pandas as pd

from io import BytesIO
from zoneinfo import ZoneInfo

from src.ai_service import analisar_incidente

from src.database import (
    criar_tabela,
    salvar_incidente,
    listar_incidentes_dataframe,
    excluir_incidente,
    listar_incidentes_excluidos,
    restaurar_incidente,
    excluir_incidente_definitivamente
)

FUSO_BRASILIA = ZoneInfo("America/Sao_Paulo")


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

        # Limpa a análise anterior antes de iniciar uma nova
        st.session_state.analise_atual = None
        st.session_state.descricao_analisada = ""
        st.session_state.analise_salva = False

        try:
            with st.spinner("A inteligência artificial está analisando o incidente..."):

                resultado = analisar_incidente(descricao.strip())

                st.session_state.analise_atual = resultado
                st.session_state.descricao_analisada = descricao.strip()
                st.session_state.analise_salva = False

        except ValueError as erro:
            st.error(str(erro))

        except Exception:
            st.error(
                "Não foi possível realizar a análise. "
                "Verifique sua conexão, a chave da API e o limite de requisições."
            )

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
                    categoria=st.session_state.analise_atual["categoria"],
                    prioridade=st.session_state.analise_atual["prioridade"],
                    impacto=st.session_state.analise_atual["impacto"],
                    causas=st.session_state.analise_atual["causas"],
                    recomendacoes=st.session_state.analise_atual["recomendacoes"]
                )

                st.session_state.analise_salva = True

                st.success(
                    f"Incidente salvo com sucesso! ID: {incidente_id}"
                )

            except Exception:
                st.error(
                    "Não foi possível salvar o incidente. "
                    "Verifique a conexão com o banco de dados."
                )

    else:
        st.success("Este incidente já foi salvo.")


# Consulta os incidentes registrados no banco de dados
df = listar_incidentes_dataframe()


# Converte os horários armazenados em UTC para Brasília
if not df.empty:
    df["data_criacao"] = (
        pd.to_datetime(df["data_criacao"], errors="coerce", utc=True)
        .dt.tz_convert(FUSO_BRASILIA)
    )


# Dashboard de indicadores operacionais
st.divider()

st.header("📊 Dashboard de operações")


if not df.empty:

    # Opções de períodos para análise
    periodos = {
        "Últimos 5 minutos": pd.Timedelta(minutes=5),
        "Últimos 10 minutos": pd.Timedelta(minutes=10),
        "Últimos 30 minutos": pd.Timedelta(minutes=30),
        "Última 1 hora": pd.Timedelta(hours=1),
        "Últimas 2 horas": pd.Timedelta(hours=2),
        "Últimas 5 horas": pd.Timedelta(hours=5),
        "Evolução diária": None
    }

    # Seletor de período
    periodo_selecionado = st.selectbox(
        "📅 Período de análise:",
        list(periodos.keys())
    )


    # Cria uma cópia dos incidentes para o dashboard
    df_dashboard = df.copy()

    # Obtém a duração do período selecionado
    duracao = periodos[periodo_selecionado]


    # Aplica o filtro temporal
    if duracao is not None:

        agora = pd.Timestamp.now(tz=FUSO_BRASILIA)
        inicio = agora - duracao

        df_dashboard = df_dashboard[
            df_dashboard["data_criacao"] >= inicio
        ]


    # Verifica se existem incidentes no período
    if not df_dashboard.empty:

        # Indicadores gerais
        total_incidentes = len(df_dashboard)

        incidentes_criticos = (
            df_dashboard["prioridade"] == "Crítica"
        ).sum()

        incidentes_altos = (
            df_dashboard["prioridade"] == "Alta"
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


        # Incidentes por categoria
        with col_grafico1:

            st.subheader("Incidentes por categoria")

            incidentes_categoria = (
                df_dashboard["categoria"]
                .fillna("Não classificado")
                .value_counts()
            )

            st.bar_chart(incidentes_categoria)


        # Incidentes por prioridade
        with col_grafico2:

            st.subheader("Incidentes por prioridade")

            incidentes_prioridade = (
                df_dashboard["prioridade"]
                .fillna("Não classificada")
                .value_counts()
            )

            st.bar_chart(incidentes_prioridade)


        # Evolução temporal dos incidentes
        st.divider()

        st.subheader("Evolução temporal dos incidentes")

        # Define o intervalo de agrupamento conforme o período selecionado
        frequencias_grafico = {
            "Últimos 5 minutos": "1min",
            "Últimos 10 minutos": "2min",
            "Últimos 30 minutos": "5min",
            "Última 1 hora": "10min",
            "Últimas 2 horas": "15min",
            "Últimas 5 horas": "30min",
            "Evolução diária": "D"
        }

        frequencia = frequencias_grafico[periodo_selecionado]

        # Cria uma cópia para preservar o DataFrame original
        df_temporal = (
            df_dashboard
            .dropna(subset=["data_criacao"])
            .copy()
        )

        if not df_temporal.empty:

            # Agrupa os incidentes conforme a frequência selecionada
            incidentes_por_intervalo = (
                df_temporal
                .set_index("data_criacao")
                .resample(frequencia)
                .size()
                .reset_index(name="Quantidade")
            )

            # Formata as datas para facilitar a leitura
            if duracao is None:
                incidentes_por_intervalo["Data"] = (
                    incidentes_por_intervalo["data_criacao"]
                    .dt.strftime("%d/%m/%Y")
                )
            else:
                incidentes_por_intervalo["Data"] = (
                    incidentes_por_intervalo["data_criacao"]
                    .dt.strftime("%d/%m %H:%M")
                )

            # Exibe o gráfico
            st.line_chart(
                incidentes_por_intervalo,
                x="Data",
                y="Quantidade"
            )

        else:
            st.info("Não existem dados temporais para exibir.")


    else:
        st.info("Não existem incidentes registrados no período selecionado.")


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


    # Cria uma cópia para exibição
    df_exibicao = df_filtrado.copy()

    # Remove a informação do fuso, mantendo o horário de Brasília
    df_exibicao["data_criacao"] = (
        df_exibicao["data_criacao"].dt.tz_localize(None)
    )


    # Exibe o histórico filtrado
    st.dataframe(
        df_exibicao,
        width="stretch",
        hide_index=True
    )


    # Área de exclusão de incidentes
    if not df_filtrado.empty:

        st.divider()

        st.subheader("🗑️ Excluir incidente")

        # Lista os IDs disponíveis no histórico filtrado
        incidentes_disponiveis = df_filtrado["id"].tolist()

        incidente_selecionado = st.selectbox(
            "Selecione o incidente que deseja excluir:",
            incidentes_disponiveis,
            format_func=lambda incidente_id: (
                f"ID {incidente_id} - "
                f"{df_filtrado.loc[df_filtrado['id'] == incidente_id, 'descricao'].iloc[0][:60]}"
            )
        )

        # Solicita confirmação antes da exclusão
        if st.button("Excluir incidente selecionado"):
            st.session_state["incidente_para_excluir"] = incidente_selecionado

        # Exibe a confirmação
        incidente_confirmacao = st.session_state.get(
            "incidente_para_excluir"
        )

        if incidente_confirmacao is not None:

            st.warning(
                f"Tem certeza de que deseja excluir o incidente "
                f"ID {incidente_confirmacao}? Ele será enviado para a lixeira."
            )

            col_confirmar, col_cancelar = st.columns(2)

            with col_confirmar:

                if st.button("Sim, excluir", type="primary"):
                    try:
                        excluido = excluir_incidente(incidente_confirmacao)

                        if excluido:
                            st.session_state["mensagem_exclusao"] = (
                                f"Incidente ID {incidente_confirmacao} enviado para a lixeira."
                            )
                        else:
                            st.session_state["mensagem_exclusao"] = (
                                "O incidente não foi encontrado."
                            )

                        st.session_state.pop("incidente_para_excluir", None)
                        st.rerun()

                    except Exception:
                        st.error("Não foi possível excluir o incidente.")

            with col_cancelar:

                if st.button("Cancelar"):
                    st.session_state.pop("incidente_para_excluir", None)
                    st.rerun()

        # Exibe o resultado da última exclusão
        mensagem_exclusao = st.session_state.pop(
            "mensagem_exclusao",
            None
        )

        if mensagem_exclusao:
            st.success(mensagem_exclusao)


    # Exportação dos incidentes para Excel
    if not df_filtrado.empty:

        # Cria uma cópia para preservar o histórico original
        df_excel = df_filtrado.copy()

        # Remove a informação do fuso, mantendo o horário de Brasília
        df_excel["data_criacao"] = (
            df_excel["data_criacao"].dt.tz_localize(None)
        )

        arquivo_excel = BytesIO()

        with pd.ExcelWriter(
            arquivo_excel,
            engine="openpyxl"
        ) as escritor:

            df_excel.to_excel(
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




# ==========================================
# LIXEIRA DE INCIDENTES
# ==========================================

st.divider()

st.header("🗑️ Lixeira de incidentes")

df_excluidos = listar_incidentes_excluidos()

if not df_excluidos.empty:

    # Converte os horários armazenados em UTC para Brasília
    for coluna in ["data_criacao", "data_exclusao"]:

        df_excluidos[coluna] = (
            pd.to_datetime(
                df_excluidos[coluna],
                errors="coerce",
                utc=True
            )
            .dt.tz_convert(FUSO_BRASILIA)
            .dt.tz_localize(None)
        )

    # Exibe os incidentes excluídos
    st.dataframe(
        df_excluidos,
        width="stretch",
        hide_index=True
    )

    st.caption(
        f"Total de incidentes na lixeira: {len(df_excluidos)}"
    )

    incidentes_excluidos = df_excluidos["id"].tolist()

    # ==========================================
    # RESTAURAR INCIDENTE
    # ==========================================

    st.divider()

    st.subheader("♻️ Restaurar incidente")

    incidente_selecionado_restauracao = st.selectbox(
        "Selecione o incidente que deseja restaurar:",
        incidentes_excluidos,
        format_func=lambda incidente_id: (
            f"ID {incidente_id} - "
            f"{df_excluidos.loc[df_excluidos['id'] == incidente_id, 'descricao'].iloc[0][:60]}"
        ),
        key="selecao_restauracao"
    )

    if st.button("Restaurar incidente selecionado"):

        st.session_state["incidente_para_restaurar"] = (
            incidente_selecionado_restauracao
        )

    incidente_confirmacao_restauracao = st.session_state.get(
        "incidente_para_restaurar"
    )

    if incidente_confirmacao_restauracao is not None:

        st.warning(
            f"Deseja restaurar o incidente ID "
            f"{incidente_confirmacao_restauracao}?"
        )

        col_restaurar, col_cancelar_restauracao = st.columns(2)

        with col_restaurar:

            if st.button("Sim, restaurar", type="primary"):

                try:
                    restaurado = restaurar_incidente(
                        incidente_confirmacao_restauracao
                    )

                    if restaurado:
                        st.session_state["mensagem_restauracao"] = (
                            f"Incidente ID {incidente_confirmacao_restauracao} "
                            "restaurado com sucesso!"
                        )
                    else:
                        st.session_state["mensagem_restauracao"] = (
                            "O incidente não foi encontrado na lixeira."
                        )

                    st.session_state.pop("incidente_para_restaurar", None)
                    st.rerun()

                except Exception:
                    st.error(
                        "Não foi possível restaurar o incidente. "
                        "Verifique se ele já existe no histórico."
                    )

        with col_cancelar_restauracao:

            if st.button("Cancelar restauração"):
                st.session_state.pop("incidente_para_restaurar", None)
                st.rerun()

    # ==========================================
    # EXCLUSÃO DEFINITIVA
    # ==========================================

    st.divider()

    st.subheader("❌ Excluir permanentemente")

    incidente_selecionado_exclusao = st.selectbox(
        "Selecione o incidente que deseja apagar definitivamente:",
        incidentes_excluidos,
        format_func=lambda incidente_id: (
            f"ID {incidente_id} - "
            f"{df_excluidos.loc[df_excluidos['id'] == incidente_id, 'descricao'].iloc[0][:60]}"
        ),
        key="selecao_exclusao_definitiva"
    )

    if st.button("Excluir definitivamente"):

        st.session_state["incidente_para_excluir_definitivamente"] = (
            incidente_selecionado_exclusao
        )

    incidente_confirmacao_exclusao = st.session_state.get(
        "incidente_para_excluir_definitivamente"
    )

    if incidente_confirmacao_exclusao is not None:

        st.error(
            f"ATENÇÃO: o incidente ID {incidente_confirmacao_exclusao} "
            "será removido permanentemente. Essa ação não poderá ser desfeita."
        )

        col_excluir, col_cancelar_exclusao = st.columns(2)

        with col_excluir:

            if st.button("Sim, apagar permanentemente", type="primary"):

                try:
                    excluido = excluir_incidente_definitivamente(
                        incidente_confirmacao_exclusao
                    )

                    if excluido:
                        st.session_state["mensagem_exclusao_definitiva"] = (
                            f"Incidente ID {incidente_confirmacao_exclusao} "
                            "excluído permanentemente."
                        )
                    else:
                        st.session_state["mensagem_exclusao_definitiva"] = (
                            "O incidente não foi encontrado na lixeira."
                        )

                    st.session_state.pop(
                        "incidente_para_excluir_definitivamente", None
                    )

                    st.rerun()

                except Exception:
                    st.error(
                        "Não foi possível excluir definitivamente o incidente."
                    )

        with col_cancelar_exclusao:

            if st.button("Cancelar exclusão definitiva"):
                st.session_state.pop(
                    "incidente_para_excluir_definitivamente", None
                )
                st.rerun()

else:

    st.info("Nenhum incidente excluído.")


# Exibe o resultado da última restauração
mensagem_restauracao = st.session_state.pop(
    "mensagem_restauracao",
    None
)

if mensagem_restauracao:
    st.success(mensagem_restauracao)


# Exibe o resultado da última exclusão definitiva
mensagem_exclusao_definitiva = st.session_state.pop(
    "mensagem_exclusao_definitiva",
    None
)

if mensagem_exclusao_definitiva:
    st.success(mensagem_exclusao_definitiva)
