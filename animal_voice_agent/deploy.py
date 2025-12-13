import asyncio
import vertexai
from google.genai import types
from vertexai.preview.reasoning_engines import A2aAgent
from vertexai.preview.reasoning_engines.templates.a2a import create_agent_card
from animal_voice_agent.agent_executor import agent_executor_builder, create_agent_card as create_adk_agent_card
from animal_voice_agent.config import PROJECT_ID, LOCATION, STAGING_BUCKET


vertexai.init(project=PROJECT_ID, location=LOCATION, staging_bucket=STAGING_BUCKET)

async def main():
    # 既存のAgent Engine IDを環境変数から取得（存在する場合）
    from animal_voice_agent.config import AGENT_ENGINE_ID
    existing_agent_id = AGENT_ENGINE_ID if AGENT_ENGINE_ID else None

    print(f"Deploying with Agent Engine ID: {existing_agent_id}")

    # ADKのユーティリティでAgentCardの情報を生成
    # 既存のAgent IDがある場合は、それを使用して正しいURLを設定
    adk_agent_card = await create_adk_agent_card(agent_engine_id=existing_agent_id)

    print(f"Agent Card URL (before conversion): {adk_agent_card.url}")

    # Agent Engineが要求する形式にAgentCardを変換
    agent_card = create_agent_card(agent_card=adk_agent_card.model_dump())

    print(f"Agent Card URL (after conversion): {agent_card.url}")
    
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
                "google-cloud-aiplatform[adk,agent_engines]>=1.130.0",
                "google-adk==1.21.0",
                "google-genai>=1.55.0",
                "a2a-sdk>=0.3.21",
                "cloudpickle>=3.0,<4",
                "pydantic>=2.6.4",
            ],
            "extra_packages": ["animal_voice_agent"],
            "http_options": {
                "base_url": f"https://{LOCATION}-aiplatform.googleapis.com",
                "api_version": "v1beta1",
            },
            "staging_bucket": STAGING_BUCKET,
        },
    )

    print("\n=== Deployment Successful ===")
    # AgentEngineオブジェクトからリソース名を取得
    resource_name = remote_a2a_agent.api_resource.name
    agent_id = resource_name.split("/")[-1]

    print(f"Full resource name: {resource_name}")
    print(f"Agent Engine ID: {agent_id}")
    print(f"Display Name: {a2a_agent.agent_card.name}")
    print(f"Description: {a2a_agent.agent_card.description}")

    # 既存のIDと新しいIDを比較
    if existing_agent_id and existing_agent_id != agent_id:
        print(f"\n⚠️  Agent ID has changed!")
        print(f"   Old ID: {existing_agent_id}")
        print(f"   New ID: {agent_id}")

    if not existing_agent_id or existing_agent_id != agent_id:
        print(f"\n📝 Please update your .env file with:")
        print(f'   AGENT_ENGINE_ID="{agent_id}"')
        print(f"\n🔄 Then run the deploy script again to update the agent URL:")
        print(f"   uv run python -m animal_voice_agent.deploy")
    else:
        print(f"\n✅ Agent URL is correctly configured!")
        print(f"   You can now call the agent programmatically.")

if __name__ == "__main__":
    asyncio.run(main())
