from mcp.server.fastmcp import FastMCP
from utilidades import *
from dotenv import load_dotenv
import os

from ia import *

import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

ARQUIVO_ADRS = 'arquitetura/ADRs_Clinica_Santa_Clara.md'

NOME = "saude-ocupacional"
mcp = FastMCP(NOME)
logger = logging.getLogger(NOME)

INFO = {
    "descricao": "Um servidor MCP para processamento de ADRs do projeto Saúde Ocupacional.",
    "versao": "1.0",
}

global adrs
adrs = None
global adrs_carregadas
adrs_carregadas = False

load_dotenv()

provider = None
connection = None

def iniciar_adrs():
    global adrs
    global adrs_carregadas

    if not adrs or len(adrs) == 0:
        adrs_carregadas, adrs = carregar_adrs(ARQUIVO_ADRS)
        if adrs_carregadas:
            logger.info("ADRs carregadas com sucesso")
        else:
            logger.info("Erro carregando ADRs")
    return adrs_carregadas, adrs


def iniciar_ia():
    global provider
    global connection
    if provider is None or connection is None:
        provider, connection = conectar_ia()
    return provider, connection

@mcp.tool(name="informacoes", title="lista de informacoes", description="apresenta lista de informacoes basicas sobre este servidor mcp")
def get_info():
    return INFO

@mcp.tool(name="decisoes_arquiteturais", title="lista de decisoes arquiteturais do saude ocupacional", description="retorna uma lista completa das decisoes arquiteturais do projeto Saúde Ocupacional")
def get_adrs():
    decisoes = []
    carregadas, adrs = iniciar_adrs()
    if carregadas:
        for adr in adrs.values():
            decisoes.append({
                "id": adr["id"],
                "titulo": adr["titulo"]
            })
    return decisoes

@mcp.tool(name="detalhe_decisao_arquitetural", title="lista os detalhes de uma decisao arquitetural", description="encontra as informacoes sobre uma decisao arquitetural atraves de um identificador unico")
def get_detalhes_adr(id_adr):
    detalhes = {}
    carregadas, adrs = iniciar_adrs()
    if carregadas:
        detalhes = adrs.get(id_adr, {})
    return detalhes

@mcp.tool(name="recomendacoes", title="recomendacoes para uma decisao arquitetural", description="dado o identificador de uma decisao arquitetural retorna recomendacoes de boas praticas sobre como implementar")
def get_recomendacoes(id_adr, linguagem_framework):
    recomendacoes = {}
    carregadas, adrs = iniciar_adrs()
    if carregadas and id_adr in adrs:
        provider, connection = iniciar_ia()
        recomendacoes = ia_recomendacoes_para_adr(provider, connection, adrs[id_adr], linguagem_framework)
    return recomendacoes

@mcp.tool(name="listar_consequencias_negativas", title="lista consequencias negativas das ADRs", description="retorna as consequencias negativas registradas em cada ADR")
def listar_consequencias_negativas():
    lista = []
    carregadas, adrs = iniciar_adrs()
    if carregadas:
        for adr in adrs.values():
            lista.append({
                "id": adr["id"],
                "titulo": adr["titulo"],
                "status": adr.get("status"),
                "consequencias_negativas": adr.get("consequencias_negativas", [])
            })
    return lista

@mcp.tool(name="sugerir_contingencia_api_externa", title="sugere contingencia para APIs externas de validacao", description="usa IA para sugerir estrategias de contingencia quando APIs de validacao estiverem indisponiveis")
def sugerir_contingencia_api_externa(id_adr):
    resultado = {}
    carregadas, adrs = iniciar_adrs()
    if carregadas and id_adr in adrs:
        provider, connection = iniciar_ia()
        resultado = ia_sugerir_contingencia_para_apis(provider, connection, adrs[id_adr])
    return resultado


# ============================================
# MAPEAMENTO DE REQUISITOS PARA ADRs
# ============================================
# Relaciona cada requisito funcional com as ADRs que derivaram dele

MAPEAMENTO_REQUISITOS_ADRS = {
    "RF001": ["ADR-02", "ADR-06"],  # Cadastrar Empresa -> APIs externas (CNPJ) + Banco relacional
    "RF005": ["ADR-02", "ADR-04"],  # Cadastrar Paciente -> APIs externas (CPF, CEP) + Integridade referencial
    "RF009": ["ADR-03"],            # Cadastrar Login -> Autenticação
    "RF013": ["ADR-02"],            # Cadastrar Médico -> APIs externas (CRM)
    "RF021": ["ADR-04"],            # Cadastrar Agendamento -> Integridade referencial
}

