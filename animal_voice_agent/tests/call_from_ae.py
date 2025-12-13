import sys
from pathlib import Path

# プロジェクトルートをパスに追加
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import os
import asyncio
import vertexai
from vertexai import agent_engines
from animal_voice_agent.config import PROJECT_ID, LOCATION, AGENT_ENGINE_ID

import asyncio
import vertexai
from vertexai import agent_engines
from animal_voice_agent.config import PROJECT_ID, LOCATION, AGENT_ENGINE_ID

async def main():
    vertexai.init(project=PROJECT_ID, location=LOCATION)

    name = f"projects/{PROJECT_ID}/locations/{LOCATION}/reasoningEngines/{AGENT_ENGINE_ID}"
    remote_agent = agent_engines.get(name)

    # どのoperationがあるか確認（便利）
    print(remote_agent.operation_schemas())

    # 認証付き agent card を取得
    card = await remote_agent.handle_authenticated_agent_card()
    print(card)  # card["url"] が A2A の base URL

asyncio.run(main())