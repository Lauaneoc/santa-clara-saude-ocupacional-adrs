from openai import OpenAI
import json
import re
from dotenv import load_dotenv
import os

# Modelo OpenRouter (grátis)
MODEL = "openai/gpt-oss-120b:free"


def conectar_ia():
    """Conecta ao OpenRouter usando a chave API do .env."""
    load_dotenv()

    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENROUTER_API_KEY não encontrada no .env. "
            "Adicione: OPENROUTER_API_KEY=sua_chave"
        )

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key
    )

    return client


def completar_com_ia(client, prompt):
    """Envia prompt para a IA e retorna a resposta."""
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1000
        )

        if response and len(response.choices):
            return response.choices[0].message.content
        return ""

    except Exception as e:
        print(f"Erro ao chamar IA: {e}")
        return ""


def parse_json_response(text, default_obj):
    """Extrai JSON da resposta da IA."""
    candidate = re.search(r"\{.*\}", text, re.DOTALL)
    if candidate:
        try:
            return json.loads(candidate.group(0))
        except json.JSONDecodeError:
            return default_obj
    return default_obj


def ia_recomendacoes_para_adr(client, adr, linguagem_framework):
    """Gera recomendações de implementação para uma ADR."""
    prompt = f"""
    Você é um arquiteto de software que deve ajudar desenvolvedores a implementar decisões arquiteturais.

    Tarefa:
    Analise a seguinte ADR e forneça recomendações de boas práticas para a implementação.

    Documento:
    {adr}

    Instruções:
    - Retorne um JSON com os campos: "id", "titulo", "status", "decisao" e "recomendacoes".
    - O campo "recomendacoes" deve ser uma lista de sugestões claras.
    - Considere a linguagem/framework: {linguagem_framework}.
    - Não inclua texto extra fora do JSON.
    - Cada recomendação deve ser breve.
    """

    text = completar_com_ia(client, prompt)

    default = {
        "id": adr.get("id"),
        "titulo": adr.get("titulo"),
        "status": adr.get("status"),
        "decisao": adr.get("decisao"),
        "recomendacoes": ["Não foi possível obter recomendações da IA."]
    }
    return parse_json_response(text, default)


def ia_sugerir_contingencia_para_apis(client, adr):
    """Sugere estratégias de contingência para APIs externas."""
    prompt = f"""
    Você é um arquiteto de software especializado em disponibilidade e contingência.

    Tarefa:
    Analise a seguinte Arquitetura Decision Record (ADR) e sugira estratégias de contingência
    para o caso de APIs externas de validação (CPF, CNPJ, CEP, CRM) estarem indisponíveis.

    Documento:
    {adr}

    Instruções:
    - Retorne um JSON somente com os campos: "id", "titulo", "status", "decisao" e "contingencias".
    - O campo "contingencias" deve ser uma lista de estratégias de fallback práticas.
    - Inclua no máximo 5 itens na lista.
    - Não inclua explicações longas nem texto adicional fora do JSON.
    - Use termos claros e diretos.
    """

    text = completar_com_ia(client, prompt)

    default = {
        "id": adr.get("id"),
        "titulo": adr.get("titulo"),
        "status": adr.get("status"),
        "decisao": adr.get("decisao"),
        "contingencias": ["Não foi possível obter estratégia de contingência da IA."]
    }
    return parse_json_response(text, default)


if __name__ == "__main__":
    # Teste
    load_dotenv()

    if not os.getenv("OPENROUTER_API_KEY"):
        print("ERRO: OPENROUTER_API_KEY não encontrada no .env")
        exit(1)

    client = conectar_ia()

    # ADR de teste
    ADR_TESTE = {
        "id": "ADR-02",
        "titulo": "Integração com APIs Externas para Validação",
        "status": "Aceita",
        "decisao": "Integrar o backend com APIs externas responsáveis pela validação das informações fornecidas pelos usuários.",
    }

    print("Testando sugestão de contingência...")
    resultado = ia_sugerir_contingencia_para_apis(client, ADR_TESTE)
    print(json.dumps(resultado, indent=2, ensure_ascii=False))
