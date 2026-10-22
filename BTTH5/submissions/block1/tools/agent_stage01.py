"""LangChain agent của stage 01: read_file, write_file."""

from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware, ToolCallLimitMiddleware
from langchain_openai import ChatOpenAI 

from config import MODEL_CALL_LIMIT, TOOL_CALL_LIMIT, Settings
from observer import ObserverMiddleware
from prompts import build_system_prompt
from tools import list_files, read_file, write_file

TOOLS = [list_files, read_file, write_file]


from langchain_google_genai import ChatGoogleGenerativeAI

def build_model(settings: Settings):
    return ChatGoogleGenerativeAI(
        model=settings.model_name,
        google_api_key=settings.api_key,
    )


def system_prompt() -> str:
    return build_system_prompt()


def capabilities() -> dict:
    return {"tools": [t.name for t in TOOLS], "skills": [], "skill_diagnostics": []}


def build_agent(model):
    return create_agent(
        model=model,
        tools=TOOLS,
        system_prompt=system_prompt(),
        middleware=[
            ModelCallLimitMiddleware(run_limit=MODEL_CALL_LIMIT, exit_behavior="end"),
            ToolCallLimitMiddleware(run_limit=TOOL_CALL_LIMIT),
            ObserverMiddleware(),  # cuối danh sách = sát model/tool invocation nhất
        ],
    )
