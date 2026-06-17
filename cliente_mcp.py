from mcp.client.stdio import stdio_client
from mcp import ClientSession as session, StdioServerParameters as session_parameters
from dotenv import load_dotenv
from ia import conectar_ia
import asyncio
import sys
import os

MODEL = "openai/gpt-oss-120b:free"

SYSTEM_PROMPT = """
Você é o Arquiteto de Software do projeto Saúde Ocupacional. Seu papel é ajudar desenvolvedores a analisar, evoluir e auditar as decisões arquiteturais.

Quando o usuário solicitar algo, você deve utilizar as ferramentas MCP disponíveis para:
1. Listar as decisões arquiteturais (ADRs) do projeto
2. Obter detalhes de decisões específicas
3. Gerar recomendações de implementação usando IA
4. Listar consequências negativas de cada ADR
5. Sugerir estratégias de contingência para APIs externas

Regras:
- Sempre que precisar de informações sobre ADRs, use as ferramentas disponíveis
- Execute as chamadas de ferramentas no loop enquanto necessário
- Somente após coletar todas as informações, consolide os resultados e retorne a resposta final
"""

async def get_response(ai_connection, mensagem):
    params = session_parameters(command=sys.executable, args=["adrs.py"])
    async with stdio_client(params) as (read, write):
        async with session(read, write) as s:
            await s.initialize()

            list_tools = await s.list_tools()
            arch_tools = [
                {
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.inputSchema
                    }
                } for tool in list_tools.tools
            ]

            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": mensagem}
            ]

            while True:
                response = ai_connection.chat.completions.create(
                    model=MODEL,
                    messages=messages,
                    tools=arch_tools,
                    tool_choice="auto"
                )

                choice = response.choices[0]

                if choice.finish_reason == "stop":
                    print(f"\n{'='*60}")
                    print(f"RESPOSTA FINAL:")
                    print(f"{'='*60}")
                    print(choice.message.content)
                    print(f"{'='*60}\n")
                    break

                if choice.finish_reason == "tool_calls":
                    messages.append(choice.message)

                    for tool in choice.message.tool_calls:
                        print(f"\n[TOOL] Executando: {tool.function.name}")
                        tool_response = await s.call_tool(
                            name=tool.function.name,
                            arguments=eval(tool.function.arguments)
                        )
                        print(f"[OK] '{tool.function.name}' concluída")

                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool.id,
                            "name": tool.function.name,
                            "content": str(tool_response.content)
                        })

if __name__ == "__main__":
    load_dotenv()

    try:
        # Forçar uso do OpenRouter para este cliente
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise Exception("OPENROUTER_API_KEY não encontrada no .env")

        from openai import OpenAI
        connection = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )
        provider = "openrouter"

        print(f"\n[Cliente MCP] Saude Ocupacional")
        print(f"[Provider] {provider}")
        print(f"[Modelo] {MODEL}\n")

        while True:
            try:
                mensagem = input(">>> Digite sua pergunta (ou 'sair' para encerrar): ")
                if mensagem.lower() in ['sair', 'exit', 'quit', '']:
                    print("[Encerrando...]")
                    break

                print(f"\n[Processando] {mensagem}...\n")
                asyncio.run(get_response(connection, mensagem))

            except KeyboardInterrupt:
                print("\n[Encerrando...]")
                break
            except Exception as e:
                print(f"[ERRO] {e}")
                continue

    except Exception as e:
        print(f"[ERRO AO CONECTAR] {e}")
        print("[DICA] Verifique se OPENROUTER_API_KEY esta definida no .env")
