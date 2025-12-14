from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.memory import InMemoryMemoryService
from google.adk.artifacts import InMemoryArtifactService
from google.adk.auth.credential_service.in_memory_credential_service import InMemoryCredentialService
from musical_instrument_agent.agent import root_agent

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
