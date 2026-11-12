
import sqlite3
import json
from pathlib import Path

import pandas as pd

# Caminho da pasta principal do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Caminho do banco de dados
DB_PATH = BASE_DIR / "data" / "smartops.db"


def criar_tabela():
    """Cria o banco de dados e a tabela de incidentes, caso não existam."""

    # Garante que a pasta data exista
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Conecta ao banco de dados
    conexao = sqlite3.connect(DB_PATH)

    cursor = conexao.cursor()

    # Cria a tabela de incidentes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS incidentes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT NOT NULL,
            categoria TEXT,
            prioridade TEXT,
            impacto TEXT,
            causas TEXT,
            recomendacoes TEXT,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conexao.commit()
    conexao.close()



def salvar_incidente(descricao, categoria=None, prioridade=None,
                     impacto=None, causas=None, recomendacoes=None):
    """Salva um incidente no banco de dados."""

    conexao = sqlite3.connect(DB_PATH)
    cursor = conexao.cursor()

    # Converte listas em JSON para armazenamento no SQLite
    causas_json = json.dumps(causas, ensure_ascii=False) if causas else None
    recomendacoes_json = json.dumps(recomendacoes, ensure_ascii=False) if recomendacoes else None

    cursor.execute("""
        INSERT INTO incidentes (
            descricao,
            categoria,
            prioridade,
            impacto,
            causas,
            recomendacoes
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        descricao,
        categoria,
        prioridade,
        impacto,
        causas_json,
        recomendacoes_json
    ))

    conexao.commit()

    incidente_id = cursor.lastrowid

    conexao.close()

    return incidente_id


def listar_incidentes():
    """Retorna todos os incidentes cadastrados, do mais recente ao mais antigo."""

    conexao = sqlite3.connect(DB_PATH)

    cursor = conexao.cursor()

    cursor.execute("""
        SELECT *
        FROM incidentes
        ORDER BY data_criacao DESC, id DESC
    """)

    incidentes = cursor.fetchall()

    conexao.close()

    return incidentes


def listar_incidentes_dataframe():
    """Retorna os incidentes em formato de DataFrame."""

    conexao = sqlite3.connect(DB_PATH)

    consulta = """
        SELECT *
        FROM incidentes
        ORDER BY data_criacao DESC, id DESC
    """

    df = pd.read_sql_query(consulta, conexao)

    conexao.close()

    return df
