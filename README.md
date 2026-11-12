# SmartOps AI

**Análise inteligente de incidentes de TI com Inteligência Artificial**

O SmartOps AI é uma aplicação desenvolvida em Python e Streamlit que utiliza Inteligência Artificial para auxiliar na análise e classificação de incidentes de Tecnologia da Informação.

A solução transforma descrições de problemas em análises estruturadas, identificando categorias, prioridades, impactos operacionais, possíveis causas técnicas e recomendações para investigação e resolução.

## Funcionalidades

- **Análise inteligente:** utiliza a API Google Gemini para interpretar descrições de incidentes.
- **Classificação automática:** identifica a categoria e a prioridade do incidente.
- **Análise de impacto:** apresenta possíveis consequências operacionais.
- **Investigação técnica:** sugere possíveis causas e ações para resolução.
- **Histórico de incidentes:** armazena e permite consultar análises anteriores.
- **Dashboard operacional:** apresenta indicadores e gráficos de acompanhamento.
- **Filtros:** permite consultar incidentes por categoria e prioridade.
- **Exportação para Excel:** gera relatórios com os registros filtrados.

## Tecnologias utilizadas

| Tecnologia | Aplicação |
|---|---|
| Python | Linguagem principal |
| Streamlit | Interface web |
| Google Gemini API | Análise inteligente dos incidentes |
| SQLite | Armazenamento dos registros |
| Pandas | Manipulação e análise dos dados |
| OpenPyXL | Exportação para Excel |
| Python-dotenv | Gerenciamento de variáveis de ambiente |
| Git | Controle de versão |

## Estrutura do projeto

```text
SmartOpsAI/
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

### Principais arquivos

- `app.py`: aplicação principal e interface do sistema.
- `src/ai_service.py`: integração com a API Google Gemini e análise dos incidentes.
- `src/database.py`: criação, armazenamento e consulta dos registros no SQLite.
- `data/`: diretório utilizado para armazenar o banco de dados local, criado automaticamente pela aplicação.
- `.env.example`: modelo das variáveis de ambiente.
- `requirements.txt`: dependências do projeto.
- `.gitignore`: define os arquivos e diretórios que não devem ser publicados no GitHub.

## Como executar o projeto

### 1. Pré-requisitos

- Python 3.13 ou compatível.
- Uma chave de API do Google Gemini.
- Git.

### 2. Clonar o repositório

```bash
git clone URL_DO_REPOSITORIO
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

`http://localhost:8501`

## Objetivo do projeto

O SmartOps AI foi desenvolvido como projeto prático para aplicar conhecimentos de desenvolvimento Python, integração com serviços de Inteligência Artificial, persistência de dados e construção de indicadores operacionais.

A proposta é demonstrar como a IA pode apoiar equipes de operações de TI na interpretação de incidentes, organização de informações e apoio à tomada de decisão.

## Dados e segurança

Os incidentes utilizados para demonstração são fictícios. Nenhum dado confidencial ou informação operacional interna de empresas é utilizado no projeto.

---

**Status:** Projeto em desenvolvimento.