DESCRICAO_REQUISITOS = {
    "RF001": "Cadastrar Empresa com validação de CNPJ e verificação de duplicidade",
    "RF005": "Cadastrar Paciente vinculado às empresas, incluindo validação de CPF e CEP",
    "RF009": "Cadastrar Login permitindo criação de credenciais de acesso utilizando e-mail e senha",
    "RF013": "Cadastrar Médico com validação de CRM",
    "RF021": "Cadastrar Agendamento relacionando empresa, paciente e exame",
}


@mcp.tool(name="listar_requisitos", title="lista requisitos funcionais relacionados as ADRs", description="retorna a lista de requisitos funcionais mapeados e suas ADRs relacionadas")
def listar_requisitos():
    """
    Lista todos os requisitos funcionais mapeados e as ADRs relacionadas a cada um.
    """
    requisitos = []
    for req_id, req_desc in DESCRICAO_REQUISITOS.items():
        requisitos.append({
            "id": req_id,
            "descricao": req_desc,
            "adrs_relacionadas": MAPEAMENTO_REQUISITOS_ADRS.get(req_id, [])
        })
    return requisitos


@mcp.tool(name="listar_adrs_por_requisito", title="lista ADRs relacionadas a um requisito", description="retorna as ADRs que derivam de um requisito funcional especificado, mostrando a rastreabilidade")
def listar_adrs_por_requisito(requisito_id):
    """
    Relaciona ADRs com requisitos funcionais do documento de requisitos.
    Permite visualizar qual requisito originou cada decisão arquitetural.

    Exemplos de uso:
    - listar_adrs_por_requisito("RF001") -> Retorna ADR-02 e ADR-06
    - listar_adrs_por_requisito("RF009") -> Retorna ADR-03
    """
    if requisito_id not in MAPEAMENTO_REQUISITOS_ADRS:
        return {
            "erro": f"Requisito {requisito_id} não encontrado",
            "requisitos_disponiveis": list(MAPEAMENTO_REQUISITOS_ADRS.keys()),
            "dica": "Use a ferramenta 'listar_requisitos' para ver todos os requisitos disponíveis"
        }

    carregadas, adrs = iniciar_adrs()
    resultado = {
        "requisito": requisito_id,
        "descricao": DESCRICAO_REQUISITOS.get(requisito_id, ""),
        "adrs": []
    }

    for adr_id in MAPEAMENTO_REQUISITOS_ADRS[requisito_id]:
        if adr_id in adrs:
            resultado["adrs"].append({
                "id": adrs[adr_id]["id"],
                "titulo": adrs[adr_id]["titulo"],
                "decisao": adrs[adr_id]["decisao"],
                "status": adrs[adr_id]["status"]
            })
        else:
            resultado["adrs"].append({
                "id": adr_id,
                "erro": f"ADR {adr_id} não encontrada no documento"
            })

    return resultado


@mcp.tool(name="listar_adrs_por_todos_requisitos", title="lista mapeamento completo de requisitos para ADRs", description="retorna o mapeamento completo de todos os requisitos funcionais e suas ADRs relacionadas em uma unica chamada")
def listar_adrs_por_todos_requisitos():
    """
    Retorna o mapeamento completo de requisitos para ADRs.
    Útil para visualizar a rastreabilidade completa em uma única chamada.
    """
    carregadas, adrs = iniciar_adrs()

    resultado = {
        "mapeamento": [],
        "total_requisitos": len(MAPEAMENTO_REQUISITOS_ADRS),
        "total_adrs_envolvidas": len(set([adr for adrs_list in MAPEAMENTO_REQUISITOS_ADRS.values() for adr in adrs_list]))
    }

    for req_id in DESCRICAO_REQUISITOS.keys():
        item = {
            "requisito": req_id,
            "descricao": DESCRICAO_REQUISITOS[req_id],
            "adrs": []
        }

        for adr_id in MAPEAMENTO_REQUISITOS_ADRS.get(req_id, []):
            if adr_id in adrs:
                item["adrs"].append({
                    "id": adrs[adr_id]["id"],
                    "titulo": adrs[adr_id]["titulo"],
                    "decisao": adrs[adr_id]["decisao"],
                    "status": adrs[adr_id]["status"]
                })

        resultado["mapeamento"].append(item)

    return resultado

if __name__ == "__main__":
    try:
        iniciar_adrs()
        mcp.run()
    except Exception as e:
        raise

