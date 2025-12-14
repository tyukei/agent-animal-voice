import asyncio
import vertexai
from google.genai import types
from vertexai.agent_engines import AdkApp
from musical_instrument_agent.agent import root_agent
from musical_instrument_agent.config import PROJECT_ID, LOCATION, STAGING_BUCKET


vertexai.init(project=PROJECT_ID, location=LOCATION, staging_bucket=STAGING_BUCKET)

async def main():
    # 既存のAgent Engine IDを環境変数から取得（存在する場合）
    from musical_instrument_agent.config import AGENT_ENGINE_ID
    existing_agent_id = AGENT_ENGINE_ID if AGENT_ENGINE_ID else None

    print(f"Deploying with Agent Engine ID: {existing_agent_id}")
    print(f"Agent Name: {root_agent.name}")
    print(f"Agent Description: {root_agent.description}")

    # ADK Appを作成
    adk_app = AdkApp(agent=root_agent)

    # Vertex AI Client を作成
    client = vertexai.Client(
        project=PROJECT_ID,
        location=LOCATION,
        http_options=types.HttpOptions(
            api_version="v1beta1", base_url=f"https://{LOCATION}-aiplatform.googleapis.com/"
        ),
    )

    # Agent Engine にデプロイ
    remote_agent = client.agent_engines.create(
        agent=adk_app,
        config={
            "display_name": root_agent.name,
            "description": root_agent.description,
            "requirements": [
                "google-cloud-aiplatform[adk,agent_engines]>=1.130.0",
                "google-adk==1.21.0",
                "google-genai>=1.55.0",
                "cloudpickle>=3.0,<4",
                "pydantic>=2.6.4",
                "requests>=2.31.0",
            ],
            "extra_packages": ["musical_instrument_agent"],
            "http_options": {
                "base_url": f"https://{LOCATION}-aiplatform.googleapis.com",
                "api_version": "v1beta1",
            },
            "staging_bucket": STAGING_BUCKET,
        },
    )

    print("\n=== Deployment Successful ===")
    # AgentEngineオブジェクトからリソース名を取得
    resource_name = remote_agent.api_resource.name
    agent_id = resource_name.split("/")[-1]

    print(f"Full resource name: {resource_name}")
    print(f"Agent Engine ID: {agent_id}")
    print(f"Display Name: {root_agent.name}")
    print(f"Description: {root_agent.description}")

    # 既存のIDと新しいIDを比較
    if existing_agent_id and existing_agent_id != agent_id:
        print(f"\n⚠️  Agent ID has changed!")
        print(f"   Old ID: {existing_agent_id}")
        print(f"   New ID: {agent_id}")

    if not existing_agent_id or existing_agent_id != agent_id:
        print(f"\n📝 Please update your .env file with:")
        print(f'   AGENT_ENGINE_ID="{agent_id}"')
        print(f"\n🔄 Then run the deploy script again to update the agent configuration:")
        print(f"   uv run python -m musical_instrument_agent.deploy")
    else:
        print(f"\n✅ Agent is correctly configured!")
        print(f"   You can now call the agent programmatically.")

if __name__ == "__main__":
    asyncio.run(main())
