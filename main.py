# main.py

import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from mcp_markdown_writer import save_markdown

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
あなたはMarkdownドキュメント生成のアシスタントです。

ユーザーが自然言語で与える「トピック」や「指示文」から、
MCPツール `save_markdown` に渡すためのJSON構造を生成してください。

ツールの定義は以下の通りです：

name: save_markdown  
description: 自然言語で入力された内容をMarkdown形式で保存します。  
parameters:
- topic: ドキュメントのタイトル（string、必須）
- content: Markdown本文（string、必須）
- folder: 保存先パス（string、省略可能、デフォルトは ~/Documents）
- filename: 保存ファイル名（string、省略可能、デフォルトは output.md）

出力は以下の形式のJSONオブジェクトのみとしてください：

{
  "topic": "トピック名",
  "content": "# Markdown構造の本文",
  "folder": "/Users/yourname/Documents",
  "filename": "ファイル名.md"
}

説明や補足、囲み記号は一切不要です。
"""

def chatgpt_to_json(user_prompt: str) -> dict:
    res = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0
    )
    return json.loads(res.choices[0].message.content)

def main():
    print("🗣️ 自然言語で保存したい内容を指示してください:")
    user_input = input("🧠 入力: ")

    print("🧠 ChatGPTに問い合わせ中...\n")
    structured = chatgpt_to_json(user_input)

    print("📦 ChatGPT出力:")
    print(json.dumps(structured, indent=2, ensure_ascii=False))

    print("\n🚀 実行中...\n")
    result = save_markdown(**structured)

    print("✅ 保存完了:")
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()