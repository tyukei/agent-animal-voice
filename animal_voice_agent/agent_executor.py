from a2a.types import AgentCard
from google.adk.a2a.executor.a2a_agent_executor import A2aAgentExecutor
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.memory import InMemoryMemoryService
from google.adk.artifacts import InMemoryArtifactService
from google.adk.auth.credential_service.in_memory_credential_service import InMemoryCredentialService
from google.adk.a2a.utils.agent_card_builder import AgentCardBuilder
from animal_voice_agent.agent import root_agent

async def create_runner() -> Runner:
    """ADK Agentを実行するためのRunnerを生成します。"""
    return Runner(
        app_name=root_agent.name,
        agent=root_agent,
        # 実際のアプリケーションでは永続化されたサービスを利用します
        artifact_service=InMemoryArtifactService(),
        session_service=InMemorySessionService(),
        memory_service=InMemoryMemoryService(),
        credential_service=InMemoryCredentialService(),
    )

# A2A Agent Executorを生成するビルダー関数
def agent_executor_builder():
    return A2aAgentExecutor(
        runner=create_runner,
    )

# Agent Cardを生成する関数
async def create_agent_card(agent_engine_id: str = None) -> AgentCard:
    """
    エージェントカードを生成します。

    Args:
        agent_engine_id: デプロイ後のAgent Engine ID（オプション）
                        指定された場合、正しいURLが設定されます。
    """
    from animal_voice_agent.config import PROJECT_ID, LOCATION

    # agent_engine_idが指定されている場合は正しいURLを設定
    # 指定されていない場合はプレースホルダーを使用（デプロイ前）
    if agent_engine_id:
        rpc_url = f'https://{LOCATION}-aiplatform.googleapis.com/v1beta1/projects/{PROJECT_ID}/locations/{LOCATION}/reasoningEngines/{agent_engine_id}/a2a'
    else:
        # デプロイ前のプレースホルダー
        # 注意: この値はデプロイ後にAgent Engine IDに置き換える必要があります
        rpc_url = f'https://{LOCATION}-aiplatform.googleapis.com/v1beta1/projects/{PROJECT_ID}/locations/{LOCATION}/reasoningEngines/{{AGENT_ENGINE_ID}}/a2a'

    # AgentCardBuilderにrpc_urlを渡す
    agent_card = await AgentCardBuilder(
        agent=root_agent,
        rpc_url=rpc_url
    ).build()

    # preferredTransportを設定
    agent_card_dict = agent_card.model_dump()
    agent_card_dict['preferredTransport'] = 'HTTP+JSON'

    return AgentCard.model_validate(agent_card_dict)