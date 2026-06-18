from mcp.server.fastmcp import FastMCP
from utilidades import *
from dotenv import load_dotenv
import os

from ia import *

import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
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


if __name__ == "__main__":
    try:
        iniciar_adrs()
        mcp.run()
    except Exception as e:
        raise
