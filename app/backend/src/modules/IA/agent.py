from agno.agent import Agent
from agno.models.ollama import Ollama

local_agent = Agent(
    model=Ollama(id="qwen2.5:3b"),
    instructions=["Seja conciso, direto e objetivo. Explique de forma sucinta sem floreios."],
    markdown=False
)

# Execução
local_agent.print_response("Explique resumidamente o que é o docker.", stream=True)