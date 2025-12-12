from a2a.types import AgentCard
from google.adk.a2a.executor.a2a_agent_executor import A2aAgentExecutor
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.memory import InMemoryMemoryService
from google.adk.artifacts import InMemoryArtifactService
from google.adk.auth.credential_service.in_memory_credential_service import InMemoryCredentialService
from google.adk.a2a.utils.agent_card_builder import AgentCardBuilder

# ADKで作成したAgentをインポート
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

# Agent Cardを生成する非同期関数
async def create_agent_card() -> AgentCard:
    builder = AgentCardBuilder(agent=root_agent)
    return await builder.build()