from mcp.server.fastmcp import FastMCP
from pathlib import Path

app = FastMCP("Markdown Writer")

def save_markdown(
    topic: str,
    content: str,
    folder: str = str(Path.home() / "Documents"),
    filename: str = "output.md"
):
    folder_path = Path(folder).expanduser()
    folder_path.mkdir(parents=True, exist_ok=True)
    file_path = folder_path / filename

    with file_path.open("w", encoding="utf-8") as f:
        f.write(f"# {topic}\n\n{content}")

    return {
        "status": "saved",
        "path": str(file_path)
    }

# MCPツールとして登録（デコレータの代わり）
app.tool()(save_markdown)

if __name__ == "__main__":
    app.run()