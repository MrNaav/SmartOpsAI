# SmartOps AI

**Análise inteligente de incidentes de TI com Inteligência Artificial**

O SmartOps AI é uma aplicação desenvolvida em Python e Streamlit que utiliza Inteligência Artificial para auxiliar na análise e classificação de incidentes de Tecnologia da Informação.

A solução transforma descrições de problemas em análises estruturadas, identificando categorias, prioridades, impactos operacionais, possíveis causas técnicas e recomendações para investigação e resolução.

O projeto busca demonstrar como a Inteligência Artificial pode apoiar equipes de operações de TI na interpretação de incidentes, organização de informações e tomada de decisão.

## Funcionalidades

- **Análise inteligente:** utiliza a API Google Gemini para interpretar descrições de incidentes.
- **Classificação automática:** identifica a categoria e a prioridade do incidente.
- **Análise de impacto:** apresenta possíveis consequências operacionais.
- **Investigação técnica:** sugere possíveis causas e recomendações para resolução.
- **Histórico de incidentes:** armazena e permite consultar análises anteriores.
- **Dashboard operacional:** apresenta indicadores e gráficos para acompanhamento dos incidentes.
- **Filtros temporais:** permite visualizar dados conforme diferentes intervalos de tempo.
- **Filtros por categoria e prioridade:** facilita a consulta e a organização dos registros.
- **Exportação para Excel:** gera relatórios com os incidentes filtrados.
- **Lixeira de incidentes:** permite excluir registros sem removê-los imediatamente do sistema.
- **Restauração:** possibilita recuperar incidentes enviados à lixeira.
- **Exclusão definitiva:** permite remover permanentemente registros da lixeira.
- **Dados demonstrativos:** disponibiliza um script para gerar incidentes fictícios para testes.

## Tecnologias utilizadas

| Tecnologia | Aplicação |
|---|---|
| Python | Linguagem principal |
| Streamlit | Desenvolvimento da interface web |
| Google Gemini API | Análise inteligente dos incidentes |
| SQLite | Armazenamento local dos registros |
| Pandas | Manipulação e análise dos dados |
| OpenPyXL | Exportação de relatórios para Excel |
| Python-dotenv | Gerenciamento de variáveis de ambiente |
| Git | Controle de versão |

## Estrutura do projeto

```text
SmartOpsAI/
│
├── data/
│   └── smartops.db
│
├── scripts/
│   └── seed_demo_data.py
│
├── src/
│   ├── ai_service.py
│   └── database.py
│
├── .env.example
├── .gitignore
├── app.py
├── requirements.txt
└── README.md
```

### Principais arquivos e diretórios

- `app.py`: aplicação principal, interface e funcionalidades do sistema.
- `src/ai_service.py`: integração com a API Google Gemini e processamento das análises.
- `src/database.py`: criação das tabelas, armazenamento, consulta, restauração e exclusão dos registros no SQLite.
- `scripts/seed_demo_data.py`: geração de incidentes fictícios para demonstração e testes.
- `data/`: diretório utilizado para armazenar o banco de dados local.
- `.env.example`: modelo das variáveis de ambiente necessárias.
- `.gitignore`: define os arquivos e diretórios que não devem ser publicados no GitHub.
- `requirements.txt`: lista as dependências do projeto.

## Como executar o projeto

### 1. Pré-requisitos

- Python 3.13 ou compatível.
- Uma chave de API do Google Gemini.
- Git.

### 2. Clonar o repositório

```bash
git clone https://github.com/MrNaav/SmartOpsAI.git
cd SmartOpsAI
```

### 3. Criar um ambiente virtual

```bash
python -m venv .venv
```

Ativar no Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 5. Configurar a API Gemini

Crie um arquivo `.env` na raiz do projeto e configure sua chave:

```env
GEMINI_API_KEY=sua_chave_aqui
```

A chave pode ser obtida no [Google AI Studio](https://aistudio.google.com/).

**Importante:** nunca compartilhe ou publique sua chave de API. O arquivo `.env` está protegido pelo `.gitignore`.

### 6. Executar a aplicação

```bash
streamlit run app.py
```

A aplicação será disponibilizada localmente, normalmente em:

http://localhost:8501

## Dados demonstrativos

O projeto disponibiliza um script para popular o banco de dados com incidentes fictícios:

```bash
python scripts/seed_demo_data.py
```

Esses registros permitem testar o histórico, os filtros, os indicadores e os gráficos do dashboard sem depender de incidentes reais.

## Dados e segurança

Os incidentes utilizados para demonstração são fictícios. Nenhum dado confidencial ou informação operacional interna de empresas é utilizado nos dados demonstrativos.

As descrições enviadas para análise são encaminhadas à API do Google Gemini. Portanto, não devem ser inseridas informações confidenciais, credenciais ou dados sensíveis.

O banco de dados SQLite é armazenado localmente no ambiente de execução.

## Objetivo do projeto

O SmartOps AI foi desenvolvido como projeto prático para aplicar conhecimentos de desenvolvimento Python, integração com serviços de Inteligência Artificial, persistência de dados, manipulação de informações e construção de indicadores operacionais.

A proposta é demonstrar como a IA pode apoiar processos de operações de TI, contribuindo para a análise de incidentes, identificação de possíveis causas, organização de informações e apoio à tomada de decisão.

---

**Status:** Projeto em desenvolvimento.