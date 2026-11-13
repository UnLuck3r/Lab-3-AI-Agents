import asyncio
import ollama
from mcp import Client, StdioServerParameters

MODEL = "qwen3.5:2b"
server = StdioServerParameters(command="python", args=["server.py"])

SYSTEM = ("Ты помощник сотрудников компании. Отвечай только по документам. "
          "Если в документах нет ответа, так и скажи.")

async def ask(question):
    async with Client(server) as client:
        tools = [{"type": "function",
                  "function": {"name": t.name,
                               "description": t.description,
                               "parameters": t.input_schema}}
                 for t in (await client.list_tools()).tools]
        messages = [{"role": "system", "content": SYSTEM},
                    {"role": "user", "content": question}]
        for step in range(5):
            reply = ollama.chat(model=MODEL, messages=messages, tools=tools)
            messages.append(reply.message)
            if not reply.message.tool_calls:
                return reply.message.content
            for call in reply.message.tool_calls:
                print(f"Шаг {step + 1}: {call.function.name}({call.function.arguments})")
                result = await client.call_tool(call.function.name, call.function.arguments)
                text = "\n".join(c.text for c in result.content) or "ничего не найдено"
                messages.append({"role": "tool", "tool_name": call.function.name,
                                 "content": text})
        return "Не успел ответить за 5 шагов"

question = input("Ваш вопрос: ")
print(asyncio.run(ask(question)))
