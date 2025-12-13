"""
カスタムエージェントカードを使用したデプロイスクリプト

ユーザーが期待する形式のシンプルなエージェントカードを手動で作成し、
正しいURLを設定してデプロイします。
"""
import asyncio
import vertexai
from google.genai import types
from vertexai.preview.reasoning_engines import A2aAgent
from a2a.types import AgentCard, AgentSkill, AgentCapabilities
from animal_voice_agent.agent_executor import agent_executor_builder
from animal_voice_agent.config import PROJECT_ID, LOCATION, STAGING_BUCKET, AGENT_ENGINE_ID


vertexai.init(project=PROJECT_ID, location=LOCATION, staging_bucket=STAGING_BUCKET)


async def main():
    # 既存のAgent Engine IDを使用
    if not AGENT_ENGINE_ID:
        print("Error: AGENT_ENGINE_ID is not set in .env file")
        print("Please deploy once to get an ID, then run this script")
        return

    print(f"Using existing Agent Engine ID: {AGENT_ENGINE_ID}")

    # カスタムスキルを定義
    skill = AgentSkill(
        id="animal_voice",
        name="Animal_voice",
        description="ユーザーから受け取った動物の鳴き声に関する質問に対して回答します。",
        tags=["動物", "鳴き声", "癒し"],
        examples=[{
            "input": {"text": "リャマってどんな鳴き声するの？"},
            "output": [{"text": "リャマは「フフフ」や「プー」といった柔らかい鳴き声を出します"}]
        }],
    )

    # 正しいURLを使用してエージェントカードを作成
    agent_url = f"https://{LOCATION}-aiplatform.googleapis.com/v1beta1/projects/{PROJECT_ID}/locations/{LOCATION}/reasoningEngines/{AGENT_ENGINE_ID}/a2a"

    agent_card = AgentCard(
        name="animal_voice",
        description="ユーザーから受け取った動物の鳴き声に関する質問に対して回答するエージェントです。",
        url=agent_url,
        version="0.0.1",
        default_input_modes=["text/plain"],
        default_output_modes=["text/plain"],
        capabilities=AgentCapabilities(streaming=True),
        skills=[skill],
        preferred_transport="HTTP+JSON",
        protocol_version="0.3.0",
    )

    print(f"\nAgent Card URL: {agent_card.url}")
    print(f"Agent Card Name: {agent_card.name}")
    print(f"Agent Card Skills: {[s.name for s in agent_card.skills]}")

    # A2aAgentオブジェクトを作成
    a2a_agent = A2aAgent(agent_card=agent_card, agent_executor_builder=agent_executor_builder)
    a2a_agent.set_up()

    # クライアントを作成
    client = vertexai.Client(
        project=PROJECT_ID,
        location=LOCATION,
        http_options=types.HttpOptions(
            api_version="v1beta1", base_url=f"https://{LOCATION}-aiplatform.googleapis.com/"
        ),
    )

    # デプロイ（既存のIDを上書き）
    print(f"\nDeploying agent to Agent Engine {AGENT_ENGINE_ID}...")

    remote_a2a_agent = client.agent_engines.create(
        agent=a2a_agent,
        config={
            "display_name": agent_card.name,
            "description": agent_card.description,
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

    # デプロイ結果を表示
    resource_name = remote_a2a_agent.api_resource.name
    new_agent_id = resource_name.split("/")[-1]

    print("\n=== Deployment Successful ===")
    print(f"Agent Engine ID: {new_agent_id}")
    print(f"Agent URL in card: {agent_url}")

    if new_agent_id != AGENT_ENGINE_ID:
        print(f"\n⚠️ Warning: New Agent ID created: {new_agent_id}")
        print(f"   Update .env with: AGENT_ENGINE_ID=\"{new_agent_id}\"")
        print(f"   Then run this script again")
    else:
        print(f"\n✅ Agent successfully deployed with correct URL!")


if __name__ == "__main__":
    asyncio.run(main())
