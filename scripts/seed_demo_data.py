
import json
import sqlite3
from contextlib import closing

from datetime import datetime, timedelta, timezone
from pathlib import Path
from src.database import criar_tabela


# Caminho do banco de dados
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "smartops.db"

# Identificador para reconhecer os registros fictícios
MARCADOR_DEMO = "DEMO FICTÍCIO | "


def inserir_dados_demo():
    """Insere incidentes fictícios para demonstração do dashboard."""

    criar_tabela()

    agora = datetime.now(timezone.utc)

    # Incidentes distribuídos pelas últimas cinco horas
    incidentes_recentes = [
        {
            "descricao": MARCADOR_DEMO + "Falha de comunicação entre servidores.",
            "categoria": "Infraestrutura",
            "prioridade": "Crítica",
            "impacto": "Serviços internos indisponíveis.",
            "causas": ["Falha no servidor", "Serviço interrompido"],
            "recomendacoes": ["Verificar os serviços", "Analisar os logs"],
            "minutos": 277,
        },
        {
            "descricao": MARCADOR_DEMO + "Consultas ao banco de dados apresentam lentidão.",
            "categoria": "Banco de dados",
            "prioridade": "Alta",
            "impacto": "Atraso no processamento de informações.",
            "causas": ["Consultas não otimizadas", "Alto volume de acessos"],
            "recomendacoes": ["Analisar consultas", "Verificar índices"],
            "minutos": 225,
        },
        {
            "descricao": MARCADOR_DEMO + "Instabilidade na conexão de rede.",
            "categoria": "Rede",
            "prioridade": "Média",
            "impacto": "Intermitência no acesso aos sistemas.",
            "causas": ["Perda de pacotes", "Instabilidade no equipamento"],
            "recomendacoes": ["Verificar conectividade", "Analisar equipamentos"],
            "minutos": 170,
        },
        {
            "descricao": MARCADOR_DEMO + "Aplicação apresenta erro ao realizar login.",
            "categoria": "Aplicação",
            "prioridade": "Alta",
            "impacto": "Usuários não conseguem acessar o sistema.",
            "causas": ["Erro na autenticação", "Falha na aplicação"],
            "recomendacoes": ["Analisar logs", "Testar autenticação"],
            "minutos": 110,
        },
        {
            "descricao": MARCADOR_DEMO + "Tentativas suspeitas de acesso ao sistema.",
            "categoria": "Segurança",
            "prioridade": "Crítica",
            "impacto": "Possível comprometimento de contas.",
            "causas": ["Tentativas de acesso indevido"],
            "recomendacoes": ["Verificar logs de acesso", "Revisar permissões"],
            "minutos": 55,
        },
        {
            "descricao": MARCADOR_DEMO + "Estação de trabalho não inicializa.",
            "categoria": "Hardware",
            "prioridade": "Baixa",
            "impacto": "Um usuário impossibilitado de trabalhar.",
            "causas": ["Possível falha na fonte de alimentação"],
            "recomendacoes": ["Verificar componentes", "Testar alimentação"],
            "minutos": 20,
        },
        {
            "descricao": MARCADOR_DEMO + "Solicitação de configuração de novo usuário.",
            "categoria": "Outro",
            "prioridade": "Baixa",
            "impacto": "Atraso na disponibilização do acesso.",
            "causas": ["Configuração pendente"],
            "recomendacoes": ["Validar solicitação", "Realizar configuração"],
            "minutos": 3,
        },
    ]

    # Incidentes históricos distribuídos pelos últimos sete dias
    incidentes_historicos = [
        {
            "descricao": MARCADOR_DEMO + "Armazenamento do servidor próximo da capacidade máxima.",
            "categoria": "Infraestrutura",
            "prioridade": "Alta",
            "impacto": "Risco de interrupção de serviços.",
            "causas": ["Espaço insuficiente em disco"],
            "recomendacoes": ["Verificar utilização", "Planejar expansão"],
            "dias": 1,
        },
        {
            "descricao": MARCADOR_DEMO + "Erro durante atualização de registros.",
            "categoria": "Banco de dados",
            "prioridade": "Média",
            "impacto": "Registros não atualizados corretamente.",
            "causas": ["Falha na transação"],
            "recomendacoes": ["Verificar integridade", "Analisar transações"],
            "dias": 2,
        },
        {
            "descricao": MARCADOR_DEMO + "Equipamento de rede sem resposta.",
            "categoria": "Rede",
            "prioridade": "Crítica",
            "impacto": "Indisponibilidade de conexão em um setor.",
            "causas": ["Falha no equipamento"],
            "recomendacoes": ["Verificar equipamento", "Acionar suporte"],
            "dias": 3,
        },
        {
            "descricao": MARCADOR_DEMO + "Erro ao gerar relatório operacional.",
            "categoria": "Aplicação",
            "prioridade": "Baixa",
            "impacto": "Atraso na geração de relatório.",
            "causas": ["Erro no processamento"],
            "recomendacoes": ["Analisar aplicação", "Revisar parâmetros"],
            "dias": 4,
        },
        {
            "descricao": MARCADOR_DEMO + "Alerta de acesso fora do padrão.",
            "categoria": "Segurança",
            "prioridade": "Alta",
            "impacto": "Necessidade de validação de acesso.",
            "causas": ["Atividade incomum"],
            "recomendacoes": ["Auditar acesso", "Validar usuário"],
            "dias": 5,
        },
        {
            "descricao": MARCADOR_DEMO + "Periférico apresenta falha de funcionamento.",
            "categoria": "Hardware",
            "prioridade": "Média",
            "impacto": "Redução da produtividade do usuário.",
            "causas": ["Possível defeito físico"],
            "recomendacoes": ["Realizar testes", "Avaliar substituição"],
            "dias": 6,
        },
        {
            "descricao": MARCADOR_DEMO + "Solicitação de ajuste de perfil de acesso.",
            "categoria": "Outro",
            "prioridade": "Baixa",
            "impacto": "Acesso pendente a uma funcionalidade.",
            "causas": ["Perfil desatualizado"],
            "recomendacoes": ["Validar autorização", "Atualizar perfil"],
            "dias": 7,
        },
    ]

    # Prepara os registros com seus respectivos horários UTC
    registros = []

    for incidente in incidentes_recentes:
        data = agora - timedelta(minutes=incidente["minutos"])
        registros.append((incidente, data))

    for incidente in incidentes_historicos:
        data = agora - timedelta(days=incidente["dias"])
        registros.append((incidente, data))

    with closing(sqlite3.connect(DB_PATH)) as conexao:
        with conexao:
            cursor = conexao.cursor()

            # Impede a inserção duplicada dos dados de demonstração
            cursor.execute(
                "SELECT COUNT(*) FROM incidentes WHERE descricao LIKE ?",
                (MARCADOR_DEMO + "%",)
            )

            if cursor.fetchone()[0] > 0:
                print("Os dados de demonstração já foram inseridos.")
                return

            for incidente, data in registros:
                cursor.execute(
                    """
                    INSERT INTO incidentes (
                        descricao,
                        categoria,
                        prioridade,
                        impacto,
                        causas,
                        recomendacoes,
                        data_criacao
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        incidente["descricao"],
                        incidente["categoria"],
                        incidente["prioridade"],
                        incidente["impacto"],
                        json.dumps(incidente["causas"], ensure_ascii=False),
                        json.dumps(incidente["recomendacoes"], ensure_ascii=False),
                        data.strftime("%Y-%m-%d %H:%M:%S"),
                    )
                )

    print(f"{len(registros)} incidentes fictícios inseridos com sucesso!")


if __name__ == "__main__":
    inserir_dados_demo()
