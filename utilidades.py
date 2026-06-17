import re

def separar_adrs(conteudo):
    # Procura blocos de ADR até o próximo "---" ou fim do arquivo
    padrao = r"## (ADR-\d+): (.+?)\n\n(.*?)(?=\n---|\Z)"

    blocos = re.findall(padrao, conteudo, re.DOTALL)

    adrs = {}
    for match in blocos:
        id = match[0]
        titulo = match[1]
        bloco_conteudo = match[2]
        
        # Extrai contexto
        contexto_match = re.search(
            r"###\s*Contexto\s*(.*?)(?=\n###|\Z)",
            bloco_conteudo,
            re.DOTALL
        )

        # Extrai decisão
        decisao_match = re.search(
            r"###\s*Decisão\s*(.*?)(?=\n###|\Z)",
            bloco_conteudo,
            re.DOTALL
        )

        # Extrai status
        status_match = re.search(
            r"###\s*Status\s*([^\n]+)",
            bloco_conteudo
        )

        # Extrai consequências
        consequencias_match = re.search(
            r"###\s*Consequências\s*(.*?)(?=\n###|\n---|$)",
            bloco_conteudo,
            re.DOTALL
        )

        # Extrai apenas as consequências negativas
        consequencias_negativas = []
        if consequencias_match:
            negativas = re.findall(
                r"- \*\*Negativa:\*\*\s*(.+?)(?=\n-|\n\n|$)",
                consequencias_match.group(1),
                re.DOTALL
            )
            consequencias_negativas = [n.strip() for n in negativas]

        adr = {
            "id": id,
            "titulo": titulo,
            "contexto": contexto_match.group(1).strip() if contexto_match else None,
            "decisao": decisao_match.group(1).strip() if decisao_match else None,
            "status": status_match.group(1).strip() if status_match else None,
            "consequencias_negativas": consequencias_negativas,
        }
        adrs[id] = adr

    return adrs

def carregar_adrs(arquivo):
    carregadas, adrs = False, []

    try:
        with open(arquivo, "r", encoding="utf-8") as a:
            adrs = separar_adrs(a.read())
            carregadas = True

            a.close()
    except Exception as e:
        print(f"erro carregando ADRs: {e}")

    return carregadas, adrs