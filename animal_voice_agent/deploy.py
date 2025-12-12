import asyncio
import os
import vertexai
from dotenv import load_dotenv
from google.genai import types
from vertexai.preview.reasoning_engines import A2aAgent
from vertexai.preview.reasoning_engines.templates.a2a import create_agent_card
from animal_voice_agent.agent_executor import agent_executor_builder, create_agent_card as create_adk_agent_card
from animal_voice_agent.config import PROJECT_ID, LOCATION, STAGING_BUCKET



vertexai.init(project=PROJECT_ID, location=LOCATION, staging_bucket=STAGING_BUCKET)

async def main():
    # ADKのユーティリティでAgentCardの情報を生成
    adk_agent_card = await create_adk_agent_card()

    # Agent Engineが要求する形式にAgentCardを変換
    agent_card = create_agent_card(agent_name=adk_agent_card.name, description=adk_agent_card.description, skills=adk_agent_card.skills)
    
    # デプロイ用のA2aAgentオブジェクトを作成
    a2a_agent = A2aAgent(agent_card=agent_card, agent_executor_builder=agent_executor_builder)
    a2a_agent.set_up()

    client = vertexai.Client(
        project=PROJECT_ID,
        location=LOCATION,
        http_options=types.HttpOptions(
            api_version="v1beta1", base_url=f"https://{LOCATION}-aiplatform.googleapis.com/"
        ),
    )
        
    remote_a2a_agent = client.agent_engines.create(
        agent=a2a_agent,
        config={
            "display_name": a2a_agent.agent_card.name,
            "description": a2a_agent.agent_card.description,
            "requirements": [
                "google-cloud-aiplatform[agent_engines,adk]>=1.112.0",
                "a2a-sdk>=0.3.5",
                "cloudpickle==3.0"
            ],
            "extra_packages": ["animal_voice"],
            "http_options": {
                "base_url": f"https://{LOCATION}-aiplatform.googleapis.com",
                "api_version": "v1beta1",
            },
            "staging_bucket": STAGING_BUCKET,
        },
    )

    print(remote_a2a_agent)

if __name__ == "__main__":
    asyncio.run(main())