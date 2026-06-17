# MCP Saúde Ocupacional

Servidor MCP (Model Context Protocol) para processamento e análise de Architecture Decision Records (ADRs) do projeto Saúde Ocupacional - Clínica Santa Clara.

## 📋 Ferramentas MCP Implementadas

| Ferramenta | Descrição | Usa IA? |
|-------------|-----------|---------|
| `informacoes` | Informações básicas do servidor | ❌ |
| `decisoes_arquiteturais` | Lista todas as ADRs | ❌ |
| `detalhe_decisao_arquitetural` | Detalhes de uma ADR específica | ❌ |
| `recomendacoes` | Recomendações de implementação | ✅ |
| `listar_consequencias_negativas` | Lista consequências negativas | ❌ |
| `sugerir_contingencia_api_externa` | Sugere contingência para APIs | ✅ |
| `listar_requisitos` | Lista requisitos funcionais | ❌ |
| `listar_adrs_por_requisito` | ADRs por requisito | ❌ |
| `listar_adrs_por_todos_requisitos` | Mapeamento completo | ❌ |

## 🚀 Instalação

```bash
# Criar ambiente virtual
python -m venv .venv

# Ativar (Windows)
.venv\Scripts\activate

# Ativar (Linux/Mac)
source .venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

## 🔑 Configurar Variáveis de Ambiente

```bash
# Copiar arquivo de exemplo
copy .env.example .env

# Editar .env e adicionar sua chave
# OPENROUTER_API_KEY=sua_chave_aqui
```

## 🧪 Como Usar

### Opção 1: Cliente Interativo

```bash
python cliente_mcp.py
```

### Opção 2: MCP Inspector

```bash
mcp dev adrs.py
```

### Opção 3: Servidor MCP Direto

```bash
python adrs.py
```

## 📊 ADRs Documentadas

| ID | Título |
|----|--------|
| ADR-01 | Adoção do Estilo Arquitetural N-Camadas |
| ADR-02 | Integração com APIs Externas para Validação |
| ADR-03 | Autenticação com E-mail e Senha |
| ADR-04 | Uso de Integridade Referencial |
| ADR-05 | Interface Web Baseada em Componentes Padrão |
| ADR-06 | Utilização de Banco de Dados Relacional |

## 📦 Estrutura do Projeto

```
saude-ocupacional/
├── adrs.py              # Servidor MCP com 9 ferramentas
├── ia.py                # Funções de IA (OpenRouter)
├── utilidades.py        # Parsing de ADRs
├── cliente_mcp.py       # Cliente MCP interativo
├── requirements.txt     # Dependências
├── .env.example         # Variáveis de ambiente (modelo)
└── arquitetura/
    └── ADRs_Clinica_Santa_Clara.md  # Documento com 6 ADRs
```

## 🎯 Exemplos de Uso

No cliente interativo, experimente:

- `Quais são as decisões arquiteturais do projeto?`
- `Liste as consequências negativas de todas as ADRs`
- `Quais são os requisitos funcionais mapeados?`
- `Sugira estratégias de contingência para a ADR-02`

## 📝 Autores

Lauane Oliveira da Cunha
Anderson Neves dos Santos

IFBA - Campus Vitória da Conquista
