from pathlib import Path
from mcp.server.mcpserver import MCPServer

DOCS = Path(__file__).parent / "docs"
mcp = MCPServer("file-search")

@mcp.tool()
def search_files(query: str) -> list[dict]:
    """Ищет слово или фразу во всех документах компании (папка docs).
    Используй, когда вопрос касается правил, сроков или контактов компании."""
    hits = []
    for f in DOCS.glob("*.txt"):
        for line in f.read_text(encoding="utf-8").splitlines():
            if query.lower() in line.lower():
                hits.append({"file": f.name, "text": line})
    return hits

if __name__ == "__main__":
    mcp.run()
